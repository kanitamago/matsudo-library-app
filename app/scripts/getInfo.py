"""
送信されたキーワードを引数にスクレイピングする
スクレイピングしてきた情報を整形し、データベースに投入しやすい状態にする

松戸市立図書館 -> https://www.library-matsudo.jp/opac/wopc/pc/pages/SearchDetail.jsp
西部図書館 -> https://www.library.pref.chiba.lg.jp/licsxp-iopac/WOpacMnuTopInitAction.do
"""
from app.scripts import libraryData
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import math
from pprint import pprint
from time import sleep

class Library():

    def __init__(self, keyword):
        self.keyword = keyword

    def scraping(self):

        #松戸市立図書館/松戸市立/千葉県立を除いて検索
        library_names = [row["名称"].replace("松戸市立図書館", "").replace("松戸市立", "").replace("千葉県立", "") for row in libraryData.results]

        Matsudo_Library_URL = "https://www.library-matsudo.jp/opac/wopc/pc/pages/SearchDetail.jsp"
        Seibu_Library_URL = "https://www.library.pref.chiba.lg.jp/licsxp-iopac/WOpacMnuTopInitAction.do"

        PATH = r"C:/Users/Masato/Downloads/chromedriver_win32/chromedriver.exe"

        #ブラウザ非表示の設定
        options = Options()
        options.add_argument('--headless')

        driver = webdriver.Chrome(executable_path=PATH, chrome_options=options)

        #松戸市立図書館へアクセス
        driver.get(Matsudo_Library_URL)

        #蔵書検索画面へ
        driver.find_element_by_id("topPageForm:searchDetail").click()

        #検索キーワードを入力
        driver.find_element_by_id("searchDetailForm:txtKeyword1").send_keys(self.keyword)

        """
        #input要素のid属性を取得
        items = driver.find_elements_by_name("chkTargetLibrary")
        item_ids = [item.get_attribute("id") for item in items]

        #label要素のテキストを取得し、idとセットにする
        input_label = {}
        for id in item_ids:
            text = driver.find_element_by_xpath("//label[@for='{}']".format(id)).get_attribute("innerHTML").replace("&nbsp;", "")
            input_label[text] = id
        """

        input_items = {'新松戸分館': 'chkTargetLibrary:3', '六実分館': 'chkTargetLibrary:11',
                       '馬橋分館': 'chkTargetLibrary:7', '八柱分館': 'chkTargetLibrary:17',
                       '小金北分館': 'chkTargetLibrary:14', '館外書庫': 'chkTargetLibrary:21',
                       '馬橋東分館': 'chkTargetLibrary:13', '東部分館': 'chkTargetLibrary:12',
                       '明分館': 'chkTargetLibrary:10', '矢切分館': 'chkTargetLibrary:6',
                       '古ヶ崎分館': 'chkTargetLibrary:8', '小金原分館': 'chkTargetLibrary:2',
                       '常盤平分館': 'chkTargetLibrary:1', '小金分館': 'chkTargetLibrary:4',
                       '本館': 'chkTargetLibrary:0', '松飛台分館': 'chkTargetLibrary:15',
                       '二十世紀が丘分館': 'chkTargetLibrary:16', '子ども読書推進ｾﾝﾀｰ': 'chkTargetLibrary:20',
                       '五香分館': 'chkTargetLibrary:9', '八ヶ崎分館': 'chkTargetLibrary:18',
                       '和名ヶ谷分館': 'chkTargetLibrary:19', '稔台分館': 'chkTargetLibrary:5'}

        #総書籍数
        all_exist_num = 0

        #全ての図書館の情報
        all_library_info = {}

        #各館リスト
        each_library_list = []

        for name in library_names:

            #各館の情報
            library_info = {}

            #館名情報追加
            library_info["library_name"] = name

            #キーワード追加
            library_info["keyword"] = self.keyword

            #書籍情報
            books_info = {}

            #タイトルリスト
            title_list = []

            #出版社リスト
            publisher_list = []

            #出版年月リスト
            publish_date_list = []

            #著者リスト
            author_list = []

            #貸出の有無リスト
            lend_list = []

            #所蔵リスト
            holding_list = []

            #予約状況リスト
            reserve_list = []

            #すべてクリアにしておく
            driver.find_element_by_id("searchDetailForm:chkTargetLibraryAll:0").click()

            #100件表示に変更
            driver.find_element_by_id("searchDetailForm:rdoDisplayCount:3").click()

            #松戸市立図書館の場合
            if name != "西部図書館":

                #対象館の変更
                driver.find_element_by_id(input_items[name]).click()

                #検索ボタンをクリック
                driver.find_element_by_id("searchDetailForm:btnSearch").click()

                #キーワード書籍が存在する場合
                try:
                    exist_num = driver.find_element_by_css_selector("#searchResultListForm .contents .full .list-title font b").get_attribute("innerHTML").replace("件", "")
                    exist_num = int(exist_num)

                    #書籍数追加
                    library_info["exist_num"] = exist_num

                    #総書籍数
                    all_exist_num += exist_num

                    #100件以上であったら、ページ文の情報を引き出す
                    if exist_num > 100:

                        #繰り返し回数の計算
                        range_num = math.ceil(exist_num/100)

                        for _ in range(range_num):

                            #下までスクロール
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                            #1ページに表示されている書籍を取得
                            books = driver.find_element_by_id("searchResultListForm:searchResultTable2:tbody_element").find_elements_by_tag_name("tr")

                            #タイトル/画像/出版社と出版時期/著者名/貸し出しと所蔵と予約を取得
                            for book in books:

                                #必要な情報を取得
                                title = book.find_element_by_class_name("title-font").get_attribute("innerHTML").replace("\u3000", " ").replace("&amp;", " ")
                                publisher_author_lend = book.find_elements_by_class_name("indent1")[1:]
                                publisher_author_lend = [item.get_attribute("innerHTML").replace("\u3000", " ") for item in publisher_author_lend]
                                publisher, author, lend = publisher_author_lend
                                temp_publish = publisher.split(" ")

                                try:
                                    int(temp_publish[-1][0])
                                    publish_date = temp_publish[-1]
                                    publisher = " ".join(temp_publish[:-1])
                                except:
                                    publish_date = ""
                                    publisher = " ".join(temp_publish[:-1])
                                try:
                                    holding_reserve = book.find_elements_by_class_name("indent_m_05")
                                    holding_reserve = [item.get_attribute("innerHTML") for item in holding_reserve]
                                    holding, reserve = holding_reserve
                                except:
                                    holding = ""
                                    reserve = ""

                                if publisher == "":
                                    publisher = "不明"
                                if publish_date == "":
                                    publish_date = "不明"
                                if author == "":
                                    author = "不明"
                                if lend == "" or "貸出" not in lend:
                                    lend = "不明"
                                if lend == "貸出可能":
                                    lend = "○"
                                if lend == "貸出不可":
                                    lend = "×"
                                if holding == "":
                                    holding = "不明"
                                if reserve == "":
                                    reserve = "不明"

                                title_list.append(title)
                                publisher_list.append(publisher)
                                publish_date_list.append(publish_date)
                                author_list.append(author)
                                lend_list.append(lend)
                                holding_list.append(holding)
                                reserve_list.append(reserve)

                            #次のページへ
                            driver.find_element_by_id("searchResultListForm:btnGoNext").click()

                        #別館に移るため蔵書検索に戻る
                        driver.find_element_by_id("historyListTable:1:pageLink").click()

                    #一ページで事足りる場合
                    else:

                        #下までスクロール
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                        #1ページに表示されている書籍を取得
                        books = driver.find_element_by_id("searchResultListForm:searchResultTable2:tbody_element").find_elements_by_tag_name("tr")

                        #タイトル/画像/出版社と出版時期/著者名/貸し出しと所蔵と予約を取得
                        for book in books:

                            #必要な情報を取得
                            title = book.find_element_by_class_name("title-font").get_attribute("innerHTML").replace("\u3000", " ").replace("&amp;", " ")
                            publisher_author_lend = book.find_elements_by_class_name("indent1")[1:]
                            publisher_author_lend = [item.get_attribute("innerHTML").replace("\u3000", " ") for item in publisher_author_lend]
                            publisher, author, lend = publisher_author_lend
                            temp_publish = publisher.split(" ")

                            try:
                                int(temp_publish[-1][0])
                                publish_date = temp_publish[-1]
                                publisher = " ".join(temp_publish[:-1])
                            except:
                                publish_date = ""
                                publisher = " ".join(temp_publish[:-1])
                            try:
                                holding_reserve = book.find_elements_by_class_name("indent_m_05")
                                holding_reserve = [item.get_attribute("innerHTML") for item in holding_reserve]
                                holding, reserve = holding_reserve
                            except:
                                holding = ""
                                reserve = ""

                            if publisher == "":
                                publisher = "不明"
                            if publish_date == "":
                                publish_date = "不明"
                            if author == "":
                                author = "不明"
                            if lend == "" or "貸出" not in lend:
                                lend = "不明"
                            if lend == "貸出可能":
                                lend = "○"
                            if lend == "貸出不可":
                                lend = "×"
                            if holding == "":
                                holding = "不明"
                            if reserve == "":
                                reserve = "不明"

                            title_list.append(title)
                            publisher_list.append(publisher)
                            publish_date_list.append(publish_date)
                            author_list.append(author)
                            lend_list.append(lend)
                            holding_list.append(holding)
                            reserve_list.append(reserve)

                        #別館に移るため蔵書検索に戻る
                        driver.find_element_by_id("historyListTable:1:pageLink").click()

                #見つからない場合
                except:
                    library_info["exist_num"] = 0
                    driver.back()

            #西部図書館の場合
            else:

                #松戸市立図書館へアクセス
                driver.get(Seibu_Library_URL)

                #検索キーワードを入力
                driver.find_element_by_id("SearchKW1Input").send_keys(self.keyword)

                #100件表示に変更
                num_select = driver.find_element_by_id("AssistListSelect")

                # 取得したエレメントをSelectタグに対応したエレメントに変化させる
                num_select_element = Select(num_select)

                # 選択したいvalueを指定する
                num_select_element.select_by_value("100")

                #検索ボタンをクリック
                driver.find_element_by_css_selector(".ex-navi .large").click()

                #キーワード書籍が存在する場合
                try:

                    #キーワード書籍の数
                    exist_num = driver.find_elements_by_css_selector(".read .force")[2].get_attribute("innerHTML")
                    exist_num = int(exist_num)

                    #書籍数追加
                    library_info["exist_num"] = exist_num

                    #総書籍数
                    all_exist_num += exist_num

                    #100件以上であったら、ページ文の情報を引き出す
                    if exist_num > 100:

                        #繰り返し回数の計算
                        range_num = math.ceil(exist_num/100)

                        for _ in range(range_num):

                            #下までスクロール
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                            #表示されているページ内の書籍を取得
                            books = driver.find_elements_by_css_selector(".main .list .ItemNo")

                            #タイトル/画像/出版社と出版時期/著者名/貸し出しと所蔵と予約を取得
                            for book in books:

                                #本情報
                                book_info = {}

                                #必要な情報を取得
                                title = book.find_element_by_class_name("sorthere").find_element_by_tag_name("a").get_attribute("innerHTML").strip().replace("　　", " ").replace("　", " ").replace("&amp;", " ")
                                author, publisher = book.find_elements_by_class_name("innerScrollCell")[1:]
                                author = author.find_element_by_tag_name("a").get_attribute("innerHTML").strip()
                                publisher = publisher.find_element_by_tag_name("a").get_attribute("innerHTML").strip()
                                publish_date = book.find_elements_by_tag_name("td")[-4].get_attribute("innerHTML").strip()
                                lend = book.find_element_by_class_name("a-center").get_attribute("innerHTML").strip()

                                if publisher == "":
                                    publisher = "不明"
                                if publish_date == "":
                                    publish_date = "不明"
                                if author == "":
                                    author = "不明"
                                if lend == "":
                                    lend = "不明"

                                title_list.append(title)
                                publisher_list.append(publisher)
                                publish_date_list.append(publish_date)
                                author_list.append(author)
                                lend_list.append(lend)
                                holding_list.append("不明")
                                reserve_list.append("不明")

                            #次ページへ
                            driver.find_element_by_link_text("次へ")

                    #100件以下の場合
                    else:

                        #下までスクロール(これをしないと取得できずにエラー)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                        #表示されているページ内の書籍を取得
                        books = driver.find_elements_by_css_selector(".main .list .ItemNo")

                        #タイトル/画像/出版社と出版時期/著者名/貸し出しと所蔵と予約を取得
                        for book in books:

                            #本情報
                            book_info = {}

                            #必要な情報を取得
                            title = book.find_element_by_class_name("sorthere").find_element_by_tag_name("a").get_attribute("innerHTML").strip().replace("　　", " ").replace("　", " ").replace("&amp;", " ")
                            author, publisher = book.find_elements_by_class_name("innerScrollCell")[1:]
                            author = author.find_element_by_tag_name("a").get_attribute("innerHTML").strip()
                            publisher = publisher.find_element_by_tag_name("a").get_attribute("innerHTML").strip()
                            publish_date = book.find_elements_by_tag_name("td")[-4].get_attribute("innerHTML").strip()
                            lend = book.find_element_by_class_name("a-center").get_attribute("innerHTML").strip()

                            if publisher == "":
                                publisher = "不明"
                            if publish_date == "":
                                publish_date = "不明"
                            if author == "":
                                author = "不明"
                            if lend == "":
                                lend = "不明"

                            title_list.append(title)
                            publisher_list.append(publisher)
                            publish_date_list.append(publish_date)
                            author_list.append(author)
                            lend_list.append(lend)
                            holding_list.append("不明")
                            reserve_list.append("不明")

                #見つからない場合
                except:
                    library_info["exist_num"] = 0

            books_info["title"] = title_list
            books_info["publisher"] = publisher_list
            books_info["publish_date"] = publish_date_list
            books_info["author"] = author_list
            books_info["lend"] = lend_list
            books_info["holding"] = holding_list
            books_info["reserve"] = reserve_list

            library_info["books_info"] = books_info

            each_library_list.append(library_info)

        all_library_info["all_exist_num"] = all_exist_num
        all_library_info["each_library"] = each_library_list

        return all_library_info
