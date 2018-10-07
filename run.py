from application import app
from config import config

app.run(**config['runwith'])
