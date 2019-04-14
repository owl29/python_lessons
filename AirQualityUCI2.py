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

def get_trace(data, x_label, y_label):
  trace = go.Scatter(
    x = data[x_label],
    y = data[y_label],
    name = x_label
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
        #最初の2列には日付と時刻のデータなので、parse_datesで日時データとして結合して［DateTime］列にまとめる。
        parse_dates={'DateTime': ['Date','Time']},
        #-200が欠損値（NA Values）として入力されているため、読み込み時にこれを指定する。
        na_values=[-200.0],
        # Falseがされると、すべてのデータがfloat値のまま読み込まれる。
        convert_float=False
      )
  print('-----------------------')
  print(raw2)
  print(type(raw2['DateTime'][0]))

  import plotly
  from plotly import tools

  # jupyterで実行時に有効化する
  #plotly.offline.init_notebook_mode(connected=False)

  # make trace
  report = raw2

  labels = report.columns.values
  sub_titles = []
  for col in report.columns.values:
    if col != "DateTime":
      sub_titles.append(col)

  #labels.shift();
  print(sub_titles)
  print(len(sub_titles))

  for col in report.columns.values:
    if col != "DateTime":
      print(col)
      trace = get_trace(report, col, "DateTime")


  trace0 = go.Scatter(
    x = report["DateTime"],
    y = report["CO(GT)"],
    name = "NMHC(GT)",
    #mode = "markers",  # markerで大きさや色などのstyleを変更できます．
    #marker = dict(size=10, color="rgb(255, 0, 255)")
  )

  trace1 = go.Scatter(
    x = report["DateTime"],
    y = report["PT08.S1(CO)"],
    name = "PT08.S1(CO)",
    #mode = "markers",
    #marker = dict(size=10, color="rgb(255, 165, 0)")
  )

  trace2 = go.Scatter(
    x = report["DateTime"],
    y = report["C6H6(GT)"],
    name = "C6H6(GT)",
    #mode = "markers",
    #marker = dict(size=10, color="rgb(255, 165, 0)")
  )

  trace3 = go.Scatter(
    x = report["DateTime"],
    y = report["NMHC(GT)"],
    name = "NMHC(GT)",
    #mode = "markers",
    #marker = dict(size=5, color="rgb(155, 165, 0)")
  )

#  fig = tools.make_subplots(rows=4, cols=1,subplot_titles=("-CO(GT)-",...,"-NMHC(GT)-"))
  sub_titles=["-CO(GT)-","-PT08.S1(CO)-","-C6H6(GT)-","-NMHC(GT)-"]
  fig = tools.make_subplots(rows=4, cols=1,subplot_titles=sub_titles)
  fig.append_trace(trace0, 1, 1)
  fig.append_trace(trace1, 2, 1)
  fig.append_trace(trace2, 3, 1)
  fig.append_trace(trace3, 4, 1)
  fig['layout'].update(height=900, width=1400, title='Air Qualityi 2004 - 2005')

  plotly.offline.plot(fig)

###
if __name__ == '__main__':
    main()
