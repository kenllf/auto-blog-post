#!/bin/bash

# 设置虚拟环境名称
VENV_NAME="myenv"

# 检查 Python 是否安装
if ! command -v python &> /dev/null
then
    echo "Python could not be found. Please install it."
    exit 1
fi


# 检查虚拟环境目录是否存在
if [ ! -d "$VENV_NAME" ]; then
    # 创建虚拟环境
    python -m venv $VENV_NAME
fi


# 检查虚拟环境目录是否存在
if [ ! -d "$VENV_NAME" ]; then
    echo "Failed to create virtual environment. Please check your Python installation."
    exit 1
fi

# 根据操作系统选择激活脚本
if [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ] || [ "$(expr substr $(uname -s) 1 4)" == "MSYS" ]; then
    # Windows 环境 (Git Bash)
    source $VENV_NAME/Scripts/activate
else
    # Unix-like 环境
    source $VENV_NAME/bin/activate
fi

# 检查 requirements.txt 文件是否存在
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found. Creating an empty one."
    touch requirements.txt
fi

# 升级 pip
python -m pip install --upgrade pip

# 安装 requirements.txt 中的包
pip install -r requirements.txt

echo "Virtual environment '$VENV_NAME' has been created and activated, and packages have been installed."
echo "To deactivate the virtual environment, type 'deactivate'."