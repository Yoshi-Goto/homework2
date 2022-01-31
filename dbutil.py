import psycopg2


# データベースへの操作を行う
def iud_db(rsql):
    # DBに接続
    conn = psycopg2.connect("postgresql://postgres@localhost:5432/test_db")
    cur = conn.cursor()
    # SQLを実行
    cur.execute(rsql)
    # 実行状態を保存
    conn.commit()
    # コネクションを閉じる
    conn.close()


# データの存在確認用
def select_count(rurl):
    conn = psycopg2.connect("postgresql://postgres@localhost:5432/test_db")
    cur = conn.cursor()
    sql = f"SELECT COUNT(title) AS CNT FROM hacker_news WHERE url = '{rurl}';"
    cur.execute(sql)
    # 理屈上、１レコードしか返さないはずなのでfetconeを使用
    cnt = cur.fetchone()
    conn.commit()
    conn.close()

    return cnt[0]


# データの選択結果を返却する
def select_data(rsql):
    conn = psycopg2.connect("postgresql://postgres@localhost:5432/test_db")
    cur = conn.cursor()
    cur.execute(rsql)
    ret = cur.fetchall()
    conn.commit()
    conn.close()

    return ret
