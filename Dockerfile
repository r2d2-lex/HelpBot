FROM python:3.9.19-alpine3.19

WORKDIR /help_bot

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN cp /usr/share/zoneinfo/Asia/Yekaterinburg /etc/localtime && \
echo "Asia/Yekaterinburg" >  /etc/timezone && \

COPY ./ .
