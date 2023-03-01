import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
import urllib
from flask import make_response
import base64

class ControllDataClass:
    vege_growth_csv_path = 'web_app/static/vege_growth.csv'
    def __init__(self):
        self.vege_growth_df = pd.read_csv(ControllDataClass.vege_growth_csv_path, index_col = 'date')
        
    # date, sizeの形状でcsvに保存する
    def insert_data(self, data):
        nowtime = datetime.datetime.now()
        self.vege_growth_df.loc[nowtime] = [data]
        self.vege_growth_df.to_csv(ControllDataClass.vege_growth_csv_path)
    
    # htmlにグラフを描画する
    def plot_data(self):
        fig, ax = plt.subplots()
        date = self.vege_growth_df.index
        size = self.vege_growth_df['vege_size']
        ax.plot(date, size, label = "vege_size")
        plt.legend()
        
        # グラフをバイト列に変換してBase64でエンコード
        buffer = BytesIO()
        fig.savefig(buffer, format = "png")
        buffer.seek(0)
        image_data = base64.b64encode(buffer.getvalue()).decode()
        
        return image_data        
    
if __name__ == '__main__':
    cd = ControllDataClass()
    cd.insert_data(123)