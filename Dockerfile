# 使用Alpine Linux 3.13作为基础镜像
FROM alpine:3.13

# 更新包列表并安装基本工具和g++
RUN apk update && \
    apk add --no-cache \
    build-base \
    g++

# 设置国内镜像源（这里假设使用腾讯云的镜像）
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.cloud.tencent.com/g' /etc/apk/repositories

# 安装 Python3 和 pip
RUN apk add --update --no-cache \
    python3 \
    py3-pip \
    && pip3 install --upgrade pip

# 设置 pip 配置为国内镜像
RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple && \
    pip config set global.trusted-host mirrors.cloud.tencent.com

# 拷贝当前目录下的所有文件到工作目录 /app
COPY . /app

# 设置工作目录
WORKDIR /app

# 安装 Python 依赖（如果有 requirements.txt）
RUN pip install --user -r requirements.txt

# 安装 OpenCV
RUN apk add --no-cache \
    opencv-dev

# 暴露端口（如果需要）
EXPOSE 80

# 启动命令（示例）
CMD ["python3", "run.py", "0.0.0.0", "80"]
