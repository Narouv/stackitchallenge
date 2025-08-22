FROM python:3.10 

RUN pip install fastapi[standard] requests

EXPOSE 8000

ENTRYPOINT ["tail", "-f"]