FROM python:3.11-slim

LABEL maintainer="database-course"

WORKDIR /app

# 先装依赖，利用镜像层缓存
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 再拷贝源码
COPY . .

EXPOSE 8080

# 生产可换成 gunicorn：CMD ["gunicorn","-b","0.0.0.0:8080","app:app"]
CMD ["python", "app.py"]
