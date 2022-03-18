FROM python:3.9
ENV PYTHONUNBUFFERED 1
EXPOSE 8080
ENV PORT 8080
ENV HOST 0.0.0.0
RUN mkdir /Exeplore
WORKDIR /Exeplore
COPY requirements.txt /Exeplore/
RUN pip install -r requirements.txt
COPY . /Exeplore/
ENTRYPOINT python /ExePlore/manage.py runserver 0.0.0.0:8080