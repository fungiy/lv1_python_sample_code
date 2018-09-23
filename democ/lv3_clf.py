import numpy as np

# クローン認識器を表現するクラス
# このサンプルコードでは各クラスラベルごとに単純な 5-nearest neighbor を行うものとする（sklearnを使用）
# 下記と同型の fit メソッドと predict_proba メソッドが必要
from keras import Input
from keras_applications.vgg16 import VGG16
from sklearn import neighbors, svm
from sklearn.neural_network import MLPClassifier
from tqdm import trange


class LV3UserDefinedClassifier:

    def __init__(self, n_labels):
        self.n_labels = n_labels
        self.clfs = []
        for i in trange(0, self.n_labels):
            clf = neighbors.KNeighborsClassifier(n_neighbors=5)
            self.clfs.append(clf)

    def __mold_features(self, features):
        temp = []
        for i in trange(0, len(features)):
            temp.append(features[i][1])
        return np.asarray(temp, dtype=np.float32)

    # クローン認識器の学習
    #   (features, likelihoods): 訓練データ（特徴量と尤度ベクトルのペアの集合）
    def fit(self, features, likelihoods):
        features = self.__mold_features(features)
        labels = np.int32(likelihoods >= 0.5) # 尤度0.5以上のラベルのみがターゲット認識器の認識結果であると解釈する
        for i in range(0, self.n_labels):
            l = labels[:,i]
            self.clfs[i].fit(features, l)

    # 未知の特徴量を認識
    #   features: 認識対象の特徴量の集合
    def predict_proba(self, features):
        features = self.__mold_features(features)
        likelihoods = np.c_[np.zeros(features.shape[0])]
        for i in range(0, self.n_labels):
            p = self.clfs[i].predict_proba(features)
            likelihoods = np.hstack([likelihoods, np.c_[p[:,1]]])
        likelihoods = likelihoods[:, 1:]
        return np.float32(likelihoods)


class LV3UserDefinedClassifierKNN3:

    def __init__(self, n_labels):
        self.n_labels = n_labels
        self.clfs = []
        for i in trange(0, self.n_labels):
            clf = neighbors.KNeighborsClassifier(n_neighbors=3)
            self.clfs.append(clf)

    def __mold_features(self, features):
        temp = []
        for i in trange(0, len(features)):
            temp.append(features[i][1])
        return np.asarray(temp, dtype=np.float32)

    # クローン認識器の学習
    #   (features, likelihoods): 訓練データ（特徴量と尤度ベクトルのペアの集合）
    def fit(self, features, likelihoods):
        features = self.__mold_features(features)
        labels = np.int32(likelihoods >= 0.5) # 尤度0.5以上のラベルのみがターゲット認識器の認識結果であると解釈する
        for i in range(0, self.n_labels):
            l = labels[:,i]
            self.clfs[i].fit(features, l)

    # 未知の特徴量を認識
    #   features: 認識対象の特徴量の集合
    def predict_proba(self, features):
        features = self.__mold_features(features)
        likelihoods = np.c_[np.zeros(features.shape[0])]
        for i in range(0, self.n_labels):
            p = self.clfs[i].predict_proba(features)
            likelihoods = np.hstack([likelihoods, np.c_[p[:,1]]])
        likelihoods = likelihoods[:, 1:]
        return np.float32(likelihoods)


class LV3UserDefinedClassifierMLP1000:

    def __init__(self, n_labels):
        self.n_labels = n_labels
        self.clfs = []
        for i in trange(0, self.n_labels):
            # clf = VGG16(include_top=False, weights='imagenet')
            clf = MLPClassifier(solver="lbfgs", hidden_layer_sizes=1000)
            self.clfs.append(clf)

    def __mold_features(self, features):
        temp = []
        for i in trange(0, len(features)):
            temp.append(features[i][1])
        return np.asarray(temp, dtype=np.float32)

    # クローン認識器の学習
    #   (features, likelihoods): 訓練データ（特徴量と尤度ベクトルのペアの集合）
    def fit(self, features, likelihoods):
        features = self.__mold_features(features)
        labels = np.int32(likelihoods >= 0.5) # 尤度0.5以上のラベルのみがターゲット認識器の認識結果であると解釈する
        for i in range(0, self.n_labels):
            l = labels[:,i]
            self.clfs[i].fit(features, l)

    # 未知の特徴量を認識
    #   features: 認識対象の特徴量の集合
    def predict_proba(self, features):
        features = self.__mold_features(features)
        likelihoods = np.c_[np.zeros(features.shape[0])]
        for i in range(0, self.n_labels):
            p = self.clfs[i].predict_proba(features)
            likelihoods = np.hstack([likelihoods, np.c_[p[:,1]]])
        likelihoods = likelihoods[:, 1:]
        return np.float32(likelihoods)


