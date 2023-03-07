import pandas as pd
import datetime
# Flaskこれが必要
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
import urllib
from flask import make_response
from matplotlib import dates as mdates
import base64
import cv2 as cv
import os

class ControllDataClass:
    vege_growth_csv_path = 'web_app/static/vege_growth.csv'
    def __init__(self):
        self.vege_growth_df = pd.read_csv(ControllDataClass.vege_growth_csv_path, index_col = 'date')

    # date, sizeの形状でcsvに保存する
    def insert_data(self, img, vege_size):
        nowtime = datetime.datetime.now()
        self.vege_growth_df.loc[nowtime] = [vege_size]
        self.vege_growth_df.to_csv(ControllDataClass.vege_growth_csv_path)
        self.vege_img_save(img, vege_size, nowtime)

    def vege_img_save(self,img, vege_size, nowtime):
        # 検出結果にテキスト情報を書き込む
        cv.putText(img, '{}cm, {}'.format(round(vege_size, 2), nowtime), (10, 150),
                   cv.FONT_HERSHEY_PLAIN, 7,
                   (0, 0, 255), 10, cv.LINE_AA)
        save_img_path = self.calc_file_number('web_app/static/images/result.png')
        cv.imwrite(save_img_path, img)
        #cv.imwrite('web_app/static/images/result2.png', binary)

    # htmlにグラフを描画する
    def plot_data(self):
        self.__init__()
        fig, ax = plt.subplots()
        # datetimeにして読み込む
        date = pd.to_datetime(self.vege_growth_df.index)
        size = self.vege_growth_df['vege_size']
        ax.plot(date, size, label = "vege_size")
        plt.legend()

        # グラフをバイト列に変換してBase64でエンコード
        buffer = BytesIO()
        fig.savefig(buffer, format = "png")
        buffer.seek(0)
        image_data = base64.b64encode(buffer.getvalue()).decode()

        return image_data

    def calc_file_number(self, save_path, digit = 4):
        # 拡張子を取得
        ext_name = os.path.splitext(os.path.basename(save_path))[1]
        # 拡張子なしのファイル名
        save_file_name = os.path.splitext(os.path.basename(save_path))[0]
        # _数字付きは消す
        if self.isint(save_file_name.split("_")[-1]) :
            save_file_name = "_".join(save_file_name.split("_")[:-1])

        # ファイルパスから保存フォルダのパス取得
        save_folder = os.path.dirname(save_path)

        # 保存フォルダにあるファイルをリストで取得
        folder_file = os.listdir(save_folder)
        # 同じファイル名を探す
        same_ext_files = []
        # 今保存されている同じファイル名の中から、最大ナンバーを探す
        max_file_num = -1

        for x in folder_file:
            split_file = os.path.splitext(x)
            if self.isint(split_file[0].split("_")[-1]) :
                saved_file_name = "_".join(split_file[0].split("_")[:-1])
            else:
                saved_file_name = "_".join(split_file[0])
            if split_file[1] == ext_name and saved_file_name == save_file_name:
                same_ext_files.append(split_file[0])
                file_num = split_file[0][-digit+1:]
                if int(file_num) > int(max_file_num):
                    max_file_num = "{:0>{}}".format(file_num, str(digit))

        # 最大ナンバーが0以外なら、+1 して保存するナンバーを決定
        if max_file_num != 0:
            max_file_num = "{:0>{}}".format(int(max_file_num) + 1, str(digit))

        # ナンバリングしたパスと保存ファイル名に変換
        file_path = os.path.join(save_folder + "/" + save_file_name + "_" + max_file_num + ext_name)

        return file_path

    def isint(self, text):
        # 文字列を実際にint関数で変換してみる
        try:
            int(text)
        # 例外が発生＝変換できないのでFalseを返す
        except ValueError:
            return False
        # 変換できたのでTrueを返す
        return True
