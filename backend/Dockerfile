   FROM python:3.9-slim

   RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential \
       && apt-get clean \
       && rm -rf /var/lib/apt/lists/*

   RUN adduser --disabled-password --gecos '' myuser
   USER myuser

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 5000

   CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
