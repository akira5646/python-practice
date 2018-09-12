import xlrd
import xlsxwriter
import re
import Levenshtein
import sys
import configparser

def readXlsx(path):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0] 
    nrows = table.nrows     
    password_table = {} 
    for curr_row in range(nrows):
        if curr_row != 0:
            row = table.row_values(curr_row)
            #此处加入密码验证函数
            password_table[curr_row] = checkPassword(row)
    return password_table

def writeXlsx(password_table,path):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    # workbook = xlwt.Workbook(encoding='utf8')
    # worksheet = workbook.add_sheet('sheet1')
    title_format = workbook.add_format(
        {'bold': True}
    ) 
    weak_format = workbook.add_format(
        {'bg_color': 'yellow'}
    ) 
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:F', 20)
    #写入标题
    row0 = ['IP','账号','密码','账号密码相似度','问题','验证结果']
    for i in range(0,len(row0)):
        worksheet.write(0,i,row0[i],title_format)
    #写入数据
    for key,value in password_table.items():
        worksheet.write(key,0,value[0])
        worksheet.write(key,1,value[1])
        worksheet.write(key,2,value[2])
        worksheet.write(key,3,value[3])
        worksheet.write(key,4,value[4])
        if(value[5]==False):
            worksheet.write(key,5,'弱口令',weak_format)
        else:
            worksheet.write(key,5,'强口令')
    workbook.close()

def checkPassword(row):
    # 验证密码强度,包含数字，字母，和特殊字符,长度>=8
    pattern = re.compile(r'[-\da-zA-Z`=\\;,./~!@#$%^&*()_+|{}:<>?]*((\d+[a-zA-Z]+[-`=\\;,./~!@#$%^&*()_+|{}:<>?]+)|(\d+[-`=\\;,./~!@#$%^&*()_+|{}:<>?]+[a-zA-Z]+)|([a-zA-Z]+\d+[-`=\\;,./~!@#$%^&*()_+|{}:<>?]+)|([a-zA-Z]+[-`=\\;,./~!@#$%^&*()_+|{}:<>?]+\d+)|([-`=\\;,./~!@#$%^&*()_+|{}:<>?]+\d+[a-zA-Z]+)|([-`=\\;,./~!@#$%^&*()_+|{}:<>?]+[a-zA-Z]+\d+))[-\da-zA-Z`=\\;,./~!@#$%^&*()_+|{}:<>?]*')
    ip, username, password = row
    password = str(password).split(".")[0]
    print("正在处理IP:{0:20}用户名:{1:20}密码:{2:15}".format(ip,username,password))
    result = re.match(pattern,password)
    ratio = Levenshtein.ratio(username, password)
    row.append(str(round(ratio*100,2))+"%")
    if len(password) < 8:
        row.append("密码长度没有大于8位")
        row.append(False)
    elif username in password:
        row.append("密码内包含账号")
        row.append(False)
    elif result == None:
        row.append("密码规格错误")
        row.append(False)
    elif ratio > 0.8:
        row.append("账号密码相似度太高")
        row.append(False)
    else:
        row.append("没有问题")
        row.append(True)
    return row

if __name__ == "__main__":
    config=configparser.ConfigParser()
    config.read('config.ini','utf-8-sig')
    password_table_dir = config['password_check']['password_table_dir']
    output_dir = config['password_check']['output_dir']
    print("password check start")
    password_table = readXlsx(password_table_dir)
    writeXlsx(password_table,output_dir)
    str = input("处理完毕，请按回车键退出")