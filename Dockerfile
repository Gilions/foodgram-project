FROM python:3.8.5
WORKDIR /code
COPY foodgram/ .
RUN pip install --upgrade pip && pip install -r requirements.txt && mkdir static media
COPY ./foodgram/entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]