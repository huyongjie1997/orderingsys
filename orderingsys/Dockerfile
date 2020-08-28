FROM python:3.7.6

ENV PYTHONNBUFFERED 1

ADD ./requirements.txt /requirements.txt

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

ADD ./ /code/

WORKDIR /code/

RUN chmod +x /code/*.sh 

