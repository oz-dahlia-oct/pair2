import time
import random
import sys
from datetime import datetime
import logging


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


from pairs.footprint import *



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler1 = logging.FileHandler(filename='log/main.log')
handler1.setLevel(logging.DEBUG)
handler1.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
logger.addHandler(handler1)

handler2 = logging.StreamHandler()
handler2.setLevel(logging.DEBUG)
handler2.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
logger.addHandler(handler2)




def execute(
    d, last_login=1,
    age_list=list(range(29, 60)),
    prefs_list = [
        [1, 2, 3, 4, 5, 6], # 北海道・東北
        [7, 8, 9, 10, 15, 16, 17, 18], # 北関東, 北陸
        [11, 12, 14], # 千葉・埼玉・神奈川
        [13], # 東京
        [19, 20, 21, 22, 24], # 中部(愛知除く)
        [23], # 愛知
        [25, 26, 28, 29, 30], # 関西(大阪除く)
        [27], # 大阪
        [31, 32, 33, 33, 34, 35, 36, 37, 38, 39], # 中四国
        [40, 41, 42, 43, 44, 45, 46, 47], # 九州・沖縄
    ],
    tall_list = [[1, 999]],
    random_sort=True,
):
    """
    last_login=1: オンライン
    last_login=2: 24時間以内
    """
    results = []

    if random_sort:
        random.shuffle(age_list)
        random.shuffle(prefs_list)

    for age in age_list:
        for prefs in prefs_list:
            for tall in tall_list:  
                try:
                    # 実行開始ア合図
                    logger.debug(f'年齢: {age}, 都道府県: {prefs}, 身長: {tall}, 最終ログイン: {last_login}')
                    success, result, search_result, click_count = exe_pattern(d, age, prefs, last_login, tall, wait_time=2.0)
                    logger.debug(f'検索結果: {search_result}, 足跡付けた数: {click_count}')
                    if success:
                        results.append(result)
                    
                except Exception as e:
                    print(e)
                    time.sleep(120)
                    continue





if __name__ == '__main__':

    # 引数の確認
    last_login = sys.argv[1]
    iteration = int(sys.argv[2])
    sep_tall = sys.argv[3]
    print('last_login:', last_login)
    print('iteration:', iteration)
    print('sep_tall:', sep_tall, '\n')

    # 準備
    d = webdriver.Chrome('./driver/chromedriver')
    d.implicitly_wait(10)
    d.get('https://pairs.lv/search')
    a = input()

    if sep_tall=='sep':
        tall_list = [
            [1, 155],
            [155, 160],
            [160, 165],
            [165, 999]
        ]
    else:
        tall_list = [[1, 999]]

    # 反復実行
    for _ in range(iteration):
        execute(
            d, age_list=list(range(34, 60)),
            last_login=last_login, 
            tall_list=tall_list,
            random_sort=True
        )

