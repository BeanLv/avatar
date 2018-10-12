FROM python:3.6

WORKDIR /root/avatar/src

COPY . .

RUN pip install --no-cache -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]