import random
import pyperclip
import sys

from models.publish_data import PublishData
from publisher.common_handler import wait_login
from selenium.webdriver import Keys, ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from utils.file_utils import (
    read_file_with_footer,
    convert_md_to_html,
    convert_content_to_html,
    read_file,
    parse_front_matter,
)
from utils.selenium_utils import get_html_web_content
from utils.sleep_utils import exponential_sleep
from utils.yaml_file_utils import (
    read_jianshu,
    read_common,
    read_segmentfault,
    read_oschina,
    read_zhihu,
    read_51cto,
    read_infoq,
    read_txcloud,
    read_alcloud,
    read_toutiao,
)


def close_ai_assistant(driver):
    # 随机选择位方法
    # if random.choice([True, False]):
    close_button = driver.find_element(By.CSS_SELECTOR, "h1.header svg.close-btn")
    # else:
    #     close_button = driver.find_element(
    #         By.XPATH,
    #         "//h1[contains(@class, 'header')]//svg[contains(@class, 'close-btn')]",
    #     )

    # 模拟鼠标移动
    actions = ActionChains(driver)
    actions.move_to_element(close_button).perform()

    # 随机等待
    exponential_sleep(2)  # 等待2秒

    # 点击
    close_button.click()

    # 随机等待
    exponential_sleep(2)  # 等待2秒


def toutiao_publisher(driver, publish_data: PublishData):
    toutiao_config = read_toutiao()  # 读取头条配置
    common_config = read_common()  # 读取通用配置

    auto_publish = common_config["auto_publish"]  # 是否自动发布

    driver.switch_to.new_window("tab")  # 打开新标签页并切换到新标签页
    driver.get(toutiao_config["site"])  # 浏览器实例现在可以被重用，进行你的自动化操作
    exponential_sleep(2)  # 等待2秒

    wait_login(
        driver,
        By.XPATH,
        '//div[@class="publish-editor-title-inner"]//textarea[contains(@placeholder,"请输入文章标题")]',
    )  # 等待用户登录

    # 标题设置
    title = driver.find_element(
        By.XPATH,
        '//div[@class="publish-editor-title-inner"]//textarea[contains(@placeholder,"请输入文章标题")]',
    )  # 找到文章标题元素
    title.clear()  # 清空标题内容

    title.send_keys(publish_data.title)  # 设置标题内容
    exponential_sleep(2)  # 等待2秒

    close_ai_assistant(driver)  # 关闭 头条创作助手

    # 正文内容设置
    content_file_html = convert_content_to_html(
        publish_data.content, False
    )  # 将文章内容转成 HTML

    get_html_web_content(driver, content_file_html)  # 获取 HTML 内容
    exponential_sleep(2)  # 等待2秒

    driver.switch_to.window(driver.window_handles[-1])  # 切换到新标签页(这一步可能多余)
    exponential_sleep(1)  # 等待1秒

    # 用 tab 定位，然后拷贝
    cmd_ctrl = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL  # 确定命令键
    action_chains = webdriver.ActionChains(
        driver
    )  # 模拟实际的粘贴操作（在某些情况下可能更合适）：
    # action_chains.key_down(Keys.TAB).key_up(Keys.TAB).perform()
    # exponential_sleep(2)  # 等待2秒
    # print(pyperclip.paste())

    content_element = driver.find_element(
        By.XPATH, '//div[@class="publish-editor"]//div[@class="ProseMirror"]'
    )  # 定位到要粘贴的位置
    content_element.click()  # 点击一下
    exponential_sleep(1)  # 等待1秒

    action_chains.key_down(cmd_ctrl).send_keys("v").key_up(
        cmd_ctrl
    ).perform()  # 粘贴正文内容
    exponential_sleep(3)  # 等待3秒

    # # 展示封面
    # # TODO

    # # 摘要
    # summary = common_config["summary"]
    # if summary:
    #     summary_input = driver.find_element(
    #         By.XPATH,
    #         '//div[@class="multi-abstract-cell-content-input"]//textarea[contains(@placeholder,"好的摘要比标题更吸引读者")]',
    #     )
    #     summary_input.send_keys(summary)
    # exponential_sleep(2)  # 等待2秒

    # # 投放广告
    # # TODO

    # # 原创首发
    # 声明首发
    original_button = driver.find_element(
        By.XPATH,
        '//div[contains(@class, "exclusive-checkbox-wraper")]//label[contains(@class, "byte-checkbox")]//input[@type="checkbox"]',
    )
    if not original_button.is_selected():
        original_button.click()
    exponential_sleep(2)  # 等待2秒

    # original_button = driver.find_element(
    #     By.XPATH, '//div[@class="original-tag"]//span[contains(text(),"声明原创")]'
    # )
    # original_button.click()
    # exponential_sleep(2)  # 等待2秒

    # # 合集
    # # TODO

    # # 发布
    # if auto_publish:
    #     publish_button = driver.find_element(
    #         By.XPATH, '//div[contains(@class,"publish-btn-last")]'
    #     )
    #     publish_button.click()
