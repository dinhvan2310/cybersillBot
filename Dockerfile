FROM python:3.12

WORKDIR /app

COPY requirements.txt ./
ENV HTTP_PROXY="http://kslxewcb:2aeup7adbyjv@136.0.207.84:6661"
ENV HTTPS_PROXY="http://kslxewcb:2aeup7adbyjv@136.0.207.84:6661"
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"] 