import cv2 as cv
from cv2 import aruco
import numpy as np

class VegeMeasureClass:
    def __init__(self):
        pass
    
    def measure_vege(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        
        # 2値化 下限, 上限
        low = (30,20,0)
        upp = (75, 255, 255)
        binary = cv.inRange(hsv, low, upp)
        
        # 輪郭抽出
        contours, hierarchy = cv.findContours(
            binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )
        # 小さい輪郭は除外する
        max_contour = max(contours, key = lambda x: cv.contourArea(x))
        
        # 矩形を描画
        x, y, w, h = cv.boundingRect(max_contour)
        vege_height = h
        cv.rectangle(img, (x, y), (x + w, y + h), color = (0, 0, 255), thickness = 3)
        cv.imwrite('web_app/static/images/result.png', img)
        cv.imwrite('web_app/static/images/result2.png', binary)
        return vege_height
    
    # markerの作成
    def make_aruco_marker(self):
        # cv.arucoマーカーを生成して、画像として保存する

        # マーカーの保存先
        dir_mark = 'C:/Users/toui/Desktop/vegetable_size_project/web_app/static/aruco/'

        # 生成するマーカー用のパラメータ
        num_mark = 5 
        size_mark = 500 
        
        # マーカー種類を呼び出し
        dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)

        for count in range(num_mark) :
            #countをidとして流用
            id_mark = count 
            img_mark = aruco.drawMarker(dict_aruco, id_mark, size_mark)

            if count < 10 :
                img_name_mark = 'mark_id_0' + str(count) + '.jpg'
            else :
                img_name_mark = 'mark_id_' + str(count) + '.jpg'
            path_mark = os.path.join(dir_mark, img_name_mark)
            cv.imwrite(path_mark, img_mark)
    
    # markerの高さを取得
    def get_marker_height(self, img):
        # arucoの設定
        dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
        parameters = aruco.DetectorParameters_create()
        
        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)
        num_id = 0
        
        # マーカー検出時
        if num_id in np.ravel(ids):
            index = np.where(ids == num_id)[0][0]
            cornerUR = corners[index][0][1]
            cornerDR = corners[index][0][2]
            
            marker_height = cornerUR - cornerDR
            marker_height = np.abs(marker_height)[1]
            return marker_height
            
if __name__ == '__main__':
    vm = VegeMeasureClass()
    img = cv.imread('static/images/vege.png')