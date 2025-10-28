#!/usr/bin/env bash
set -euo pipefail

# ======================
# 配置区（与 supervisor 配置一致）
# ======================
CONFIG_NAME="mes_services.conf"
SUPERVISOR_DIR="/etc/supervisor/conf.d"
BASE_PATH="/opt/mes"

# ======================
# 服务配置（与 supervisor 完全对应）
# ======================
declare -A PROJECT_ROOTS=(
    ["alpha"]="${BASE_PATH}/alpha/mespy"  # 测试环境
    ["prod"]="${BASE_PATH}/prod/mespy"    # 生产环境
)

# 服务映射（服务代码 -> supervisor 服务名）
declare -A SERVICES=(
    ["alpha_web"]="mes_alpha_8000"
    ["alpha_worker"]="mes_alpha_celery_worker"
    ["alpha_beat"]="mes_alpha_celery_beat"
    ["prod_web"]="mes_prod_8100"
    ["prod_worker"]="mes_prod_celery_worker"
    ["prod_beat"]="mes_prod_celery_beat"
)

# 服务显示名称
declare -A SERVICE_DISPLAY_NAMES=(
    ["alpha_web"]="Alpha Web (8000)"
    ["alpha_worker"]="Alpha Celery Worker"
    ["alpha_beat"]="Alpha Celery Beat"
    ["prod_web"]="Prod Web (8100)"
    ["prod_worker"]="Prod Celery Worker"
    ["prod_beat"]="Prod Celery Beat"
)

# 服务分组
declare -A SERVICE_GROUPS=(
    ["alpha"]="alpha_web alpha_worker alpha_beat"
    ["prod"]="prod_web prod_worker prod_beat"
    ["all"]="alpha_web alpha_worker alpha_beat prod_web prod_worker prod_beat"
)

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
CYAN='\033[0;36m'
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
        "DEBUG")
            colored_message="${CYAN}[调试]${NC} $message"
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
    local service_code="$1"
    local display_name="${SERVICE_DISPLAY_NAMES[$service_code]}"

    # 根据服务类型确定项目路径
    local project_dir=""
    if [[ $service_code == alpha_* ]]; then
        project_dir="${PROJECT_ROOTS[alpha]}"
    elif [[ $service_code == prod_* ]]; then
        project_dir="${PROJECT_ROOTS[prod]}"
    else
        log "ERROR" "无法确定服务 $service_code 的项目路径"
        return 1
    fi

    if [ ! -d "${project_dir}/.git" ]; then
        log "WARN" "$display_name: 非 Git 仓库，跳过更新"
        return 0
    fi

    log "INFO" "$display_name: 正在更新 Git 仓库 (${project_dir})"

    # 检查是否有未提交的更改
    if ! git -C "$project_dir" diff --quiet; then
        log "WARN" "$display_name: 存在未提交的更改，尝试暂存"
        git -C "$project_dir" stash
    fi

    # 获取当前分支
    local current_branch=$(git -C "$project_dir" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

    # 获取最新变更
    if ! git -C "$project_dir" fetch --all --quiet; then
        log "ERROR" "$display_name: Git fetch 失败"
        return 1
    fi

    # 拉取最新代码
    if ! git -C "$project_dir" pull origin "$current_branch" --quiet; then
        log "ERROR" "$display_name: Git pull 失败"
        return 1
    fi

    local latest_commit=$(git -C "$project_dir" log --oneline -1 2>/dev/null || echo "unknown")
    log "SUCCESS" "$display_name: 成功更新 (分支: ${current_branch}, 提交: ${latest_commit})"
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
    local config_source="${PROJECT_ROOTS[alpha]}/deploy/${CONFIG_NAME}"

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

    for service_code in "${services[@]}"; do
        local supervisor_service="${SERVICES[$service_code]}"
        local display_name="${SERVICE_DISPLAY_NAMES[$service_code]}"

        if [ -z "$supervisor_service" ]; then
            log "ERROR" "未知的服务代码: $service_code"
            return 1
        fi

        log "INFO" "$display_name: 正在重启服务..."

        if ! sudo supervisorctl restart "$supervisor_service"; then
            log "ERROR" "$display_name: 服务重启失败"
            return 1
        fi

        # 等待一段时间让服务启动
        sleep 3

        # 检查服务状态
        local status_info=$(sudo supervisorctl status "$supervisor_service")
        local status=$(echo "$status_info" | awk '{print $2}')

        if [ "$status" == "RUNNING" ]; then
            log "SUCCESS" "$display_name: 服务重启成功"
        else
            log "ERROR" "$display_name: 服务状态异常 - $status_info"
            return 1
        fi
    done

    return 0
}

# ======================
# 使用说明
# ======================
usage() {
    echo -e "${GREEN}使用方法: $0 [选项] [服务代码...]${NC}"
    echo "选项:"
    echo "  -h, --help      显示帮助信息"
    echo "  -g, --git       重启前更新 Git 仓库"
    echo "  -l, --list      显示可用的服务"
    echo "  -G, --group     按组管理服务"
    echo ""
    echo "服务代码:"
    echo "  单个服务:"
    echo "    alpha_web        Alpha Web 服务 (8000)"
    echo "    alpha_worker     Alpha Celery Worker"
    echo "    alpha_beat       Alpha Celery Beat"
    echo "    prod_web         Prod Web 服务 (8100)"
    echo "    prod_worker      Prod Celery Worker"
    echo "    prod_beat        Prod Celery Beat"
    echo ""
    echo "  服务组:"
    echo "    alpha            Alpha 所有服务"
    echo "    prod             Prod 所有服务"
    echo "    all              所有服务"
    echo ""
    echo "示例:"
    echo "  $0 alpha_web prod_web          # 重启 Alpha 和 Prod 的 Web 服务"
    echo "  $0 -g alpha_web                # 更新代码并重启 Alpha Web 服务"
    echo "  $0 -G alpha                    # 重启 Alpha 所有服务"
    echo "  $0 -g -G prod                  # 更新代码并重启 Prod 所有服务"
    echo "  $0                            # 重启所有服务"
    exit 0
}

