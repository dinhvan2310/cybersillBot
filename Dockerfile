FROM python:3.12

WORKDIR /app

COPY requirements.txt ./
ENV HTTP_PROXY="http://kslxewcb:2aeup7adbyjv@198.23.239.134:6540"
ENV HTTPS_PROXY="http://kslxewcb:2aeup7adbyjv@198.23.239.134:6540"
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"] 