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
    ["mes"]="${BASE_PATH}/service/mespy"
)

declare -A SERVICES=(
    ["8000"]="mes_services:mes_8000"
    ["8100"]="mes_services:mes_8100"
)

# 反向映射，用于验证
declare -A SERVICE_PORTS
for port in "${!SERVICES[@]}"; do
    SERVICE_PORTS["${SERVICES[$port]}"]=$port
done

# ======================
# 日志配置
# ======================
LOG_DIR="${BASE_PATH}/deploy_logs"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
LOG_FILE="${LOG_DIR}/deploy_${TIMESTAMP}.log"
mkdir -p "$LOG_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %T')
    local colored_message

    case "$level" in
        "ERROR")
            colored_message="${RED}[错误]${NC} $message"
            ;;
        "WARN")
            colored_message="${YELLOW}[警告]${NC} $message"
            ;;
        "INFO")
            colored_message="${BLUE}[信息]${NC} $message"
            ;;
        "SUCCESS")
            colored_message="${GREEN}[成功]${NC} $message"
            ;;
        *)
            colored_message="$message"
            ;;
    esac

    echo -e "${timestamp} ${colored_message}" | tee -a "$LOG_FILE" >/dev/tty
}

# ======================
# Git 相关操作
# ======================
git_update() {
    local project_dir="$1"
    local service_code="$2"

    if [ ! -d "${project_dir}/.git" ]; then
        log "WARN" "${service_code}: 非 Git 仓库，跳过更新"
        return 0
    fi

    log "INFO" "${service_code}: 正在更新 Git 仓库 (${project_dir})"

    # 检查是否有未提交的更改
    if ! git -C "$project_dir" diff --quiet; then
        log "WARN" "${service_code}: 存在未提交的更改，尝试暂存"
        git -C "$project_dir" stash
    fi

    # 获取当前分支
    local current_branch=$(git -C "$project_dir" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

    # 获取最新变更
    if ! git -C "$project_dir" fetch --all --quiet; then
        log "ERROR" "${service_code}: Git fetch 失败"
        return 1
    fi

    # 拉取最新代码
    if ! git -C "$project_dir" pull origin "$current_branch" --quiet; then
        log "ERROR" "${service_code}: Git pull 失败"
        return 1
    fi

    local latest_commit=$(git -C "$project_dir" log --oneline -1)
    log "SUCCESS" "${service_code}: 成功更新到最新版本 (分支: ${current_branch}, 最新提交: ${latest_commit})"
    return 0
}

# ======================
# 服务管理函数
# ======================
check_dependencies() {
    log "INFO" "正在检查依赖项..."
    local missing_deps=()

    for cmd in git supervisorctl python3; do
        if ! command -v "$cmd" >/dev/null; then
            missing_deps+=("$cmd")
        fi
    done

    if [ ${#missing_deps[@]} -gt 0 ]; then
        log "ERROR" "缺少依赖: ${missing_deps[*]}"
        return 1
    fi

    log "SUCCESS" "所有依赖项检查通过"
    return 0
}

deploy_config() {
    local config_source="${PROJECT_ROOTS[mes]}/deploy/${CONFIG_NAME}"

    if [ ! -f "$config_source" ]; then
        log "ERROR" "配置文件不存在: $config_source"
        return 1
    fi

    log "INFO" "正在部署配置文件..."
    if ! sudo cp -v "$config_source" "${SUPERVISOR_DIR}/"; then
        log "ERROR" "配置文件复制失败"
        return 1
    fi

    log "SUCCESS" "配置文件部署成功"
    return 0
}

reload_supervisor() {
    log "INFO" "正在重载 Supervisor..."

    if ! sudo supervisorctl reread; then
        log "ERROR" "Supervisor reread 失败"
        return 1
    fi

    if ! sudo supervisorctl update; then
        log "ERROR" "Supervisor update 失败"
        return 1
    fi

    log "SUCCESS" "Supervisor 重载成功"
    return 0
}

restart_services() {
    local services=("$@")

    for service in "${services[@]}"; do
        log "INFO" "正在重启服务 $service..."

        if ! sudo supervisorctl restart "$service"; then
            log "ERROR" "服务 $service 重启失败"
            return 1
        fi

        # 等待一段时间让服务启动
        sleep 2

        # 检查服务状态
        local status_info=$(sudo supervisorctl status "$service")
        local status=$(echo "$status_info" | awk '{print $2}')

        if [ "$status" == "RUNNING" ]; then
            log "SUCCESS" "服务 $service 重启成功 (状态: $status)"
        else
            log "ERROR" "服务 $service 状态异常: $status_info"
            return 1
        fi
    done

    return 0
}

# ======================
# 使用说明
# ======================
usage() {
    echo -e "${GREEN}使用方法: $0 [选项] [服务端口...]${NC}"
    echo "选项:"
    echo "  -h, --help        显示帮助信息"
    echo "  -g, --git         重启前更新 Git 仓库"
    echo "  -l, --list        显示可用的服务端口"
    echo "服务端口:"
    for port in "${!SERVICES[@]}"; do
        echo "  $port              ${SERVICES[$port]}"
    done
    echo ""
    echo "示例:"
    echo "  $0 8000 8100       # 重启指定端口服务"
    echo "  $0 -g 8000 8100    # 更新代码并重启指定端口服务"
    echo "  $0                 # 重启所有服务"
    exit 0
}

list_services() {
    echo -e "${GREEN}可用的服务端口:${NC}"
    for port in "${!SERVICES[@]}"; do
        echo "  $port -> ${SERVICES[$port]}"
    done
    exit 0
}

# ======================
# 主流程
# ======================
main() {
    # 解析参数
    local RESTART_SERVICES=()
    local UPDATE_GIT=false

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage
                ;;
            -g|--git)
                UPDATE_GIT=true
                shift
                ;;
            -l|--list)
                list_services
                ;;
            *)
                if [[ -v SERVICES["$1"] ]]; then
                    RESTART_SERVICES+=("$1")
                else
                    log "ERROR" "未知的服务端口: $1"
                    usage
                    exit 1
                fi
                shift
                ;;
        esac
    done

    log "INFO" "========== 开始部署 =========="

    # 检查依赖项
    check_dependencies || exit 1

    # 如果需要更新 Git
    if [ "$UPDATE_GIT" = true ]; then
        log "INFO" "正在更新 Git 仓库..."
        if [ ${#RESTART_SERVICES[@]} -eq 0 ]; then
            # 更新所有服务
            for service_code in "${!PROJECT_ROOTS[@]}"; do
                git_update "${PROJECT_ROOTS[$service_code]}" "$service_code" || true
            done
        else
            # 只更新指定服务
            for service_port in "${RESTART_SERVICES[@]}"; do
                git_update "${PROJECT_ROOTS[mes]}" "$service_port" || true
            done
        fi
    fi

    # 部署配置文件
    deploy_config || exit 1

    # 重载 Supervisor
    reload_supervisor || exit 1

    # 确定要重启的服务
    local SERVICES_TO_RESTART=()
    if [[ ${#RESTART_SERVICES[@]} -eq 0 ]]; then
        log "INFO" "未指定服务端口，将重启所有服务"
        for service in "${SERVICES[@]}"; do
            SERVICES_TO_RESTART+=("$service")
        done
    else
        for service_port in "${RESTART_SERVICES[@]}"; do
            SERVICES_TO_RESTART+=("${SERVICES[$service_port]}")
        done
    fi

    # 重启服务
    restart_services "${SERVICES_TO_RESTART[@]}" || exit 1

    # 最终状态验证
    log "INFO" "========== 最终服务状态 =========="
    for service in "${SERVICES_TO_RESTART[@]}"; do
        local status_info=$(sudo supervisorctl status "$service")
        local status=$(echo "$status_info" | awk '{print $2}')
        local port="${SERVICE_PORTS[$service]}"

        if [ "$status" == "RUNNING" ]; then
            log "SUCCESS" "端口 ${port}: $status_info"
        else
            log "ERROR" "端口 ${port}: $status_info"
        fi
    done

    log "SUCCESS" "========== 部署完成 =========="
    log "INFO" "详细日志已保存至: $LOG_FILE"
}

# 异常处理
trap 'log "ERROR" "脚本被用户中断"; exit 1' INT
trap 'log "ERROR" "脚本执行失败: $?"' ERR

# 执行主函数
main "$@"