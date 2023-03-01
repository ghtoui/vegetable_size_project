from flask import Flask, request, send_from_directory
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

@app.route('/upload', methods = ['POST'])
def upload_file():
    # リクエストから画像ファイルを取得
    image_file = request.files['image_file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(file_path)
    print(image_file)
    print(type(image_file))
    img = cv.imread(file_path)

    df = pd.read_csv('web_app/static/config.csv', index_col = 0)
    # config.csvに書かれているマーカーのサイズを取得
    marker_size = df.at['marker_size', 'size']
    # 画像内にあるマーカーの高さ(ピクセル)を取得
    marker_height = vm.get_marker_height(img)
    if marker_height is None:
        return 'マーカーが検出されませんでした'
    image_file
    return 'OK'

    vege_height = vm.measure_vege(img)
    pixel_size = marker_size / marker_height
    vege_size = pixel_size * vege_height
    cd.insert_data(vege_size)
    
    return 'アップロード完了'

# iconの設定
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico', )



from web_app import view