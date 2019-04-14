##################
# https://deepinsider.jp/tutor/introtensorflow/buildrnn
#
#####
# Air Qualityデータセットのダウンロード
#
import os
from urllib.request import urlretrieve
from urllib.parse import urlparse
from zipfile import ZipFile

def download_file(url, output_dir, overwrite=False):
  # URLからファイル名を取得
  parse_result = urlparse(url)
  file_name = os.path.basename(parse_result.path)
  # 出力先ファイルパス
  destination = os.path.join(output_dir, file_name)

  # 無意味なダウンロードを防ぐため、上書き（overwrite）の指定か未ダウンロードの場合のみダウンロードを実施する
  if overwrite or not os.path.exists(destination):
    # 出力先ディレクトリの作成
    os.makedirs(output_dir)
    # ダウンロード
    urlretrieve(url, destination)

  return destination

zip_file = download_file('https://archive.ics.uci.edu/ml/machine-learning-databases/00360/AirQualityUCI.zip', 'UCI_data/')
print(zip_file)

###
# ダウンロードしたzipファイルからAirQualityUCI.xlsxファイルを抽出して読み込む
#
import pandas as pd
with ZipFile(zip_file) as z:
  with z.open('AirQualityUCI.xlsx') as f:
    raw2 = pd.read_excel(
      f,
      #複数column（dateとhour）をまとめて，datetime型のindex（date_hour）として読む場合
      parse_dates={'DateTime': ['Date','Time']}, # 最初の2列には日付と時刻のデータなので、parse_datesで日時データとして結合して［DateTime］列にまとめる。
      na_values=[-200.0],                             #  -200が欠損値（NA Values）として入力されているため、読み込み時にこれを指定する。
      convert_float=False                            #  Falseがされると、すべてのデータがfloat値のまま読み込まれる。
    )
print('show raw2')
print(raw2)

###
# データをグラフに可視化する（１）
# 下記一方を選択
#  pylabはインターフェイスで、本体はmatplotlib
#import pylab as plt
from matplotlib import pyplot as plt

x=raw2['DateTime']
#y=raw2['CO(GT)']
#y=raw2.loc[:,['CO(GT)','NMHC(GT)']]
y=raw2['CO(GT)']

print(x)
print('1------------')

plt.plot(x,y)
print('2------------')
#plt.show()
print('3------------')
# DateTime  CO(GT)  PT08.S1(CO)  NMHC(GT)   C6H6(GT)  ...  PT08.S4(NO2)  PT08.S5(O3)          T         RH        AH


import cufflinks as cf
cf.go_offline()
raw2.iplot(
  # 列ごとにグラフを縦に並べて描画する
  subplots=True,
  shape=(len(raw2.columns), 1),
  # グラフのx軸を共有する
  shared_xaxes=True
)
