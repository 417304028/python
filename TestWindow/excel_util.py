import xlrd

# 打开Excel文件
def ExcelReader(file):
    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_name('Sheet1')  # 根据名称选择
    data = []
    # 遍历读取行数据
    for row in range(worksheet.nrows):
        # 读取每一行的数据
        row_data = worksheet.row_values(row)
        data.append(row_data)
    return data


if __name__ == "__main__":
    excel = ExcelReader("./搜索文件名.xlsx")
    # print(excel)
    for item in excel:
        print(item)
        print('----------')