FROM python:3.5.2-alpine

COPY . /opt/app
WORKDIR /opt/app
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
	&& apk add --no-cache gcc musl-dev &&\
    pip install --no-cache-dir -r requirements.txt

CMD ["python","./app.py"]