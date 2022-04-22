FROM python:3.9.7
WORKDIR /usr/src
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -r requirements.txt
COPY alembic/ ./alembic
COPY app/ ./app/
COPY alembic.ini .
COPY .env .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
