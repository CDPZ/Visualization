# -*- coding: utf-8 -*-
import arcpy
import os
import sys
import re
import matplotlib.pyplot as plt

# font = {
#     'family':'SimHei',
#     'weight':'bold',
#     'size':12
# }
# matplotlib.rc("font", **font)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
reload(sys) 
sys.setdefaultencoding('utf-8')
path___ = u"D:/Users/Document/Tencent Files/279871734/FileRecv/实习数据/separate_buffer_inters/"
path_ = u"D:/Users/Document/Tencent Files/279871734/FileRecv/实习数据/宿舍_split_inters/"
path__ = u"D:/Users/Document/Tencent Files/279871734/FileRecv/实习数据/"
path_pic = u"D:/Users/Document/Tencent Files/279871734/FileRecv/实习数据/STA_PIC/"
Category = ["文", "教", "体", "卫", "食"]
Dep = {u'Information':"信", u'Elder':"老斋舍", u'Pfirsich':"工", u'Duftbluete':"桂", u'Eichel':"梅", u'Ahorn':"枫", u'See':"湖滨"}
legends = ["20", "50", "80", "100", "150", "300", "400", "500"]
color = ["#2c3e50", "#f1c40f", "#8e44ad", "#e67e22", "#1abc9c", "#f39c12", "#3498db", "#c0392b"]




# def index(self, value, start=None, stop=None):
#     L.index(value, [start, [stop]]) -> integer -- return first index of value.

def get_part(Name):
    # part = list()
    # for root, dirs in os.walk(path__ + u'dis/'):
    #     for di in dirs:
    #         part.append([di[di.rfind('/'):-1]])
    #         for files in os.walk(di):
    #             for fil in files:
    #                 (filename, extension) = os.path.splitext(fil)
    #                 if extension == '.shp':
    #                     part[part.index([di[di.rfind('/'):-1)]])].append(filename)
    #                 else:
    #                     continue
    #return part

    if (Name.find(u'工') != -1 and Name.find(u'教职工') != -1) or Name.find(u'梅') != -1:
        return 'Eichel'
    elif (Name.find(u'工') != -1 and Name.find(u'教职工') == -1) or Name.find(u'桃') != -1:
        return 'Pfirsich'
    elif Name.find(u'信息') != -1 or Name.find(u'国软') != -1:
        return 'Information'
    elif Name.find(u'枫') != -1:
        return 'Ahorn'
    elif Name.find(u'桂') != -1:
        return 'Duftbluete'
    elif Name.find(u'湖滨') != -1:
        return 'See'
    elif Name.find(u'老斋舍') != -1:
        return 'Elder'
    else:
        print 'unclassified name!!!!!!!!!!!'

def walk_path(pa):
    Kultur = 0
    Ausbildung = 0
    Leibeserziehung = 0
    Hygiene = 0
    Essen = 0
    statistic = list()
    statistics = list()
    path = None
    if pa == u"dorm_sta_split":
        path = path_
    elif pa == u"dorm_sta_separate":
        path = path___
    else:
        print("wrong mode")
    for root, dirs, files in os.walk(path):
        for f in files:
            (filename, extension) = os.path.splitext(f)
            if extension != u".shp":
                continue
            else:
                name = filename.split("_")[0]
                radius = filename.split("_")[1]
                cursor = arcpy.UpdateCursor(path + f)
                for row in cursor:
                    if row.Class == 0:
                        continue
                    elif row.Class == 1:
                        Kultur += 1
                    elif row.Class == 2:
                        Ausbildung += 1
                    elif row.Class == 3:
                        Leibeserziehung += 1
                    elif row.Class == 4:
                        Hygiene += 1
                    elif row.Class == 5:
                        Essen += 1
                statistic.append([name, u"文", u"教", u"体", u"卫", u"食"])
                statistic.append([radius, str(Kultur), str(Ausbildung), str(Leibeserziehung), str(Hygiene), str(Essen)])
                statistics.append(statistic)

                statistic = []
                Kultur = 0
                Ausbildung = 0
                Leibeserziehung = 0
                Hygiene = 0
                Essen = 0

    # with open(path__ + pa +".csv", "w") as f:
    #     for part in statistics:
    #         for row in part:
    #             for line in row:
    #                 f.write(line)
    #                 f.write(",")
    #             f.write("\n")

    return statistics
# def check_order(sorted_):
#     for row in sorted_:
#         for ele in row[1:]:
#             if ele


def bubble_sort(array):
    for i in range(1, len(array)):
        for j in range(0, len(array)-i):
            if int(array[j]) > int(array[j+1]):
                array[j], array[j+1] = array[j+1], array[j]
    return array



def exist(stor, name):
    count = 0
    for row in stor:
        if name == row[0]:
            return count
        count += 1
    return -1

def insert(s):
    last = None
    count = 0
    s_ = list()
    for ele in list(s):
        if ele in [str(i) for i in range(10)]:
            if last not in [str(i) for i in range(10)]:
                s_.append("\n")
            s_.append(ele)
            last = ele
            count += 1
            continue
        elif count != 0:
            s_.append("\n")
            last = ele
            count += 1
        s_.append(ele)
        last = ele
        count += 1
    return "".join(s_)

