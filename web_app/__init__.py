from flask import Flask, request, send_from_directory, jsonify, render_template, send_file
import cv2 as cv
import numpy as np
import os
import pandas as pd
from web_app.vege_measure import VegeMeasureClass
from web_app.controll_data import ControllDataClass

app = Flask(__name__)
vm = VegeMeasureClass()
cd = ControllDataClass()

# configfileの読み込み
app.config.from_object('web_app.config')


# iconの設定
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico', )

@app.route('/upload', methods = ['POST'])
def upload_file():
    FILE_NAME= 'img_file'
    # リクエストから画像ファイルを取得
    if not FILE_NAME in request.files:
        return '画像が選択されていません'
    img_file = request.files[FILE_NAME]
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], img_file.filename)
    img_file.save(file_path)
    img = cv.imread(file_path)

    df = pd.read_csv('web_app/static/config.csv', index_col = 0)
    # config.csvに書かれているマーカーのサイズを取得
    marker_size = df.at['marker_size', 'size']
    # 画像内にあるマーカーの高さ(ピクセル)を取得
    marker_height = vm.get_marker_height(img)
    if marker_height is None:
        return 'マーカーを検出出来ませんでした。もう一度写真を撮影してください'

    vege_size = vm.measure_vege(img, marker_height, marker_size)

    cd.insert_data(img, vege_size)

    return 'アップロード完了 \n 大きさは約{}cmです'.format(round(vege_size, 2))

@app.route('/get_img', methods = ['GET'])
def get_img_file():
    # 画像ファイルのパスを全部取得
    file_path = app.config['UPLOAD_FOLDER']
    files = os.listdir(file_path)
    # resultから始まって, 拡張子がjpg, png, jpegのものだけ表示する
    files = [x for x in files if (x.endswith('.jpg') or x.endswith('.png') or x.endswith('jpeg')) and x.startswith('result')]

    return jsonify(files)

from web_app import view
