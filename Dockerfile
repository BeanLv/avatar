FROM python:3.6

WORKDIR /avatar

COPY . .

RUN pip install --no-cache -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]