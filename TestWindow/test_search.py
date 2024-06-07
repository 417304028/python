import time
import os
from pywinauto import *
from compare_pic import *
from excel_util import *

# 截图保存路径
current_path = os.path.dirname(__file__)
searched_path = current_path + "\\pic\\"
img1 = searched_path + "BeforeSearch.png"
img2 = searched_path + "temp.png"


# 定义在指定的路径搜索文件方法
def search(path, file):
    window = app.window(class_name="CabinetWClass",control_type='Window')
    window.set_focus()
    address = window.child_window(title="所有位置", control_type="SplitButton")
    address.click_input()
    window.child_window(title='地址', control_type='Edit').type_keys(path).type_keys('{VK_RETURN}')
    window.child_window(auto_id="SearchEditBox", control_type="Edit").type_keys(file)
    # 截图"所有位置"按钮
    address.capture_as_image().save(img1)

    # 对比"所有位置"按钮状态，判断是否搜索完成
    while True:
        time.sleep(3)                
        address.capture_as_image().save(img2)       
        # img1 = r'D:\TestWindow\BeforeSearch.png'
        # img2 = r'D:\TestWindow\temp.png'
        degree = ComparePic().classify_aHash(img1,img2)
        print("文件搜索中...")
        # 两图差异<10,说明搜索结束
        if degree < 10:
            print("----文件搜索结束了！----")
            break 
    # 搜索结束，截图
    window.capture_as_image().save(searched_path + file + '.png')  
    # 搜索列表第1个项目
    result_items = window.child_window(title="项目视图", control_type="List")
    first_item = result_items.children()[0]


    # 创建new.txt并打印其路径
    def create_file():
        result.double_click_input()
        window.child_window(title="主页", control_type="TabItem").click_input()
        window.child_window(title="新建项目", control_type="SplitButton").click_input()
        window.child_window(title="文本文档",control_type="MenuItem").click_input()
        window.type_keys("new{VK_RETURN}")

        # 打印new.txt的路径
        window.child_window(title="new.txt", class_name="UIItem").right_click_input()
        window.type_keys("R")
        pro_window = app.window(title_re=".*属性", class_name="#32770")
        txt_path = pro_window.child_window(title="位置:", class_name="Edit", control_type="Edit").get_value()
        pro_window.close()
        print('new.txt所在目录是：' + txt_path)

    # window窗口视图设置：查看-内容
    # 搜索结果：未找到
    if first_item.window_text() == "没有与搜索条件匹配的项。":
        print('未找到任何与搜索条件匹配的项！')
    # 有搜索结果，窗口有滚动条
    elif  first_item.window_text() == '垂直滚动条':     
        result = result_items.children()[1]
        # 找到的第1个项目是文件夹，在文件夹下创建new.txt
        if not result.children(title="大小"):
            create_file()            
        # 找到的第1个项目是文件,双击打开
        else:
            result.double_click_input()
            # app.kill()
    # 有搜索结果，窗口没有滚动条
    else:
        result = result_items.children()[0]
        # 找到的第1个项目是文件夹，在文件夹下创建new.txt
        if not result.children(title="大小"):
            create_file()
        else:
            # 找到的第1个项目是文件,双击打开
            result.double_click_input()  


if __name__ == "__main__":    
    # 要搜索的文件名、指定的路径
    excel = ExcelReader("./搜索文件名.xlsx")
    # 启动程序打开窗口
    app = Application(backend="uia")
    app.start("explorer")
    app.connect(class_name="CabinetWClass", timeout=5)
    for item in excel:
        search(item[0], item[1])        
    # 关闭
    app.kill()
            
          
