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
    air_quality = pd.read_excel(
      f,
      index_col=0, parse_dates={'DateTime': [0, 1]}, # 最初の2列には日付と時刻のデータなので、parse_datesで日時データとして結合して［DateTime］列にまとめる。
      na_values=[-200.0],                             #  -200が欠損値（NA Values）として入力されているため、読み込み時にこれを指定する。
      convert_float=False                            #  Falseがされると、すべてのデータがfloat値のまま読み込まれる。
    )
with ZipFile(zip_file) as z:
  with z.open('AirQualityUCI.xlsx') as f:
    raw = pd.read_excel(
      f,
    #  index_col=0, parse_dates={'DateTime': [0, 1]}, # 最初の2列には日付と時刻のデータなので、parse_datesで日時データとして結合して［DateTime］列にまとめる。
      na_values=[-200.0],                             #  -200が欠損値（NA Values）として入力されているため、読み込み時にこれを指定する。
      convert_float=False                            #  Falseがされると、すべてのデータがfloat値のまま読み込まれる。
    )

###
# データをグラフに可視化する（１）
#
import plotly
#plotly.offline.init_notebook_mode(connected=False)
print(air_quality)

raw['datetime'] = raw['Date'].astype(str) + ' ' + raw['Time'].astype(str)
raw['datetime64']=pd.to_datetime(raw['datetime'])

#print(raw)
print(type(raw['Date'][0]))
print(type(raw['Time'][0]))
print(type(raw['datetime'][0]))
print(type(raw['datetime64'][0]))

with ZipFile(zip_file) as z:
  with z.open('AirQualityUCI.xlsx') as f:
    raw2 = pd.read_excel(
      f,
      #複数column（dateとhour）をまとめて，datetime型のindex（date_hour）として読む場合
    #  df = pd.read_csv('some.csv', parse_dates={'date_hour':['date', 'hour']}, index_col='date_hour')
      parse_dates={'DateTime': ['Date','Time']}, # 最初の2列には日付と時刻のデータなので、parse_datesで日時データとして結合して［DateTime］列にまとめる。
      na_values=[-200.0],                             #  -200が欠損値（NA Values）として入力されているため、読み込み時にこれを指定する。
      convert_float=False                            #  Falseがされると、すべてのデータがfloat値のまま読み込まれる。
    )
print('-----------------------')
print(raw2)
print(type(raw2['DateTime'][0]))
