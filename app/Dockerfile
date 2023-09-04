FROM python:3.11

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY main.py /app
COPY templates /app/templates
COPY static/styles /app/static/styles
COPY static/scripts /app/static/scripts
CMD python main.py