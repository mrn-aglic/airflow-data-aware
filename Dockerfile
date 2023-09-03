FROM apache/airflow:2.7.0-python3.10

COPY requirements ./requirements

RUN pip install --upgrade pip
RUN pip install -r ./requirements/requirements.txt
