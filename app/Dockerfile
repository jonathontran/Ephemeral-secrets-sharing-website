FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY main.py /app
COPY templates /app/templates
COPY static/styles /app/static/styles
CMD python main.py