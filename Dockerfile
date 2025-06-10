FROM sagemath/sagemath:latest

USER root

# 设置国内源加速（可选）
RUN echo "deb http://mirrors.aliyun.com/debian/ bookworm main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list

#FROM sagemath/sagemath:latest

# 安装 nbformat 读取 .ipynb 文件
RUN sage -pip install nbformat
# 创建共享文件夹（容器内路径）用于通信
RUN mkdir -p /app/share

WORKDIR /app

# 拷贝 notebook 原封不动
COPY dprf-new-docker-share.ipynb .

# 创建一个执行脚本（从 .ipynb 中提取第一段 cell 并执行）
COPY run_first_cell.sh .

RUN chmod +x run_first_cell.sh

CMD ["./run_first_cell.sh"]

