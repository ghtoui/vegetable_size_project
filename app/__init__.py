from flask import Flask
import cv2


app = Flask(__name__)
# configfileの読み込み
app.config.from_object('app.config')

# これは最後に書く
from app import view
