# 选择合适的基础镜像，这里使用 Alpine 3.20
FROM alpine:3.20

# 设置时区为上海
RUN apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone

# 安装 ca-certificates，用于 HTTPS 协议访问
RUN apk add --no-cache ca-certificates

# 设置国内镜像源，提高下载速度
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tencent.com/g' /etc/apk/repositories

# 安装基础依赖包和 Python 相关工具
RUN apk add --no-cache \
    python3 \
    py3-pip \
    g++ \
    cmake \
    make \
    linux-headers \
    musl-dev \
    ffmpeg-dev \
    libjpeg-turbo-dev \
    zlib-dev \
    tesseract-ocr \
    tesseract-ocr-dev \
    leptonica-dev

# 安装 OpenCV，这里使用预编译的包
RUN apk add --no-cache opencv-dev

# 更新 pip 并安装 Python 依赖包
RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple \
    && pip config set global.trusted-host mirrors.cloud.tencent.com \
    && pip install --upgrade pip \
    && pip install --user -r requirements.txt

# 拷贝项目文件到容器的 /app 目录
COPY . /app

# 设置工作目录
WORKDIR /app

# 暴露端口
EXPOSE 80


# 启动命令
CMD ["python3", "run.py", "0.0.0.0", "80"]
