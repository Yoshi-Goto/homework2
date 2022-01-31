from datetime import datetime as dt

import requests

from dbutil import select_count, iud_db, select_data


def main():
    #################################################################
    # APIを利用してhacker_newsのタイトルとURLを取得する
    #################################################################
    id_get_url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    id_lists = requests.get(id_get_url)
    urls_id = id_lists.json()

    for url_id in urls_id:
        # idリストより個々の詳細データを取り出す
        getjsondata = f"https://hacker-news.firebaseio.com/v0/item/{url_id}.json?print=pretty"
        response = requests.get(getjsondata)
        dic = response.json()
        # print(dic)
        # キーの存在を確認する(titleとurlのキーが存在すれば以下を実行する)
        # キーがあればValueは必ずあると勝手に解釈
        if ('title' in dic) and ('url' in dic):
            # print(f"{dic['title']},{dic['url']}")
            # urlを確認し、既にテータベースに登録されていなければ登録する
            if select_count(dic["url"]) == 0:
                # 現在の日付を取得
                tdt = dt.now()
                tstr = tdt.strftime('%Y/%m/%d')
                # タイトルにシングルコーテーションがあるとデータ登録でエラーとなる対策
                # とりあえずシングルコーテーションをチルダに変更
                title = dic['title'].replace("'", "~")
                # 登録用SQL文を作成する（Pythonではこんな書き方しないのか？？？）
                strsql = ""
                strsql += "INSERT INTO hacker_news (title, url, regday) "
                strsql += f"VALUES ('{title}', '{dic['url']}', '{tstr}');"
                # データの登録処理
                iud_db(strsql)
    #################################################################
    # 当日の取得分をテキストファイルで出力する
    #################################################################
    # 現在の日付を取得
    tdt = dt.now()
    # 日付を文字列に変換
    tstr = tdt.strftime('%Y/%m/%d')
    # 検索文字列作成
    strsql = f"SELECT * FROM hacker_news WHERE regday = '{tstr}';"
    # 本日分のデータを検索する
    dbdata = select_data(strsql)
    # データが存在すればテキストファイルに主t力する
    if len(dbdata) > 0:
        # ファイル名に使用できないため"/"を取り去る
        tstr = tstr.replace('/', '')
        # テキストファイルを開いて登録
        with open(file=f"hn_{tstr}.txt", mode="w", encoding="utf-8") as f:
            # 連続して書き込む（理屈上、同じ日にファイルは1個しかできないはず）
            for dd in dbdata:
                f.write(f"{dd[0]},{dd[1]}\n")


if __name__ == '__main__':
    main()
