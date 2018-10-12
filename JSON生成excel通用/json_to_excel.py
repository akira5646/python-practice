import xlsxwriter

def write_excel(jsonstr):
    workbook = xlsxwriter.Workbook(f"D:\Github\python-practice\json生成excel通用\output.xlsx")
    worksheet = workbook.add_worksheet()
    title_format = workbook.add_format(
        {'bold': True}
    ) 
    #写入标题
    row0 = list(jsonstr[0].keys())
    for i in range(0,len(row0)):
        worksheet.write(0,i,row0[i],title_format)
    #写入数据
    for i in range(1,len(jsonstr)+1):
        for j in range(0,len(row0)):
            worksheet.write(i,j,str(jsonstr[i-1][row0[j]]))
    print("complete")
    workbook.close()

if __name__ == '__main__':
    # 生成10个字典拼成列表
    jsonstr = []
    for i in range(1,11):
        j = {"key1":i,"key2":i*10,"key3":i*100}
        jsonstr.append(j)
    write_excel(jsonstr)