FROM pytorch/pytorch:latest

COPY . .
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 uvicorn python-multipart
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt --timeout=1000
EXPOSE 8000

#RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
