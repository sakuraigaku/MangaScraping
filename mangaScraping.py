#! python3
# mangaScraping.py 漫画サイトから必要事項を取得する

import requests
import bs4


# 一覧ページから漫画のページを取得する
def get_manga_page(url):
    global pager_next
    res = requests.get(url)
    res.raise_for_status()
    manga_site = bs4.BeautifulSoup(res.text, features="html.parser")

    manga_links_sources = manga_site.select('.itemThumb ')
    manga_links = []
    for manga in manga_links_sources:
        manga_links.append('https://www.ebookjapan.jp' + manga.get('href'))

    # 次へボタンのURLを更新する
    pager_next_source = manga_site.select('.pager.next')
    pager_next = 'https://www.ebookjapan.jp' + pager_next_source[0].get('href')

    return manga_links


# 漫画のページから必要事項を取得する
def get_manga_date(url):
    res = requests.get(url)
    res.raise_for_status()
    manga_site = bs4.BeautifulSoup(res.text, features="html.parser")

    volume_title = manga_site.select('#volumeTitle')
    book_detail_text = manga_site.select('#bookDetailText')
    book_author = manga_site.select('.bookAuthor')
    book_publisher = manga_site.select('.bookPublisher')

    manga_data = []
    manga_data.append(volume_title[0].getText())
    manga_data.append(book_detail_text[0].getText())
    manga_data.append(book_author[0].getText())
    manga_data.append(book_publisher[0].getText())

    return manga_data


# 次へボタンのURL
pager_next = 'https://www.ebookjapan.jp/ebj/search_book/page1/?q=&search_type=book'
# 漫画のデータのリスト
manga_data_list = []

# とりあえず3回繰り返す
for i in range(3):
    manga_link_url_list = get_manga_page(pager_next)
    for manga_link_url in manga_link_url_list:
        manga_data_list.append(get_manga_date(manga_link_url))

# data.txtに漫画のデータを書き込む
data_file = open('data.txt', 'w')
for manga in manga_data_list:
    for m in manga:
        data_file.write(m + '\n')
data_file.close()
