import os

from datetime import datetime

# from clone import LV1_user_function_sampling, LV1_UserDefinedClassifier, LV1_TargetClassifier
from evaluation import LV1_Evaluator
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from my_clone import LV1_user_function_sampling_meshgrid, LV1_UserDefinedClassifier, LV1_TargetClassifier, \
    LV1_user_function_sampling_meshgrid_rectangular, LV1_user_function_sampling, \
    LV1_user_function_sampling_and_predict_meshgrid_rectangular_and_edge, lv1_user_function_sampling_midpoint

RANDAM_SAMPLING = 'LV1_user_function_sampling'
MESHGRID = 'LV1_user_function_sampling_meshgrid'
MESHGRID_RECTANGULAR = 'LV1_user_function_sampling_meshgrid_rectangular'
LV1_USER_FUNCTION_SAMPLING_AND_PREDICT_MESHGRID_RECTANGULAR_AND_EDGE = 'LV1_user_function_sampling_and_predict_meshgrid_rectangular_and_edge'
LV1_USER_FUNCTION_SAMPLING_MIDPOINT = 'lv1_user_function_sampling_midpoint'

def calc_diff_area(start_n, end_n, start_height, end_height):
    rect_area = (end_n - start_n) * start_height
    triangle_area = ((end_n - start_n) * (end_height - start_height)) / 2

    print(rect_area)
    print(triangle_area)

    return rect_area + triangle_area


def calc_area(n_list, acc_list):
    sum_value = 0

    for i in range(len(n_list) - 1):
        sum_value = sum_value + calc_diff_area(start_n=n_list[i],
                                               end_n=n_list[i + 1],
                                               start_height=acc_list[i],
                                               end_height=acc_list[i + 1])

    return sum_value


def get_features(n, method_name):
    if method_name == RANDAM_SAMPLING:
        return LV1_user_function_sampling(n_samples=n)

    if method_name == MESHGRID:
        return LV1_user_function_sampling_meshgrid(n_samples=n)

    if method_name == MESHGRID_RECTANGULAR:
        return LV1_user_function_sampling_meshgrid_rectangular(n_samples=n)


def exe_my_clone(target, img_save_path, missing_img_save_path, n, method_name, grid_n_size, edge_distance):
    # ターゲット認識器への入力として用いる二次元特徴量を用意
    # features = get_features(n, method_name)
    # features = LV1_user_function_sampling_and_predict_meshgrid_rectangular_and_edge(n_samples=n, target=target,
    #                                                                                grid_n_size=grid_n_size,
    #                                                                                edge_distance=edge_distance)
    features = lv1_user_function_sampling_midpoint(n_samples=n, target=target)

    print(features)

    print(features.shape)
    print(features[0])
    #
    print("\n{0} features were sampled.".format(n))

    # ターゲット認識器に用意した入力特徴量を入力し，各々に対応するクラスラベルIDを取得
    labels = target.predict(features)
    print("\nThe sampled features were recognized by the target recognizer.")

    # クローン認識器を学習
    model = LV1_UserDefinedClassifier()
    model.fit(features, labels)
    print("\nA clone recognizer was trained.")

    # 学習したクローン認識器を可視化し，精度を評価
    evaluator = LV1_Evaluator()
    evaluator.visualize(model, img_save_path)
    print('visualized')
    evaluator.visualize_missing(model=model, target=target, filename=missing_img_save_path, features=features)
    print("\nThe clone recognizer was visualized and saved to {0} .".format(img_save_path))
    accuracy = evaluator.calc_accuracy(target, model)
    print("\naccuracy: {0}".format(accuracy))

    return accuracy


def exe_my_clone_all(start, target_path, max_n, increment_value, now_str, method_name, grid_n_size, edge_distance):
    img_save_dir = 'output/' + now_str + '/images/'
    missing_img_save_dir = 'output/' + now_str + '/missing_images/'

    n_list = []
    acc_list = []

    # ターゲット認識器を用意
    target = LV1_TargetClassifier()
    target.load(target_path)  # 第一引数で指定された画像をターゲット認識器としてロード
    print("\nA target recognizer was loaded from {0} .".format(target_path))

    os.makedirs(img_save_dir)
    os.makedirs(missing_img_save_dir)

    n_list.append(0)
    acc_list.append(0.0)

    for n in range(start, max_n, increment_value):
        acc = exe_my_clone(target=target,
                           img_save_path=img_save_dir + 'n' + str(n) + '.png',
                           missing_img_save_path=missing_img_save_dir + 'n' + str(n) + '.png',
                           n=n, method_name=method_name,
                           grid_n_size=grid_n_size,
                           edge_distance=edge_distance
                           )
        n_list.append(n)
        acc_list.append(acc)

    return n_list, acc_list


def save_csv(now_str, n_list, acc_list, log_dict):
    df_dir = 'output/' + now_str + '/csv/'
    os.makedirs(df_dir)

    save_n_accuracy_csv(n_list=n_list, acc_list=acc_list, df_dir=df_dir)
    save_log_csv(log_dict=log_dict, df_dir=df_dir)


def save_n_accuracy_csv(n_list, acc_list, df_dir):
    n_dict = {
        'n': n_list,
        'accuracy': acc_list
    }

    df = pd.DataFrame.from_dict(n_dict)
    print(df)
    df.to_csv(df_dir + "n_accuracy.csv")


def save_log_csv(log_dict, df_dir):
    df = pd.DataFrame.from_dict(log_dict)
    print(df)
    df.to_csv(df_dir + "log.csv")


def save_and_show_graph(now_str, n_list, acc_list, area, method_name):
    graph_dir = 'output/' + now_str + '/graph/'
    os.makedirs(graph_dir)

    left = np.array(n_list)
    height = np.array(acc_list)
    plt.plot(left, height)
    plt.xlabel("n samples")
    plt.ylabel("Accuracy")
    plt.grid(True)
    plt.ylim(0, 1)
    plt.title("area: " + str(area) + "\n" + method_name)
    plt.savefig(graph_dir + 'n_accuracy.png')
    plt.show()


def create_output():
    now_str = datetime.now().strftime('%Y%m%d%H%M%S')
    target_path = 'lv1_targets/classifier_01.png'
    grid_n_size = 20
    edge_distance = 0.2
    method_name = LV1_USER_FUNCTION_SAMPLING_AND_PREDICT_MESHGRID_RECTANGULAR_AND_EDGE
    n_list, acc_list = exe_my_clone_all(start=grid_n_size,
                                        target_path=target_path, now_str=now_str, max_n=grid_n_size+200, increment_value=111,
                                        method_name=method_name,
                                        grid_n_size=grid_n_size,
                                        edge_distance=edge_distance
                                        )

    area = calc_area(n_list, acc_list)
    print('横軸nと縦軸Accuracyの面積: ' + str(area))

    log_dict = {
        'nos_str': [now_str],
        'target_path': [target_path],
        'area': [area],
        'sampling_method_name': [method_name],
        'grid_n_size': [grid_n_size],
        'edge_distance': [edge_distance]
    }

    save_and_show_graph(now_str=now_str, n_list=n_list, acc_list=acc_list, area=area, method_name=method_name)
    save_csv(now_str=now_str, n_list=n_list, acc_list=acc_list, log_dict=log_dict)


if __name__ == '__main__':
    create_output()
