# segment original data file "t_alibaba_data.csv"
# to training set and test set, using parameter SEPERATEDAY
# original code by oilbeater.
#

import os
from datetime import *

########preprocess rawdate###############

def parse_date(raw_date):
    # entry_date = raw_date.decode("gbk")
    entry_date = raw_date
    year, month, day = entry_date.split(" ")[0].split("-")
    return int(year), int(month), int(day)

# save orignal data to t_all and seprate it to  t_train and t_validation

def split_file(raw_file_path, seperate_day, begin_date):
    interval_days = (seperate_day-begin_date).days

    raw_file = open(raw_file_path)
    t_train=open("t_train_temp.csv",'w')
    t_validation=open("t_validation_temp.csv",'w')
    t_all=open("t_all_temp.csv",'w')
    raw_file.readline()

    for line in raw_file.readlines():
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

    generate_sortedfile("t_train_temp.csv", "t_train.csv")
    generate_sortedfile("t_validation_temp.csv", "t_validation.csv")
    generate_sortedfile("t_all_temp.csv", "t_all.csv")

#sort file accroding to entrys in line
def generate_sortedfile(origin_file_path,filename):
    originfile = open(origin_file_path)

    entrys = originfile.readlines()
    entrys.sort(key=lambda x: x.split(",")[0])
    sortedfile = open(filename, "w")
    for i in entrys:
        sortedfile.write(i)
    sortedfile.close()
    originfile.close()
    os.remove(origin_file_path)


#############data prepocessing ###############

SEPERATEDAY =date(2014, 12, 16)
BEGINDAY = date(2014, 11, 18)
path=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+'\\source'
os.chdir(path)  ## change dir to '~/files'
raw_file_path = "tianchi_mobile_recommend_train_user.csv"
split_file(raw_file_path, SEPERATEDAY, BEGINDAY)
