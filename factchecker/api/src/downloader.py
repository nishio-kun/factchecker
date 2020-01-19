"""
Web サイトから記事をダウンロード、パースするモジュール。
"""
import lxml.html
import readability
import re
import requests


def get_page(url):
    """
    受け取った URL のサイトの本文を取得します。
    """
    response = requests.get(url)
    document = readability.Document(response.content)
    title = document.title()
    content_html = document.summary()
    content_text = lxml.html.fromstring(content_html).text_content().strip()

    return title, content_text


def split_to_sentences(document):
    """
    受け取った文章を文ごとに分割します。
    """
    document = re.sub(r'[\s]', '', document)
    sentences = re.findall(r'.*?[。]', document)
    return sentences


if __name__ == '__main__':
    url = 'http://saunners.saunasoken.jp/interviews/1.html'
    title, content = get_page(url)
    # print(title)
    # print(content)
    sentences = split_to_sentences(content)
    import pprint
    pprint.pprint(sentences)
