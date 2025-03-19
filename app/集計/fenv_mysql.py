#######################################################################################
#######################################################################################
#   MySQL接続パラーメータファイル取得モジュール           H.Nishide
#   2024.1119 V1.0  env_mysql.pyから接続パラメータを外出しする
#                   パラメータファイル「env_mysql.xml」とセットで使います。
# ######################################################################################
#  Usage: 利用するプログラムで、 import fenv_mysql　を宣言する。
#   getURL(target)  targetはstag(デバッグ環境)かprod(本番)の2択。接続URLを返す関数です。
#######################################################################################
from urllib.parse import quote_plus # MySQL　パスワードに＠があるとき対応 URLエンコード用
import xml.etree.ElementTree as ET
import os
import time


# MySQL DBへのアクセスurlを取得する関数
def getURL(target):
###############################################################################
    url = ""    #初期化
    # 環境ファイルを読み込む
    xmlfilepath: str = 'env_mysql.xml'
    if os.path.exists(xmlfilepath):
        try:
            tree = ET.parse(xmlfilepath)
            # ルートを取得する
            root = tree.getroot()
            # 以降、XMLの処理を続ける
        except ET.ParseError as e:
            print(f'★★★★ Error parsing {xmlfilepath} : {e}')
            time.sleep(10)
            return url
    else:
        print(f'★★★★ Error: File {xmlfilepath} not found.')    
        time.sleep(10)
        return url
    
    print('root.tag=' + root.tag)
    print('root.attrib=' + str(root.attrib))
    # 
    for child in root:
        print('child.tag=' + child.tag)
        print('db.target=' + str(child.attrib['target']))
        print('db.host=' + str(child.attrib['host']))
        print('db.user=' + str(child.attrib['user']))
        print('db.pwd=' + str(child.attrib['password']))
        if target == str(child.attrib['target']):
            host = str(child.attrib['host'])
            user = str(child.attrib['user'])
            password = str(child.attrib['password'])
            # パスワードをURLエンコード p@ssword -> p%40ssword
            password = quote_plus(password)
            db="authtrustuser"
            port="3306"           # ポート
            # 接続先
            url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8'
            # ループ抜ける
            break
        
    
    # 接続先
    if url == "":
        print("#★★★　エラー # ターゲットDBがありませんでした。 #")
        time.sleep(10)
    else:
        print("url="+url)
    
    return url

################################################################################
