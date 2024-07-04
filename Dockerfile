# 二开推荐阅读[如何提高项目构建效率](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/scene/build/speed.html)
# 选择基础镜像。如需更换，请到[dockerhub官方仓库](https://hub.docker.com/_/python?tab=tags)自行选择后替换。
# 已知alpine镜像与pytorch有兼容性问题会导致构建失败，如需使用pytorch请务必按需更换基础镜像。
FROM ubuntu:22.04

# 设置国内镜像源以提高下载速度（如果需要）
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

# 设置时区为上海时间（Asia/Shanghai）并安装 HTTPS 证书
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        tzdata \
        ca-certificates \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 更新包列表并安装基本工具、g++、OpenCV依赖和Python
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        g++ \
        libopencv-dev \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 设置pip国内镜像源
RUN pip install --upgrade pip && \
    pip config set global.index-url http://mirrors.aliyun.com/pypi/simple

# 拷贝当前目录下的所有文件到工作目录 /app
COPY . /app

# 设置工作目录
WORKDIR /app

# 安装Python依赖
RUN pip install --user -r requirements.txt

# 暴露端口（如果需要）
EXPOSE 80

# 启动命令（示例）
# CMD ["python3", "run.py", "0.0.0.0", "80"]
