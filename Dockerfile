# 使用 AWS 官方 Lambda Python 基礎映像
FROM public.ecr.aws/lambda/python:3.10

# 設定工作目錄
WORKDIR /var/task

# 安裝相依套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有程式碼（含main.py, assistant.py等）
COPY . .

# CMD 為 Lambda handler 的入口點
CMD ["main.handler"]