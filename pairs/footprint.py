import time
import random
import os
from pprint import pprint
import json
from datetime import datetime


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import pandas as pd









def search(d, age, prefs, login='1', tall=[1, 999], edu_background=[1], occ_list=[1]):
    
    # 検索条件全てリセット css-83urwp
    d.find_element(By.CLASS_NAME, 'css-83urwp').click()
    time.sleep(0.1)
    
    # 居住地変更開始
    d.find_element(By.CSS_SELECTOR, "ul:nth-child(3) > li:nth-child(1) > .css-a3zx38 span").click()

    # 5 | click | css=.css-y1esha:nth-child(1) .css-130bzx3 | 
    # 日本
    d.find_element(By.CSS_SELECTOR, ".css-y1esha:nth-child(1) .css-130bzx3").click()

    # 7 | click | css=.css-y1esha:nth-child(14) .list-item-label__nmShn | 
    # 都道府県
    for pref in prefs:
        d.find_element(By.CSS_SELECTOR, f".css-y1esha:nth-child({pref+1}) .list-item-label__nmShn").click()

    # 8 | click | css=*[data-test="header-submit-button"] | 
    # 決定
    d.find_element(By.CSS_SELECTOR, "*[data-test=\"header-submit-button\"]").click()

    # 学歴変更開始
    time.sleep(1)
    d.execute_script('window.scrollBy(0, -2000);')
    d.find_element(By.CSS_SELECTOR, "ul:nth-child(3) > li:nth-child(4) > .css-a3zx38").click()
    for edu in edu_background:
        # d.find_element(By.CSS_SELECTOR, f".css-y1esha:nth-child({edu}) .list-item-label__nmShn").click()
        d.find_element(By.XPATH, f'//li[@data-test="list-item-value-{edu}"]').click()
    time.sleep(1)
    d.find_element(By.CSS_SELECTOR, "*[data-test=\"header-submit-button\"]").click()
    time.sleep(1)

    # 職種変更開始
    d.find_element(By.CSS_SELECTOR, "ul:nth-child(3) > li:nth-child(3) > .css-a3zx38 span").click()
    for occ in occ_list:
        d.execute_script('window.scrollBy(0, -3000);')
        for i in range(3):
            try:
                d.find_element(By.XPATH, f'//li[@data-test="list-item-value-{occ}"]').click()
                break
            except Exception as e:
                d.execute_script('window.scrollBy(0, 1000);')
                if i == 2:
                    print('occ:', occ)
                    print(e)

    d.find_element(By.CSS_SELECTOR, "*[data-test=\"header-submit-button\"]").click()

    # 9 | select | css=li:nth-child(2) .css-dbt3au:nth-child(1) .css-1bq0nkw | label=29歳
    # 年齢開始選択
    dropdown = d.find_element(By.CSS_SELECTOR, "li:nth-child(2) .css-dbt3au:nth-child(1) .css-1bq0nkw")
    dropdown = Select(dropdown)
    dropdown.select_by_value(f'{age}')
    # dropdown.find_element(By.XPATH, "//option[. = '29歳']").click()

    # 10 | select | css=li:nth-child(2) .css-dbt3au:nth-child(3) .css-1bq0nkw | label=29歳
    # 年齢終了選択
    dropdown = d.find_element(By.CSS_SELECTOR, "li:nth-child(2) .css-dbt3au:nth-child(3) .css-1bq0nkw")
    dropdown = Select(dropdown)
    dropdown.select_by_value(f'{age}')
    # dropdown.find_element(By.XPATH, "//option[. = '29歳']").click()

    # 身長始点
    # dropdown = d.find_element(By.CSS_SELECTOR, "li:nth-child(5) .css-dbt3au:nth-child(1) .css-1bq0nkw")
    # dropdown = Select(dropdown)
    # dropdown.select_by_value(f'{tall[0]}')
    
    # 身長終点
    # dropdown = d.find_element(By.CSS_SELECTOR, "li:nth-child(5) .css-dbt3au:nth-child(3) .css-1bq0nkw")
    # dropdown = Select(dropdown)
    # dropdown.select_by_value(f'{tall[1]}')

    # 11 | select | css=.css-whh5e5 > .css-dbt3au .css-1bq0nkw | label=24時間以内
    # 最終ログイン選択
    dropdown = d.find_element(By.CSS_SELECTOR, ".css-whh5e5 > .css-dbt3au .css-1bq0nkw")
    dropdown = Select(dropdown)
    dropdown.select_by_value(login) # 24時間以内=2, オンライン=1
    # dropdown.find_element(By.XPATH, "//option[. = '24時間以内']").click()

    # 12 | click | css=li:nth-child(3) .css-1m1c9sj .css-kan3w1 | 
    # 登録日３日以内クリック
    regi_3days_button = d.find_element(By.CSS_SELECTOR, "li:nth-child(3) .css-1m1c9sj .css-kan3w1")
    regi_3days = d.find_element(By.CSS_SELECTOR, "li:nth-child(3) .css-1m1c9sj")
    regi_3days_input = regi_3days.find_element(By.CLASS_NAME, 'css-1qvnfzg')
    status = regi_3days_input.get_attribute('aria-checked')
    # print(status)
    if status == 'true':
        regi_3days_button.click()
    # new_status =  regi_3days_input.get_attribute('aria-checked')
    # print(new_status)

    # 13 | click | css=.button__E0II1 | 
    # この条件で検索
    btn_clicked = False
    buttons = d.find_elements(By.TAG_NAME, 'button')
    for button in buttons:
        if button.text == 'この条件で検索':
            button.click()
            btn_clicked = True
            break
            
    if not btn_clicked:
        d.find_element(By.CSS_SELECTOR, ".button__E0II1").click()



