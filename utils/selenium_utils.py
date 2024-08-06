import os
import sys

from selenium.webdriver import Keys, ActionChains
from utils.sleep_utils import exponential_sleep


def open_all_sites(driver):
    print("")


# 把 html 内容拷贝到剪贴板
def get_html_web_content(driver, html_file: str):
    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window("tab")
    driver.get("file://" + html_file)
    exponential_sleep(1)  # 等待1秒

    # 获取页面的所有内容
    cmd_ctrl = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL

    ActionChains(driver).key_down(cmd_ctrl).send_keys("a").key_up(cmd_ctrl).key_down(
        cmd_ctrl
    ).send_keys("c").key_up(cmd_ctrl).perform()

    driver.close()  # 关闭 WebDriver 会话

    os.remove(html_file)  # 删除 HTML 文件

    print("页面内容已复制到剪贴板。")  # 打印提示信息