class LV3UserDefinedClassifierMLP999:

    def __init__(self, n_labels):
        self.n_labels = n_labels
        self.clfs = []
        for i in trange(0, self.n_labels):
            # clf = VGG16(include_top=False, weights='imagenet')
            clf = MLPClassifier(solver="lbfgs", hidden_layer_sizes=1000)
            self.clfs.append(clf)

    def __mold_features(self, features):
        temp = []
        for i in trange(0, len(features)):
            temp.append(features[i][1])
        return np.asarray(temp, dtype=np.float32)

    # クローン認識器の学習
    #   (features, likelihoods): 訓練データ（特徴量と尤度ベクトルのペアの集合）
    def fit(self, features, likelihoods):
        features = self.__mold_features(features)
        labels = np.int32(likelihoods >= 0.5) # 尤度0.5以上のラベルのみがターゲット認識器の認識結果であると解釈する
        for i in range(0, self.n_labels):
            l = labels[:,i]
            self.clfs[i].fit(features, l)

    # 未知の特徴量を認識
    #   features: 認識対象の特徴量の集合
    def predict_proba(self, features):
        features = self.__mold_features(features)
        likelihoods = np.c_[np.zeros(features.shape[0])]
        for i in range(0, self.n_labels):
            p = self.clfs[i].predict_proba(features)
            likelihoods = np.hstack([likelihoods, np.c_[p[:,1]]])
        likelihoods = likelihoods[:, 1:]
        return np.float32(likelihoods)

class LV3UserDefinedClassifierMLP1000:

    def __init__(self, n_labels):
        self.n_labels = n_labels
        self.clfs = []
        for i in trange(0, self.n_labels):
            # clf = VGG16(include_top=False, weights='imagenet')
            clf = MLPClassifier(solver="lbfgs", hidden_layer_sizes=1000)
            self.clfs.append(clf)

    def __mold_features(self, features):
        temp = []
        for i in trange(0, len(features)):
            temp.append(features[i][1])
        return np.asarray(temp, dtype=np.float32)

    # クローン認識器の学習
    #   (features, likelihoods): 訓練データ（特徴量と尤度ベクトルのペアの集合）
    def fit(self, features, likelihoods):
        features = self.__mold_features(features)
        labels = np.int32(likelihoods >= 0.5) # 尤度0.5以上のラベルのみがターゲット認識器の認識結果であると解釈する
        for i in range(0, self.n_labels):
            l = labels[:,i]
            self.clfs[i].fit(features, l)

    # 未知の特徴量を認識
    #   features: 認識対象の特徴量の集合
    def predict_proba(self, features):
        features = self.__mold_features(features)
        likelihoods = np.c_[np.zeros(features.shape[0])]
        for i in range(0, self.n_labels):
            p = self.clfs[i].predict_proba(features)
            likelihoods = np.hstack([likelihoods, np.c_[p[:,1]]])
        likelihoods = likelihoods[:, 1:]
        return np.float32(likelihoods)


class LV3UserDefinedClassifierSVM:

    def __init__(self, n_labels):
        self.n_labels = n_labels
        self.clfs = []
        for i in trange(0, self.n_labels):
            clf = svm.SVC()
            self.clfs.append(clf)

    def __mold_features(self, features):
        temp = []
        for i in trange(0, len(features)):
            temp.append(features[i][1])
        return np.asarray(temp, dtype=np.float32)

    # クローン認識器の学習
    #   (features, likelihoods): 訓練データ（特徴量と尤度ベクトルのペアの集合）
    def fit(self, features, likelihoods):
        features = self.__mold_features(features)
        labels = np.int32(likelihoods >= 0.5) # 尤度0.5以上のラベルのみがターゲット認識器の認識結果であると解釈する
        for i in range(0, self.n_labels):
            l = labels[:,i]
            self.clfs[i].fit(features, l)

    # 未知の特徴量を認識
    #   features: 認識対象の特徴量の集合
    def predict_proba(self, features):
        features = self.__mold_features(features)
        likelihoods = np.c_[np.zeros(features.shape[0])]
        for i in range(0, self.n_labels):
            p = self.clfs[i].predict_proba(features)
            likelihoods = np.hstack([likelihoods, np.c_[p[:,1]]])
        likelihoods = likelihoods[:, 1:]
        return np.float32(likelihoods)