from plotly import tools
import plotly.graph_objs as go

# make trace
trace0 = go.Scatter(
    x = report["いいね"],
    y = report["リツイート"],
    name = "いいね",
    mode = "markers",
    marker = dict(size=10, color="rgb(255, 0, 255)")) # markerで大きさや色などのstyleを変更できます．

trace1 = go.Scatter(
    x = report["エンゲージメント"],
    y = report["リツイート"],
    name = "URLクリック",
    mode = "markers",
    marker = dict(size=10, color="rgb(255, 165, 0)"))


trace3 = go.Scatter(
    x = report["エンゲージメント"],
    y = report["リツイート"],
    name = "URLクリック",
    mode = "markers",
    marker = dict(size=5, color="rgb(155, 165, 0)"))


fig = tools.make_subplots(rows=2, cols=2,subplot_titles=("いいねプロット","エンゲージメントプロット","エンゲージメントプロット","エンゲージテスト"))

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace3, 2, 1)
fig.append_trace(trace3, 2, 2)

fig['layout'].update(height=900, width=1200, title='i <3 annotations and subplots')
plotly.offline.plot(fig)
