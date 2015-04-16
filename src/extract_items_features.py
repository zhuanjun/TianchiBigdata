# coding=utf-8
__author__ = 'jinyu'
# brand
# sold,sold_user{user,count}
# cart,cart_user[]
# fav,fav_user[]
# click,click_user[]

import os
import types

buy_behaviour_type = '4'
cart_behaviour_type = '3'
favorite_behaviour_type = '2'
click_behaviour_type = '1'
delimiter = ','

def extract_items_features(train_file_path):
    # 按商品id排序
    generate_sortedfile_byitem(train_file_path, "sorted_by_item-" + train_file_path)

    train_file = open("sorted_by_item-" + train_file_path)
    items_features_file = open("items_featurers.csv", 'w')

    item_features = {'sold_times': 0.0,     # 销量
                     'cart_times': 0.0,     # 购物车量
                     'favorite_times': 0.0, # 收藏量
                     'click_times': 0.0,    # 点击量
                     'total_user': 0.0,     # 总用户数
                     'total_cart_people': 0.0,     # 总购物车人数
                     'total_buy_people': 0.0,      # 总购买人数
                     'total_favor_people': 0.0,    # 总收藏人数
                     'total_click_people': 0.0,    # 总点击人数
                     'multiple_buy_user': 0.0,    # 多次购买的用户数
                     'once_click_user': 0.0, # 只点击过一次的用户数
                     'careful_user': 0.0,   # 不在初次访问品牌时购买的订单数
                     'sold_user': {},       # 消费用户{user，count}
                     'cart_user': [],       # 购物车用户
                     'favor_user': [],
                     'click_user': {},
                     'user': []
                     }

    pre_item_id = train_file.readline().split(delimiter)[1]  # 获取第一行的item_id
    train_file.seek(0)
    for line in train_file:
        user_id, item_id, behavior_type, user_geohash, item_category, time, date = line.split(delimiter)

        # 如果当前pre_user_id和读取到的user_id不一样则输出当前item_features并置空
        if not item_id == pre_item_id:
            item_features = get_other_basic_item_features(item_features)  # 获取用户其他特征
            items_features_file.write(
                pre_item_id + "," + get_item_features_str(item_features) + "\n")  # 输出当前item_features
            item_features = initial_item_features(item_features)  # 初始化置空item_features

        item_features['user'].append(user_id)
        if behavior_type == buy_behaviour_type:
            if not item_features['click_user'].get(user_id, 0.0) == 0.0:
                item_features['careful_user'] += 1
            item_features['sold_times'] += 1
            item_features['sold_user'][user_id] = item_features['sold_user'].get(user_id, 0) + 1
        elif behavior_type == cart_behaviour_type:
            item_features['cart_times'] += 1
            item_features['cart_user'].append(user_id)
        elif behavior_type == favorite_behaviour_type:
            item_features['favorite_times'] += 1
            item_features['favor_user'].append(user_id)
        elif behavior_type == click_behaviour_type:
            item_features['click_times'] += 1
            item_features['click_user'][user_id] = item_features['click_user'].get(user_id, 0) + 1
        else:
            pass

        pre_item_id = item_id

    item_features = get_other_basic_item_features(item_features)
    print item_features  # 输出最后一个item_features到文件并重新初始化item_features
    items_features_file.write(pre_item_id + "," + get_item_features_str(item_features) + "\n")

    items_features_file.close()
    train_file.close()
    print item_features.keys()

def get_other_basic_item_features(item_features):
    for count in item_features['sold_user'].values():
        if count > 2:
            item_features['multiple_buy_user'] += 1
    for count in item_features['click_user'].values():
        if count == 1:
            item_features['once_click_user'] += 1
    item_features['total_buy_people'] = float(len(set(item_features['sold_user'].keys())))
    item_features['total_cart_people'] = float(len(set(item_features['cart_user'])))
    item_features['total_click_people'] = float(len(set(item_features['click_user'].keys())))
    item_features['total_favor_people'] = float(len(set(item_features['favor_user'])))
    item_features['total_user'] = float(len(set(item_features['user'])))

    item_features['sold_per_cart'] = item_features['sold_times'] / (item_features['cart_times'] + 1)
    item_features['sold_per_favorite'] = item_features['sold_times'] / (item_features['favorite_times'] + 1)
    item_features['sold_per_click'] = item_features['sold_times'] / (item_features['click_times'] + 1)
    item_features['people_buy_per_cart'] = item_features['total_buy_people'] / (item_features['total_cart_people'] + 1)
    item_features['people_buy_per_favorite'] = item_features['total_buy_people'] / (item_features['total_favor_people'] + 1)
    item_features['people_buy_per_click'] = item_features['total_buy_people'] / (item_features['total_click_people'] + 1)

    # 比值特征
    item_features['comeback_rate'] = item_features['multiple_buy_user'] / (item_features['total_buy_people'] + 1)
    item_features['jump_rate'] = item_features['once_click_user'] / (item_features['total_user'] + 1)
    item_features['active_rate'] = item_features['multiple_buy_user'] / (item_features['total_user'] + 1)
    item_features['average_buy'] = item_features['sold_times'] / (item_features['total_user'] + 1)
    item_features['average_cart'] = item_features['cart_times'] / (item_features['total_user'] + 1)
    item_features['average_click'] = item_features['click_times'] / (item_features['total_user'] + 1)
    item_features['average_favor'] = item_features['favorite_times'] / (item_features['total_user'] + 1)

    return item_features


def initial_item_features(item_features):
    item_features['sold_times'] = 0.0
    item_features['cart_times'] = 0.0
    item_features['favorite_times'] = 0.0
    item_features['click_times'] = 0.0
    item_features['total_user'] = 0.0
    item_features['total_cart_people'] = 0.0
    item_features['total_buy_people'] = 0.0
    item_features['total_favor_people'] = 0.0
    item_features['total_click_people'] = 0.0
    item_features['multiple_buy_user'] = 0.0
    item_features['once_click_user'] = 0.0
    item_features['careful_user'] = 0.0
    item_features['cart_user'] = []
    item_features['favor_user'] = []
    item_features['sold_user'] = {}
    item_features['click_user'] = {}
    item_features['user'] = []

    return item_features


def get_item_features_str(item_features):
    item_features_str = ''
    for k, v in item_features.iteritems():
        if type(v) is not types.ListType:
            item_features_str += str(v) + ','
    return item_features_str


def generate_sortedfile_byitem(origin_file_path, filename):
    originfile = open(origin_file_path)

    entrys = originfile.readlines()
    entrys.sort(key=lambda x: x.split(",")[1])
    sortedfile = open(filename, "w")
    for i in entrys:
        sortedfile.write(i)
    sortedfile.close()
    originfile.close()

path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\source'
os.chdir(path)  ## change dir to '~/files'
train_file_path = "test_item.csv"
# generate_sortedfile_byitem(train_file_path, "sorted_by_item-" + train_file_path)
extract_items_features(train_file_path)
