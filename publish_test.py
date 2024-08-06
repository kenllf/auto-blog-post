import os.path
import selenium
import traceback

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from models.publish_data import PublishData
from publisher.alicloud_publisher import alicloud_publisher
from publisher.cnblogs_publisher import cnblogs_publisher
from publisher.csdn_publisher import csdn_publisher
from publisher.cto51_publisher import cto51_publisher
from publisher.infoq_publisher import infoq_publisher
from publisher.oschina_publisher import oschina_publisher
from publisher.segmentfault_publisher import segmentfault_publisher
from publisher.toutiao_publisher import toutiao_publisher
from publisher.txcloud_publisher import txcloud_publisher
from publisher.zhihu_publisher import zhihu_publisher
from publisher.jianshu_publisher import jianshu_publisher
from publisher.juejin_publisher import juejin_publisher
from publisher.mpweixin_publisher import mpweixin_publisher
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from starlette.requests import Request
from utils.file_utils import write_to_file
from utils.yaml_file_utils import read_common


# 全局变量
driver = None


common_config = read_common()
driver_type = common_config["driver_type"]
content_dir = common_config["content_dir"]

last_published_file_name = "last_published.txt"

all_sites = [
    "csdn",
    "jianshu",
    "juejin",
    "segmentfault",
    "oschina",
    "cnblogs",
    "zhihu",
    "cto51",
    "infoq",
    "txcloud",
    "alicloud",
    "toutiao",
    "mpweixin",
]


def is_driver_alive(driver):
    try:
        # 尝试访问当前窗口，如果失败则说明 driver 已经失效
        driver.current_window_handle
        return True
    except (NoSuchWindowException, WebDriverException):
        return False


def ensure_driver():
    global driver
    if driver is None or not is_driver_alive(driver):
        # 关闭现有的 driver（如果存在）
        if driver is not None:
            try:
                driver.quit()
            except:
                pass

        # 初始化 driver
        if driver_type == "chrome":
            # 启动浏览器驱动服务
            service = selenium.webdriver.chrome.service.Service(
                common_config["service_location"]
            )
            # Chrome 的调试地址
            debugger_address = common_config["debugger_address"]
            # 创建Chrome选项，重用现有的浏览器实例
            options = selenium.webdriver.chrome.options.Options()
            options.page_load_strategy = (
                "normal"  # 设置页面加载策略为'normal' 默认值, 等待所有资源下载,
            )
            options.add_experimental_option("debuggerAddress", debugger_address)
            # 使用服务和选项初始化WebDriver
            driver = webdriver.Chrome(service=service, options=options)
        elif driver_type == "firefox":
            # 启动浏览器驱动服务
            service = selenium.webdriver.firefox.service.Service(
                common_config["service_location"],
                service_args=["--marionette-port", "2828", "--connect-existing"],
            )
            # 创建firefox选项，重用现有的浏览器实例
            options = selenium.webdriver.firefox.options.Options()
            options.page_load_strategy = (
                "normal"  # 设置页面加载策略为 'normal' 默认值, 等待所有资源下载,
            )
            driver = webdriver.Firefox(service=service, options=options)

        driver.implicitly_wait(10)  # 设置隐式等待时间为 10 秒

    return driver


def publish_to_platform(publish_data: PublishData):
    """
    发布到指定平台的封装函数
    """
    try:
        platform = publish_data.platform

        driver = ensure_driver()  # 确保 driver 有效
        globals()[platform + "_publisher"](
            driver, publish_data
        )  # 动态调用对应平台的发布函数
    except Exception as e:
        print(platform, "got error")
        traceback.print_exc()  # 打印完整的异常跟踪信息
        print(e)


def publish_to_all_platforms(content=None):
    """
    发布到所有平台的封装函数
    """
    for platform in all_sites:
        if platform in common_config["enable"] and common_config["enable"][platform]:
            publish_to_platform(platform, content)
    # 在需要的时候关闭浏览器，不要关闭浏览器进程
    driver = ensure_driver()
    driver.quit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global driver
    driver = ensure_driver()  # 启动时执行的代码
    yield
    # 关闭时执行的代码
    # driver.quit()  # 关闭驱动程序


app = FastAPI(lifespan=lifespan)  # 初始化 FastAPI 应用程序时直接传递 lifespan 参数


@app.post("/publish")
async def publish(request: Request, publish_data: PublishData):
    if publish_data.platform not in all_sites:
        raise HTTPException(
            status_code=400, detail=f"Invalid platform: {publish_data.platform}"
        )

    try:
        publish_to_platform(publish_data)  # 发布到平台

        return {"status": "success", "message": f"Published to {publish_data.platform}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
