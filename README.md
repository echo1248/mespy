# mespy

    服务端代码仓库

    git clone git@github.com:echo1248/mespy.git --depth=1

    # 关闭端口占用进程
    netstat -ano | findstr ":8000"
    taskkill /PID 7664 /F
    
    # 端口占用
    ss -tulnp | grep -E '8000|9000'

# 拷贝依赖

    windows: lib/opus.dll 拷贝到 C:\Windows\System32 目录下
    linus: sudo apt install libopus-dev  # 核心开发库

# 创建oh my zsh

    sudo apt update && sudo apt install zsh
    chsh -s $(which zsh)
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 创建docker compose

    sudo apt update
    sudo apt install docker-compose-plugin  # 安装 Docker Compose V2（推荐）

# 创建supervisor

    sudo apt update
    sudo apt install -y supervisor

# 创建Miniconda3

    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    chmod +x Miniconda3-latest-Linux-x86_64.sh
    ./Miniconda3-latest-Linux-x86_64.sh

# 创建uv

    curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建依赖

    uv lock | uv sync

# 安装依赖

    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.local/bin/env

    uv sync --frozen

# 启动

    jqd run