# syntax=docker/dockerfile:1
# Source: https://fastapi.tiangolo.com/deployment/docker/

FROM python:3.11

WORKDIR /backend

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "device-management-system.main:app", "--host", "0.0.0.0", "--port", "8000"]
