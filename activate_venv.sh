#!/bin/bash

# 设置虚拟环境名称
VENV_NAME="myenv"

# 检查虚拟环境目录是否存在
if [ ! -d "$VENV_NAME" ]; then
    echo "Virtual environment '$VENV_NAME' does not exist. Please run setup script first."
    exit 1
fi

# 激活虚拟环境
source $VENV_NAME/Scripts/activate
# source myenv/Scripts/activate

# 检查是否成功激活
if [ $? -eq 0 ]; then
    echo "Virtual environment '$VENV_NAME' has been activated."
    echo "To deactivate the virtual environment, type 'deactivate'."
else
    echo "Failed to activate virtual environment. Please check your installation."
    exit 1
fi

# 保持shell打开
exec $SHELL
