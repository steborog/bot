FROM python:3

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONPATH=./:$PYTHONPATH

CMD ["python3", "app.py"]

