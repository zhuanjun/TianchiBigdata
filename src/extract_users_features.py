# coding=utf-8
__author__ = 'jinyu'

import os
import types

days = 29
buy_behaviour_type = '4'
cart_behaviour_type = '3'
favorite_behaviour_type = '2'
click_behaviour_type = '1'
delimiter = ','

def extract_user_features(train_file_path):

    train_file = open(train_file_path)
    users_features_file = open("users_featurers.csv", 'w')

    user_features={'buy_times': 0.0,                 # 购买量
                   'cart_times': 0.0,                # 购物车量
                   'favorite_times': 0.0,            # 收藏量
                   'click_times': 0.0,               # 点击量
                   'buy_brands_list': [],           # 购买过的品牌
                   'cart_brands_list': [],          # 购物车过的品牌
                   'favorite_brands_list': [],      # 收藏过的品牌
                   'click_brands_list': [],         # 点击过的品牌
                   'active_days_list': [],          # 活跃天
                   'buy_days_list': [],             # 购买天
                    }

    pre_user_id = train_file.readline().split(delimiter)[0] # 获取第一行的user_id
    train_file.seek(0)
    for line in train_file:
        user_id, item_id, behavior_type, user_geohash, item_category, time, date = line.split(delimiter)

        # 如果当前pre_user_id和读取到的user_id不一样则输出当前user_features并置空
        if not user_id == pre_user_id:
            user_features = get_other_basic_user_features(user_features)    # 获取用户其他特征
            users_features_file.write(pre_user_id + "," + get_user_features_str(user_features) + "\n")  # 输出当前user_features
            user_features = initial_user_features(user_features)    # 初始化置空user_features

        user_features['active_days_list'].append(time)
        if behavior_type == buy_behaviour_type:
            user_features['buy_times'] += 1
            user_features['buy_brands_list'].append(item_id)
            user_features['buy_days_list'].append(time)
        elif behavior_type == cart_behaviour_type:
            user_features['cart_times'] += 1
            user_features['cart_brands_list'].append(item_id)
        elif behavior_type == favorite_behaviour_type:
            user_features['favorite_times'] += 1
            user_features['favorite_brands_list'].append(item_id)
        elif behavior_type == click_behaviour_type:
            user_features['click_times'] += 1
            user_features['click_brands_list'].append(item_id)
        else:
            pass

        pre_user_id = user_id


    user_features = get_other_basic_user_features(user_features)
    print user_features # 输出最后一个user_features到文件并重新初始化user_features
    users_features_file.write(pre_user_id + "," + get_user_features_str(user_features) + "\n")

    users_features_file.close()
    train_file.close()


def get_other_basic_user_features(user_features):
    user_features['buy_brands_count'] = float(len(set(user_features['buy_brands_list'])))
    user_features['cart_brands_count'] = float(len(set(user_features['cart_brands_list'])))
    user_features['favorite_brands_count'] = float(len(set(user_features['favorite_brands_list'])))
    user_features['click_brands_count'] = float(len(set(user_features['click_brands_list'])))
    user_features['active_days_count'] = float(len(set(user_features['active_days_list'])))
    user_features['buy_days_count'] = float(len(set(user_features['buy_days_list'])))

    # 购买转化率
    user_features['buy_per_cart'] = user_features['buy_times'] / (user_features['cart_times'] + 1)
    user_features['buy_per_favorite'] = user_features['buy_times'] / (user_features['favorite_times'] + 1)
    user_features['buy_per_click'] = user_features['buy_times'] / (user_features['click_times'] + 1)
    user_features['brand_buy_per_cart'] = user_features['buy_brands_count'] / (user_features['cart_brands_count'] + 1)
    user_features['brand_buy_per_favorite'] = user_features['buy_brands_count'] / (user_features['favorite_brands_count'] + 1)
    user_features['brand_buy_per_click'] = user_features['buy_brands_count'] / (user_features['click_brands_count'] + 1)

    #比值特征

    user_features['buy_days_count_per_active_days_count'] = user_features['buy_days_count'] / (user_features['active_days_count'] + 1)
    user_features['buy_times_per_buy_days_count'] = user_features['buy_times'] / (user_features['buy_days_count'] + 1)
    user_features['active_days_count_per_days'] = user_features['active_days_count'] / days

    return user_features


def initial_user_features(user_features):
    user_features['buy_times'] = 0.0
    user_features['cart_times'] = 0.0
    user_features['favorite_times'] = 0.0
    user_features['click_times'] = 0.0
    user_features['buy_brands_list'] = []
    user_features['cart_brands_list'] = []
    user_features['favorite_brands_list'] = []
    user_features['click_brands_list'] = []
    user_features['active_days_list'] = []
    user_features['buy_days_list'] = []
    return user_features


def get_user_features_str(user_features):
    user_features_str = ''
    for k, v in user_features.iteritems():
        if type(v) is not types.ListType:
            user_features_str += str(v) + ','
    return user_features_str



path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+'\\source'
os.chdir(path)  ## change dir to '~/files'
train_file_path = "t_train.csv"
extract_user_features(train_file_path)


