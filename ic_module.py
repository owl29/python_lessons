import glob
import numpy as np
from keras.preprocessing.image import load_img, img_to_array, array_to_img
from keras.preprocessing.image import random_rotation, random_shift, random_zoom
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras.layers.core import Flatten
from keras.models import Sequential
from keras.models import model_from_json
from keras.callbacks import LearningRateScheduler
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.utils import np_utils

# 共通パラメータ
FileNames = ["img1.npy", "img2.npy", "img3.npy"]
ClassNames = ["うさぎ", "いぬ", "ねこ"]
hw = {"height":16, "width":16}        # リストではなく辞書型 中かっこで囲む
print(FileNames, ClassNames,hw)

# 前処理
def PreProcess(dirname, filename, var_amount=3):
    #定義
    num = 0
    arrlist = []
    #ファイル読み込み
    files = glob.glob(dirname + "/*.jpeg")
    print(files)
    # 画像処理
    for imgfile in files:
        img = load_img(imgfile, target_size=(hw["height"], hw["width"]))    # 画像ファイルの読み込み
        array = img_to_array(img) / 255                                     # 画像ファイルのnumpy化
        arrlist.append(array)                 # numpy型データをリストに追加
        for i in range(var_amount-1):
            arr2 = array
            arr2 = random_rotation(arr2, rg=360)
            arrlist.append(arr2)              # numpy型データをリストに追加
        num += 1
        nplist = np.array(arrlist)
    # 保存
    np.save(filename, nplist)
    print(">> " + dirname + "から" + str(num) + "個のファイル読み込み成功")

#モデルの構築
def BuildCNN(ipshape=(32, 32, 3), num_classes=3):
    # 定義
    model = Sequential()

    # 層1
    # 画像データに対し、3×3のフィルターによる畳み込み処理を24回行います。
    # この畳み込み処理を24回行います。このことを「レイヤーが24枚」と言ったりします。
    # padding='same' は画像の周りを0で埋めるという意味です。1枚目の画像が白地に「0」で
    # 囲まれているのはこれを意味していて、畳み込み処理を行った時にデータの縦横のサイズを変
    # 化させないという特徴があります。
    # Activation('relu') で活性化関数にrelu関数を指定
    model.add(Conv2D(24, 3, padding='same', input_shape=ipshape))
    model.add(Activation('relu'))

    # 層2
    # 画像データに対し、3×3のフィルターによる畳み込み処理を48回行います。
    # MaxPooling2D はpool_size(2×2)の中の最大値を出力するものです。
    # 画像データを2×2の小領域に分割し、その中の最大値を出力します。
    # Dropout(0.5) により入力の50%を0に置き換えます。こうすることで過学習を抑えます。
    model.add(Conv2D(48, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    # 層3、層4
    # 層1、層2と同様です。違いはレイヤーが96枚(畳み込み処理が96回)になっている点です。
    model.add(Conv2D(96, 3, padding='same'))
    model.add(Activation('relu'))

    model.add(Conv2D(96, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    # 層5
    # 今までデータを2次元配列で扱っていましたが、Flatten() と Dense(128) により
    # 要素128個の1次元配列にします。
    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    # 層6
    # 出力の個数を読み込んだフォルダの数(=画像の種類)にします。
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    # 構築
    # 最適化関数を Adam にして、今まで書いた構造を compile により構築します。
    # 損失関数は分類問題でよく用いられる categorical_crossentropy です。
    # 最後に return して、次項で各関数に構築したモデルを渡します。
    adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
    model.compile(loss='categorical_crossentropy',
                  optimizer=adam,
                  metrics=['accuracy'])
    return model

# 学習
# 先ほど実装したモデルと画像データを用いて、実際に学習させます。
def Learning(tsnum=30, nb_epoch=50, batch_size=8, learn_schedule=0.9):
    # データの整理1
    # 学習には入力データとして画像、教師データとして分類番号を使用するので、この2つを関連付けます。
    # 具体的には X_TRAIN_list[n] の分類番号＝ Y_TRAIN_list[n] とします。
    # また学習途中でどのくらい精度が上がっているかを見るために、tsnum 枚(画像回転で水増ししたものを含む)
    # のデータを学習しないように分けておきます。
    # 最後に target += 1 して、画像のnumpyデータごとに分類番号を変えています。
    X_TRAIN_list = []; Y_TRAIN_list = []; X_TEST_list = []; Y_TEST_list = [];
    target = 0
    for filename in FileNames :
        data = np.load(filename)          # 画像のnumpyデータを読み込み
        trnum = data.shape[0] - tsnum
        X_TRAIN_list += [data[i] for i in range(trnum)]          # 画像データ
        Y_TRAIN_list += [target] * trnum                         # 分類番号
        X_TEST_list  += [data[i] for i in range(trnum, trnum+tsnum)]     # 学習しない画像データ
        Y_TEST_list  += [target] * tsnum;                                # 学習しない分類番号
        target += 1
