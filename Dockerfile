# 使用官方 Python 3 镜像作为基础镜像
FROM python:3.8

# 设置工作目录
WORKDIR /app

# 安装OpenGL库
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# 将当前目录下的文件复制到容器的工作目录中
COPY . /app

# 安装应用程序依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install genalog


# 暴露应用程序的端口
EXPOSE 8000

# 定义容器启动命令
CMD ["streamlit", "run", "main.py", "--server.port", "8000"]