list_services() {
    echo -e "${GREEN}可用的服务:${NC}"
    echo ""
    echo -e "${CYAN}单个服务:${NC}"
    for service_code in "${!SERVICES[@]}"; do
        echo -e "  ${service_code} -> ${SERVICE_DISPLAY_NAMES[$service_code]}"
    done
    echo ""
    echo -e "${CYAN}服务组:${NC}"
    for group in "${!SERVICE_GROUPS[@]}"; do
        echo -e "  ${group} -> ${SERVICE_GROUPS[$group]}"
    done
    exit 0
}

expand_service_groups() {
    local services=("$@")
    local expanded_services=()

    for item in "${services[@]}"; do
        if [[ -v SERVICE_GROUPS["$item"] ]]; then
            # 如果是组，展开组内所有服务
            expanded_services+=(${SERVICE_GROUPS[$item]})
        else
            # 如果是单个服务，直接添加
            expanded_services+=("$item")
        fi
    done

    echo "${expanded_services[@]}"
}

# ======================
# 主流程
# ======================
main() {
    # 解析参数
    local RESTART_SERVICES=()
    local UPDATE_GIT=false
    local USE_GROUPS=false

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
            -G|--group)
                USE_GROUPS=true
                shift
                ;;
            *)
                RESTART_SERVICES+=("$1")
                shift
                ;;
        esac
    done

    log "INFO" "========== 开始部署 MES 服务 =========="

    # 检查依赖项
    check_dependencies || exit 1

    # 确定要操作的服务列表
    local SERVICES_TO_MANAGE=()
    if [[ ${#RESTART_SERVICES[@]} -eq 0 ]]; then
        log "INFO" "未指定服务，将操作所有服务"
        SERVICES_TO_MANAGE=(${SERVICE_GROUPS["all"]})
    else
        if [ "$USE_GROUPS" = true ]; then
            # 使用组模式
            SERVICES_TO_MANAGE=($(expand_service_groups "${RESTART_SERVICES[@]}"))
        else
            # 验证单个服务代码
            for service_code in "${RESTART_SERVICES[@]}"; do
                if [[ ! -v SERVICES["$service_code"] ]] && [[ ! -v SERVICE_GROUPS["$service_code"] ]]; then
                    log "ERROR" "未知的服务代码或组: $service_code"
                    usage
                    exit 1
                fi
            done
            SERVICES_TO_MANAGE=($(expand_service_groups "${RESTART_SERVICES[@]}"))
        fi
    fi

    log "INFO" "操作的服务: ${SERVICES_TO_MANAGE[*]}"

    # 如果需要更新 Git
    if [ "$UPDATE_GIT" = true ]; then
        log "INFO" "正在更新 Git 仓库..."
        local git_errors=0

        # 去重处理，避免同一个项目重复更新
        declare -A updated_projects=()

        for service_code in "${SERVICES_TO_MANAGE[@]}"; do
            # 确定项目路径
            local project_key=""
            if [[ $service_code == alpha_* ]]; then
                project_key="alpha"
            elif [[ $service_code == prod_* ]]; then
                project_key="prod"
            else
                continue
            fi

            # 如果这个项目已经更新过，跳过
            if [[ -v updated_projects["$project_key"] ]]; then
                continue
            fi

            # 更新项目
            if ! git_update "$service_code"; then
                ((git_errors++))
            fi
            updated_projects["$project_key"]=1
        done

        if [ $git_errors -gt 0 ]; then
            log "WARN" "Git 更新完成，但有 ${git_errors} 个错误"
        else
            log "SUCCESS" "所有 Git 仓库更新完成"
        fi
    fi

    # 部署配置文件
    deploy_config || exit 1

    # 重载 Supervisor
    reload_supervisor || exit 1

    # 重启服务
    restart_services "${SERVICES_TO_MANAGE[@]}" || exit 1

    # 最终状态验证
    log "INFO" "========== 最终服务状态 =========="
    local all_running=true
    for service_code in "${SERVICES_TO_MANAGE[@]}"; do
        local supervisor_service="${SERVICES[$service_code]}"
        local display_name="${SERVICE_DISPLAY_NAMES[$service_code]}"

        local status_info=$(sudo supervisorctl status "$supervisor_service")
        local status=$(echo "$status_info" | awk '{print $2}')

        if [ "$status" == "RUNNING" ]; then
            log "SUCCESS" "$display_name: $status"
        else
            log "ERROR" "$display_name: $status_info"
            all_running=false
        fi
    done

    if $all_running; then
        log "SUCCESS" "========== 所有服务部署成功 =========="
    else
        log "ERROR" "========== 部署完成，但部分服务异常 =========="
        exit 1
    fi

    log "INFO" "详细日志已保存至: $LOG_FILE"
}

# 异常处理
trap 'log "ERROR" "脚本被用户中断"; exit 1' INT
trap 'log "ERROR" "脚本执行失败"; exit 1' ERR

# 执行主函数
main "$@"