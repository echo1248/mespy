#!/usr/bin/env bash
set -euo pipefail

# ======================
# 配置区（与 supervisor 配置一致）
# ======================
CONFIG_NAME="mes_services.conf"
SUPERVISOR_DIR="/etc/supervisor/conf.d"
BASE_PATH="/opt/mes"

# ======================
# 语言项目目录配置
# ======================
declare -A PROJECT_ROOTS=(
    ["mes"]="${BASE_PATH}/service/mespy"  # mes服务
)

declare -A SERVICES=(
    ["mes"]="mes_services:mes_service_8000"
)

# ======================
# 日志配置（同时输出到终端和文件）
# ======================
LOG_DIR="${BASE_PATH}/deploy_logs"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
LOG_FILE="${LOG_DIR}/deploy_${TIMESTAMP}.log"
mkdir -p "$LOG_DIR"

log() {
    local message="$(date '+%Y-%m-%d %T') $1"
    echo "$message" | tee -a "$LOG_FILE" >/dev/tty
}

# ======================
# Git 相关操作
# ======================
git_update() {
    local project_dir="$1"
    local service_code="$2"

    if [ ! -d "${project_dir}/.git" ]; then
        log "[警告] ${service_code}: 非 Git 仓库，跳过更新"
        return
    fi

    log "${service_code}: 正在更新 Git 仓库 (${project_dir})"

    # 获取最新变更
    if ! git -C "$project_dir" fetch --all; then
        log "[错误] ${service_code}: Git fetch 失败"
        return 1
    fi

    # 获取当前分支
    local current_branch=$(git -C "$project_dir" rev-parse --abbrev-ref HEAD)

    # 拉取最新代码
    if ! git -C "$project_dir" pull origin "$current_branch"; then
        log "[错误] ${service_code}: Git pull 失败"
        return 1
    fi

    log "${service_code}: 成功更新到最新版本 (分支: ${current_branch})"
    return 0
}

# ======================
# 使用说明
# ======================
usage() {
    echo "使用方法: $0 [选项] [服务代码...]"
    echo "选项:"
    echo "  -h, --help      显示帮助信息"
    echo "  -g, --git       重启前更新 Git 仓库"
    echo "服务代码:"
    echo "  mes             服务"
    echo ""
    echo "示例:"
    echo "  $0 mes          # 重启服务"
    echo "  $0 -g mes       # 更新代码并重启服务"
    echo "  $0              # 重启所有服务"
    exit 0
}

# ======================
# 主流程
# ======================
# 解析参数
RESTART_SERVICES=()
UPDATE_GIT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            usage
            ;;
        -g|--git)
            UPDATE_GIT=true
            shift
            ;;
        *)
            if [[ -v SERVICES["$1"] ]]; then
                RESTART_SERVICES+=("$1")
            else
                log "[错误] 未知的服务代码: $1"
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

log "========== 开始部署 =========="

# 检查依赖项
log "正在检查依赖项..."
for cmd in git supervisorctl python3; do
    if ! command -v "$cmd" >/dev/null; then
        log "[错误] 缺少依赖: $cmd"
        exit 1
    fi
done

# 如果需要更新 Git
if [ "$UPDATE_GIT" = true ]; then
    log "正在更新 Git 仓库..."
    if [ ${#RESTART_SERVICES[@]} -eq 0 ]; then
        # 更新所有服务
        for service_code in "${!PROJECT_ROOTS[@]}"; do
            git_update "${PROJECT_ROOTS[$service_code]}" "$service_code" || true
        done
    else
        # 只更新指定服务
        for service_code in "${RESTART_SERVICES[@]}"; do
            git_update "${PROJECT_ROOTS[$service_code]}" "$service_code" || true
        done
    fi
fi

# 部署配置文件
log "正在部署配置文件..."
sudo cp -v "${PROJECT_ROOTS[zh]}/deploy/${CONFIG_NAME}" "${SUPERVISOR_DIR}/" || {
    log "[错误] 配置文件复制失败"
    exit 1
}

# 重载 Supervisor
log "正在重载 Supervisor..."
sudo supervisorctl reread && sudo supervisorctl update || {
    log "[错误] Supervisor 重载失败"
    exit 1
}

# 确定要重启的服务
if [[ ${#RESTART_SERVICES[@]} -eq 0 ]]; then
    log "未指定服务，将重启所有服务"
    SERVICES_TO_RESTART=("${SERVICES[@]}")
else
    SERVICES_TO_RESTART=()
    for service_code in "${RESTART_SERVICES[@]}"; do
        SERVICES_TO_RESTART+=("${SERVICES[$service_code]}")
    done
fi

# 重启服务
for service in "${SERVICES_TO_RESTART[@]}"; do
    log "正在重启服务 $service..."
    if ! sudo supervisorctl restart "$service"; then
        log "[错误] 服务 $service 重启失败"
        log "当前状态: $(sudo supervisorctl status "$service")"
        exit 1
    fi
done

# 验证状态
log "正在验证服务状态..."
for service in "${SERVICES_TO_RESTART[@]}"; do
    status=$(sudo supervisorctl status "$service" | awk '{print $2}')
    log "$service 状态: $status"
done

log "========== 部署成功 =========="
log "详细日志已保存至: $LOG_FILE"