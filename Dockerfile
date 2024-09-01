FROM apache/airflow:2.10.0-python3.12

COPY requirements ./requirements

RUN pip install --upgrade pip
RUN pip install -r ./requirements/requirements.txt
