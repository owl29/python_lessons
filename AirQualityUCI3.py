##################
# Air Qualityデータセットのダウンロード
#   https://deepinsider.jp/tutor/introtensorflow/buildrnn
#
import os
from urllib.request import urlretrieve
from urllib.parse import urlparse
from zipfile import ZipFile
import plotly.graph_objs as go

###
# urlからファイルをダウンロード
def download_file(url, output_dir, overwrite=False):
  file_name = os.path.basename(urlparse(url).path)  # URLからファイル名を取得
  destination = os.path.join(output_dir, file_name) # 出力先ファイルパス
  if overwrite or not os.path.exists(destination):
    # 上書き（overwrite）の指定か未ダウンロードの場合のみダウンロード
    os.makedirs(output_dir)         # 出力先ディレクトリの作成
    urlretrieve(url, destination)   # ダウンロード
  return destination

###
#
def get_trace(data, x_label, y_label, i):
  trace = go.Scatter(
    x = data[x_label],
    y = data[y_label],
    name = str(i) + ":" + y_label
    #mode = "markers",  # markerで大きさや色などのstyleを変更できます．
    #marker = dict(size=10, color="rgb(255, 0, 255)")
  )
  return trace

###
# main
def main():
  ###
  # zipファイルをダウンロード
  zip_url='https://archive.ics.uci.edu/ml/machine-learning-databases/00360/AirQualityUCI.zip'
  download_folder='UCI_data/'
  zip_file = download_file(zip_url, download_folder)
  print(zip_file)

  ###
  # ダウンロードしたzipファイルからAirQualityUCI.xlsxファイルを抽出して読み込む
  import pandas as pd
  with ZipFile(zip_file) as z:
    with z.open('AirQualityUCI.xlsx') as f:
      raw2 = pd.read_excel(
        f,
        #最初の2列には日付と時刻のデータなので、parse_datesで日時データとして結合
        parse_dates={'DateTime': ['Date','Time']},
        na_values=[-200.0],     #　-200を欠損値（NA Values）として入力
        convert_float=False     # すべてのデータをfloat値のまま読み込む
      )
  print(raw2.shape)
  #print(type(raw2['DateTime'][0]))

  import plotly
  from plotly import tools

  # jupyterで実行時に有効化する
  #plotly.offline.init_notebook_mode(connected=False)

  labels = raw2.columns.values
  nulldata = raw2.isnull().sum()
  sizedata=len(raw2)
  sub_titles = []
  for col in raw2.columns.values:
    if col != "DateTime":
      goods = sizedata - nulldata[col]
      i = len(sub_titles)+1
      rate = goods/sizedata
      sub_title = '{0:>2}：{1:<20} good-datas= {2:>4} ( {3:.1%})'.format( i, col, goods, rate)
      print(sub_title)
      sub_titles.append(sub_title)

  fig = tools.make_subplots(rows=len(sub_titles), cols=1,subplot_titles=sub_titles)
  i = 1
  for col in raw2.columns.values:
    if col != "DateTime":
      trace = get_trace(raw2, "DateTime", col, i)
      fig.append_trace(trace, i, 1)
      i = i + 1

  fig['layout'].update(height=len(sub_titles)*200, width=1200, title='Air Quality ( 2004 - 2005 )')
  plotly.offline.plot(fig)

###
if __name__ == '__main__':
    main()
