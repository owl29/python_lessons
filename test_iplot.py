import pandas as pd
raw = pd.read_csv("birth.csv")

print(raw)
import plotly
plotly.offline.init_notebook_mode(connected=False)

data = [
    plotly.graph_objs.Bar(x=raw["year"], y=raw["births"], name="Births"),
    plotly.graph_objs.Scatter(x=raw["year"], y=raw["birth rate"], name="Birth Rate", yaxis="y2")
]

layout = plotly.graph_objs.Layout(
    title="Births and Birth Rate in Japan",
    legend={"x":0.8, "y":0.1},
    xaxis={"title":"Year"},
    yaxis={"title":"Births"},
    yaxis2={"title":"Birth Rate", "overlaying":"y", "side":"right"},
)

fig = plotly.graph_objs.Figure(data=data, layout=layout)
#plotly.offline.iplot(fig)
plotly.offline.plot(fig)
print(raw)
