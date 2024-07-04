# 选择基础镜像
FROM alpine:3.13

# 安装基础的软件和依赖
RUN apk add --no-cache \
    ca-certificates \
    g++ \
    make \
    cmake \
    git \
    sudo

# 设置国内镜像源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tencent.com/g' /etc/apk/repositories

# 安装 Python3 和 pip
RUN apk add --update --no-cache python3 py3-pip && rm -rf /var/cache/apk/*

# 设置 pip 配置
RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple && \
    pip config set global.trusted-host mirrors.cloud.tencent.com && \
    pip install --upgrade pip

# 拷贝项目文件到容器中
COPY . /app

# 设置工作目录
WORKDIR /app

# 安装 Python 依赖
RUN pip install --user -r requirements.txt

# 安装 OpenCV（示例）
RUN apk add --no-cache \
    opencv-dev

# 暴露端口
EXPOSE 80

# 启动命令
CMD ["python3", "run.py", "0.0.0.0", "80"]
