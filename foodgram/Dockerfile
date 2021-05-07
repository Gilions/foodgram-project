FROM python:3.8.5
WORKDIR /code
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt && mkdir static media
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]