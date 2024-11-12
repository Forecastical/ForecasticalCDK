FROM tiangolo/uvicorn-gunicorn-fastapi:latest

COPY . .

RUN pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
