FROM python:3.11.5
COPY . \text_analyzer_docker
RUN pip install -r requirements.txt

