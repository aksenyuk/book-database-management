FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY initialize_database.py .
COPY data/dataset.csv dataset.csv

COPY utils.py .
COPY flask_server.py .
COPY library.html .

COPY run.sh .

RUN chmod +x initialize_database.py
RUN chmod +x flask_server.py
RUN chmod +x run.sh

EXPOSE 8089

CMD ["./run.sh"]