def visualization(statistics):
    plt.rcParams['xtick.direction'] = 'in'
    line = list()
    storage = list()
    index = None
    for sta in statistics:
        index = exist(storage, sta[0][0])
        if index != -1:
            storage[index].append(sta[1])
        else:
            storage.append([sta[0][0]])
            index = exist(storage, sta[0][0])
            storage[index].append(sta[1])
    for i in range(5):
        draw = [[row[0], row[1][i+1], row[2][i+1], row[3][i+1], row[4][i+1], row[5][i+1], row[6][i+1], row[7][i+1], row[8][i+1]] for row in storage]
        draw = [([row[0]] + bubble_sort(row[1:])) for row in draw]

        X = [m+1 for m in range(len(draw))]
        X_name = [insert(row[0]) for row in draw]
        for j in range(8):
            temp, = plt.plot(X, [row[j+1] for row in draw], color = color[j])
            #temp, = plt.bar(X, [row[j+1] for row in draw], color = color[j])
            line.append(temp)
        plt.legend(handles=line,
                labels=legends,
                #bbox_to_anchor=(1,1),#图例边界框起始位置
                loc="upper right",#图例的位置
                #ncol=1,#列数
                #mode="None",#当值设置为“expend”时，图例会水平扩展至整个坐标轴区域
                #borderaxespad=0,#坐标轴和图例边界之间的间距
                title="缓冲区半径",#图例标题
                shadow=True,#是否为线框添加阴影
                fancybox=True,#线框圆角处理参数
                fontsize=8
                )
        plt.xticks(range(1, len(X_name)), X_name if u'E\ni\nc\nh\ne\nl' not in X_name else [Dep[name.replace("\n", '')] for name in X_name], rotation = 'horizontal', fontsize = 4 if u'E\ni\nc\nh\ne\nl' not in X_name else 11)
        if len(draw) > 10:
            plt.title(Category[i])
            plt.xlabel('宿舍名')
            plt.ylabel('数量/个')
            plt.savefig(path_pic + str(Category[i]) +'.png', dpi=1000)
        else:
            plt.title(Category[i])
            plt.xlabel('区域')
            plt.ylabel('数量/个')            
            plt.savefig(path_pic + str(Category[i]) +'_.png', dpi=1000)
        #plt.show()
        plt.clf()

def get_split_sta(statistics_):
    storage_ = list()
    average = list()
    for sta in statistics_:
        index = exist(storage_, sta[0][0])
    if index != -1:
        storage_[index].append(sta[1])
    else:
        storage_.append([sta[0][0]])
        index = exist(storage_, sta[0][0])
        storage_[index].append(sta[1])

    return storage_

def get_level(name, storage_):
    for stor in storage_:
        if stor[0] == name:
            return stor
        elif stor == storage_[-1]:
            print "level not matched!"

def set_ylim_by_category(i):
    if i == 1:
        plt.ylim(0, 22)
    elif i == 0:
        plt.ylim(0,5)
    elif i == 2:
        plt.ylim(0,6)
    elif i == 4:
        plt.ylim(0,4)
def visualization_(statistics, statistics_):
    plt.rcParams['xtick.direction'] = 'in'

    line = list()
    storage = list()
    storage_ = list()
    storage_ = get_split_sta(statistics_)


    index = None
    for sta in statistics:
        index = exist(storage, sta[0][0])
        if index != -1:
            storage[index].append(sta[1])
        else:
            storage.append([sta[0][0]])
            index = exist(storage, sta[0][0])
            storage[index].append(sta[1])
    depart = [[] for i in range(7)]

    for stor in storage:
        if get_part(stor[0]) == 'Eichel':
            depart[0].append(stor)
        elif get_part(stor[0]) == 'Ahorn':
            depart[1].append(stor)
        elif get_part(stor[0]) == 'Information':
            depart[2].append(stor)
        elif get_part(stor[0]) == 'Elder':
            depart[3].append(stor)
        elif get_part(stor[0]) == 'Duftbluete':
            depart[4].append(stor)
        elif get_part(stor[0]) == 'See':
            depart[5].append(stor)
        elif get_part(stor[0]) == 'Pfirsich':
            depart[6].append(stor)
        else :
            print "name not found"


    for dep in depart:
        name = get_part(dep[0][0])
        whole_level = get_level(name, storage_)
        
        for i in range(5):
            num = whole_level[0]
            draw = [[row[0], row[1][i+1], row[2][i+1], row[3][i+1], row[4][i+1], row[5][i+1], row[6][i+1], row[7][i+1], row[8][i+1]] for row in dep]
            draw = [([row[0]] + bubble_sort(row[1:])) for row in draw]

            X = [m+1 for m in range(len(draw))]
            X_name = [insert(row[0]) for row in draw]
            for j in range(8):
                #temp, = plt.plot(X, [row[j+1] for row in draw], color = color[j])
                spc_2spc_dep = [int(row[j+1]) for row in draw]
                temp = plt.bar(X, spc_2spc_dep, color = color[j])
                line.append(temp)
                plt.legend(handles=line,
                        labels=legends,
                        #bbox_to_anchor=(1,1),#图例边界框起始位置
                        loc="upper right",#图例的位置
                        #ncol=1,#列数
                        #mode="None",#当值设置为“expend”时，图例会水平扩展至整个坐标轴区域
                        #borderaxespad=0,#坐标轴和图例边界之间的间距
                        title="缓冲区半径",#图例标题
                        shadow=True,#是否为线框添加阴影
                        fancybox=True,#线框圆角处理参数
                        fontsize=8
                        )
                plt.xticks(range(1, len(X_name)), X_name , rotation = 'horizontal')

                set_ylim_by_category(i)

                plt.title(Dep[name] + '_' + Category[i])
                plt.xlabel('宿舍名')
                plt.ylabel('数量/个')
                plt.savefig(path_pic + Dep[name] + '_' + legends[j] + '_' + str(Category[i]) + '.png', dpi=1000)

                plt.clf()
            #plt.show()
            #plt.clf()
if __name__ == '__main__':
    sta = list()
    sta_ = list()
    sta = walk_path(u"dorm_sta_separate")
    sta_ = walk_path(u"dorm_sta_split")
    visualization_(sta, sta_)
    #visualization(sta_)