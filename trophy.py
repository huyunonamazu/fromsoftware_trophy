import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import pandas as pd
import os

def PercentageOfTrophiesObtained(file_path, game_id):

    data = {"date":int(str(datetime.now().date()).replace("-", ""))}

    # スクレイピングしたいPS4ゲームのURLを指定
    url = 'https://psnprofiles.com/trophies/' + game_id

    # Webサイトに対してHTTP GETリクエストを行う
    response = requests.get(url)
    time.sleep(1)

    # HTMLの解析
    soup = BeautifulSoup(response.content, 'html.parser')

    # table = soup.select_one("[class='box no-top-border']")
    table = soup.select_one("[class='zebra']")
    title = table.select("a[class='title']")
    percent = [ item.select_one("[class='separator rarity']") for item in table.select("[class='hover-show']") ]

    for i in range(len(title)):
        print( title[i].text, end=" : " )
        print( percent[i].select_one("[class='typo-top']").text )
        data[title[i].text] = float( percent[i].select_one("[class='typo-top']").text.replace("%", "") )

    # CSVファイルが存在するか確認
    if os.path.exists(file_path):
        # CSVファイルの読み込み
        df = pd.read_csv(file_path)
        # Dictの値をCSVファイルに書き込み
        df = pd.concat([df, pd.DataFrame(data, index=[len(df)])], ignore_index=True)
    else:
        # DictをDataFrameに変換
        df = pd.DataFrame(data, index=[0])

    # CSVファイルの更新
    df.to_csv(file_path, index=False)

if __name__ == '__main__':
    print("aaaaa")    
    PercentageOfTrophiesObtained("./darksouls3.csv", "4477-dark-souls-iii")
    PercentageOfTrophiesObtained("./darksoulsRemastered.csv", "7655-dark-souls-remastered")
    PercentageOfTrophiesObtained("./darksouls2.csv", "3483-dark-souls-ii-scholar-of-the-first-sin")
    PercentageOfTrophiesObtained("./bloodborne.csv", "3431-bloodborne")




