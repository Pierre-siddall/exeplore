FROM python:3.9
ENV PYTHONUNBUFFERED 1
EXPOSE 8080
ENV PORT 8080
ENV HOST 0.0.0.0
RUN mkdir /Exeplore
WORKDIR /Exeplore
COPY requirements.txt /Exeplore/
RUN pip install -r requirements.txt
COPY . /Explore/
COPY manage.py /Exeplore/
RUN ls
ENTRYPOINT [ "python" "manage.py"]
CMD [ "runserver", "0.0.0.0:8080" ]