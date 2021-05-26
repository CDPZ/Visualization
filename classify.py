# -*- coding: utf-8 -*-
import arcpy
import os
import sys
import re
reload(sys) 
sys.setdefaultencoding('utf-8')

path = "D:/Users/Document/Tencent Files/279871734/FileRecv/实习数据/土地利用数据/全要素v1/全要素v1.shp"

def classify():
    classes = ["None", "文", "教", "体", "卫", "食"]
    re_Lu = re.compile(r'.*\xc2\xb7')
    re_Xy = re.compile(r'.*\xd1\xa7\xd4\xba')
    re_Jxl = re.compile(r'.*\xbd\xcc\xd1\xa7\xc2\xa5')
    re_St = re.compile(r'.*\xca\xb3\xcc\xc3')
    cursor = arcpy.UpdateCursor(path)
    for row in cursor:
        if row.FID < 0:
            continue
        else:
            print (row.CC)
            str1 = '%s' %(row.name.encode('gbk'))
            print (str1)
            str2 = '%s' %(str1)
            if str1 == "" or str1 == " " or re_Lu.findall(str2):
                row.Class = 0
            elif re_Xy.findall(str2) or re_Jxl.findall(str2):
                row.Class = 2
            elif re_St.findall(str2):
                row.Class = 5
            else:
                num = input()
                if num in [0,1,2,3,4,5]:
                    row.Class = num
                    print(row.name + " classified as " + classes[num])
                else:
                    print(row.FID)
            cursor.updateRow(row)


def sum_area():
    cursor = arcpy.UpdateCursor(path)
    area = 0
    for row in cursor:
        area += row.Area 
    return area



if __name__ == '__main__':
    print sum_area()