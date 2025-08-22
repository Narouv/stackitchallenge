FROM python:3.10

RUN pip install fastapi[standard] requests

EXPOSE 8000

WORKDIR /src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]