def click_users(d, wait_time=1.5, scroll_count=50):

    for i in range(scroll_count):
        d.execute_script('window.scrollBy(0, 1000);')
        time.sleep(0.2)

    first_user = d.find_element(By.CLASS_NAME, 'css-m80f7u') # css-opde7s / css-m80f7u
    first_user.click()
    time.sleep(3) # 1人目だけ追加で待機
    
    counter = 0
    user_ids = set()

    while True:
        # user の確認
        time.sleep(wait_time) # 読み込み待機
        url = d.current_url
        user_id = url.split('/')[-1]
        if user_id == 'search':
            break
        if user_id not in user_ids:
            user_ids.add(user_id)
            counter += 1
            try:
                check_user(d, user_id)
            except Exception as e:
                print(e)

        # 次のユーザーに進む
        user_arrows = d.find_elements(By.CSS_SELECTOR, ".css-1d94zew > svg")
        if len(user_arrows) >= 1:
            next_user = user_arrows[-1]
            next_user_type = next_user.find_element(By.TAG_NAME, 'title')
            if next_user_type.text == '次のお相手を見る':
                next_user.click()
            else:
                # 最後のユーザーなので終了する
                break
        else:
            # 矢印が表示されないので終了する（検索結果は一人）
            break

    # print(counter)
    return counter



def check_user(d, user_id):

    json_file_name = f'./candidates/{user_id}.json'
    detail = {'user_id': user_id}
    time_now = datetime.now()
    time_now_str = datetime.strftime(time_now, '%Y-%m-%d %H:%M:%S')
    detail['update_at'] = time_now_str

    if os.path.isfile(json_file_name):
        with open(json_file_name, 'r') as f:
            jd = json.load(f)
            detail['datetime'] = jd['datetime']
            if 'footprints' in jd:
                detail['footprints'] = jd['footprints'] + 1
            else:
                detail['footprints'] = 2
    else:
        detail['datetime'] = time_now_str
        detail['footprints'] = 1

    soup = BeautifulSoup(d.page_source, 'html.parser')
    user_elm = soup.find('div', class_='css-uyj4df')
    like_elm = user_elm.find('span', class_='css-1d0vcp5')
    like = like_elm.text.replace('いいね！', '')
    detail['いいね'] = like
    top_icon_div = soup.find('div', class_='css-3c0z1e')
    top_icon_elm = top_icon_div.find('img', class_='css-onf91i')
    detail['top_icon'] = top_icon_elm['src']

    # icon_list = []
    # while True:
    #     right_arrow = soup.find('button', class_='css-1oqslv6')
    #     if right_arrow is None:
    #         break
    #     else:
    #         d.find_element(By.CLASS_NAME, 'css-1oqslv6').click()
    #         time.sleep(0.5)
    #         soup = BeautifulSoup(d.page_source, 'html.parser')
    #         top_icon_div = soup.find('div', class_='css-3c0z1e')
    #         top_icon_elm = top_icon_div.find('img', class_='css-onf91i')
    #         icon_list.append(top_icon_elm['src'])

    # detail['icon_list'] = ' '.join(icon_list)

    side_panel = soup.find('div', class_='css-rxcc9b')
    dl_elms = side_panel.find_all('dl', class_='css-1woihig')
    
    i = 1
    for dl_elm in dl_elms:
        for child in dl_elm.contents:
            if i % 2 == 1:
                k = child.text
            else:
                detail[k] = child.text
            i += 1

    with open(json_file_name, 'w', encoding='utf-8') as f:
        json.dump(detail, f, indent=4, sort_keys=True, ensure_ascii=False)



def exe_pattern(d, age, prefs, last_login, tall=[1, 999], edu_background=1, occ_list=[1], wait_time=1.7):
    d.get('https://pairs.lv/search')
    result = {'age': age, 'pref': prefs}

    # 検索ボタンをクリックし、検索条件設定画面に遷移
    search_button = d.find_element(By.CLASS_NAME, 'css-1imkhuf')
    search_button.click()
    time.sleep(2)

    # 検索条件を設定して検索実行
    search(d, age=age, prefs=prefs, login=f'{last_login}', tall=tall, edu_background=edu_background, occ_list=occ_list)
    time.sleep(2)
    
    # 検索結果なしの場合をチェック
    judge_list = d.page_source.split('お相手が見つかりませんでした')
    if len(judge_list) == 2:
        return False, {}, '検索結果なし', 0

    # 検索結果を取得・表示
    search_result = d.find_element(By.CLASS_NAME, 'css-1x24mcp') 

    # if search_result.text == '10人未満':
    #     return False, {}, search_result.text, 0
    
    search_result.click()

    result['search_result'] = search_result.text
    search_result_number  = int(search_result.text.split('人')[0].replace(',', ''))
    scroll_count = search_result_number // 4 + 1

    # ユーザーに足跡をつける
    click_count = click_users(
        d, wait_time=wait_time, scroll_count=scroll_count
    )

    result['clickcount'] = click_count
    return True, result, result['search_result'], click_count

