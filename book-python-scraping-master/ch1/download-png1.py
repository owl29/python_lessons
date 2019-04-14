# ライブラリの取り込み --- (※1)
import urllib.request

# URLと保存パスを指定
#url = "https://uta.pw/shodou/img/28/214.png"
url = "https://qiita.com/kon_yu/items/8ac350f3951f8534c931"
savename = "test.png"

# ダウンロード --- (※2)
urllib.request.urlretrieve(url, savename)
print("保存しました")
