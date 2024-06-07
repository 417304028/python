"""
Author: 肖朝露
Date: 2024-05-28

Description:
    目录浏览和选择指定目录控件压测
    打开软件---输入目录---选择目录---输入目标目录---选择文件夹
"""

from pywinauto.application import Application
import time

def start_application_and_select_directory(app_path):
    """启动应用程序并选择目录"""
    app = Application().start(app_path)
    main_window = app.window(title="控件测试")
    time.sleep(1)
    return app, main_window

def type_directory_and_select(main_window, directory_path):
    """在预设目录输入框输入路径并点击选择目录按钮"""
    edit_box = main_window.child_window(control_type="System.Windows.Forms.TextBox")
    edit_box.type_keys(directory_path)
    time.sleep(1)
    select_directory_btn = main_window.child_window(title="选择目录")
    select_directory_btn.click()
    time.sleep(1)

def choose_folder_and_verify(app, expected_path):
    """选择文件夹并验证输入的路径是否正确"""
    select_folder_dialog = app.window(title="选择文件夹")
    folder_input = select_folder_dialog.child_window(class_name="Edit")
    folder_input.set_text(expected_path)
    time.sleep(1)
    select_folder_btn = select_folder_dialog.child_window(title="选择文件夹", class_name="Button")
    select_folder_btn.click()
    time.sleep(2)
    main_window = app.window(title="控件测试")
    try:
        assert main_window.exists(), "主窗口不存在"
        actual_text = main_window.child_window(control_type="System.Windows.Forms.TextBox").window_text()
        assert actual_text == expected_path, f"输入的路径不正确，期望：{expected_path}，实际：{actual_text}"
    except AssertionError as ae:
        print(f"断言错误: {ae}")
    except Exception as e:
        print(f"发生未知错误: {e}")

def test_free_control(app_path, test_cycles=5):
    """执行测试循环，test_cycles=测试次数"""
    global app
    for cycle in range(test_cycles):
        print(f"开始第{cycle + 1}次循环...")
        app, main_win = start_application_and_select_directory(app_path)
        type_directory_and_select(main_win, "C:")
        choose_folder_and_verify(app, "C:\\Users")
        print(f"第{cycle + 1}次循环结束\n")
        app.kill()

if __name__ == "__main__":
    # 输入测试文件的目录开始测试
    test_free_control(r"D:\test\TestFreeControl.exe")
