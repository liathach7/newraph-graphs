FROM python:slim
ENV PYTHONUNBUFFERED=1
RUN mkdir /newton-graphs2
WORKDIR /newton-graphs2
COPY requirements.txt /newton-graphs2/
RUN pip install -r requirements.txt
COPY . /newton-graphs2/
CMD gunicorn --bind 0.0.0.0:5000 -w 3 newton_graphs2:app
