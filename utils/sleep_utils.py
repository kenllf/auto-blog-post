import time
import random


# 设置平均等待时间，默认 2 秒
# 指数级分布，有时会等待更长时间
def exponential_sleep(mean=2):
    sleep_time = random.expovariate(1 / mean)
    time.sleep(sleep_time)
