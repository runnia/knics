FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /myshop
COPY . ./
RUN pip install -r requirements.txt
ENTRYPOINT ["sh","./docker-entrypoint.sh"]
#ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]