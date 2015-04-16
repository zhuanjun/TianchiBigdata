# coding=utf-8


import os
from datetime import *

delimiter = ','


# 将行为数据中的未知商品过滤
def filter_unknown_item_in_user_data(user_raw_file_path, item_raw_file_path):
    filtered_file_path = "filtered_unknownitem_" + user_raw_file_path

    item_raw_file = open(item_raw_file_path)    # 商品
    user_raw_file = open(user_raw_file_path)    # 用户行文
    filtered_user_file = open(filtered_file_path, 'w')    # 过滤后文件

    item_set = set()
    for item_raw_line in item_raw_file:
        item_id = item_raw_line.split(delimiter)[0]
        item_set.add(item_id)

    for user_raw_line in user_raw_file:
        item_id = user_raw_line.split(delimiter)[1]
        # 如果该商品未在商品集中出现，则丢弃此条行为数据
        if item_id not in item_set:
            continue
        filtered_user_file.write(user_raw_line)

    filtered_user_file.close()
    user_raw_file.close()
    item_raw_file.close()

    print "filter unknown item completed"
    return filtered_file_path


# 分割数据  分割为训练集和测试集
def split_file(raw_file_path, seperate_day, begin_date):
    train_file_path = "train_" + raw_file_path
    validation_file_path = "validation_" + raw_file_path
    all_file_path = "all_" + raw_file_path

    raw_file = open(raw_file_path)
    t_train = open("temp_" + train_file_path, 'w')
    t_validation = open("temp_" + validation_file_path, 'w')
    t_all = open("temp_" + all_file_path, 'w')

    interval_days = (seperate_day-begin_date).days
    raw_file.readline()     # 读出栏位名
    for line in raw_file:
        entry = line.split(",")
        entry_date = date(*parse_date(entry[5]))
        date_delta = (entry_date - begin_date).days

        entry.insert(5, str(date_delta))
        write_data = ",".join(entry[:7])
        if date_delta <= interval_days:
            t_train.write(write_data)
        else:
            t_validation.write(write_data)
        t_all.write(write_data)

    t_all.close()
    t_validation.close()
    t_train.close()
    raw_file.close()

    generate_sortedfile("temp_" + train_file_path, train_file_path)
    print "generate train_file completed"
    generate_sortedfile("temp_" + validation_file_path, validation_file_path)
    print "generate validation_file completed"
    generate_sortedfile("temp_" + all_file_path, all_file_path)
    print "generate all_file completed"


# 解析日期
def parse_date(raw_date):
    # entry_date = raw_date.decode("gbk")
    entry_date = raw_date
    year, month, day = entry_date.split(" ")[0].split("-")
    return int(year), int(month), int(day)


# 文件排序
def generate_sortedfile(origin_file_path, filename):
    originfile = open(origin_file_path)

    entrys = originfile.readlines()
    entrys.sort(key=lambda x: x.split(",")[0])
    sortedfile = open(filename, "w")
    for i in entrys:
        sortedfile.write(i)
    sortedfile.close()
    originfile.close()
    os.remove(origin_file_path)



SEPERATEDAY =date(2014, 12, 16)
BEGINDAY = date(2014, 11, 18)
path=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+'\\source'
os.chdir(path)  ## change dir to '~/files'

user_raw_file_path = "tianchi_mobile_recommend_train_user.csv"
item_raw_file_path = "tianchi_mobile_recommend_train_item.csv"

filtered_file_path = filter_unknown_item_in_user_data(user_raw_file_path, item_raw_file_path)
split_file(filtered_file_path, SEPERATEDAY, BEGINDAY)
