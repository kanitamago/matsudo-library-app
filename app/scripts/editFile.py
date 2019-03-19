"""
保存されたfoliumファイルから必要な部分を抽出し、indexファイルに送る
"""
from bs4 import BeautifulSoup
import os

def get_elements():
    try:
        filename = os.listdir("app/mapfile")[0]
        filepath = "app/mapfile/"+filename

        with open(filepath, encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")
        head = soup.find("head")
        head = str(head).replace("<head>", "").replace("</head>", "")
        div = soup.find("div")
        div = str(div)
        script = soup.find_all("script")[-1]
        script = str(script)

        return (head, div, script)
    except:
        return (None, None, None)
