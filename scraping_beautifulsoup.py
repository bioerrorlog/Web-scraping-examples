"""
Reference:
https://qiita.com/kuto/items/9730037c282da45c1d2b
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


def main():
    keyword = "\"Evolution of an Optimal Lexicon under Constraints from Embodiment\""
    number = 1
    search_results_df = get_search_results_df(keyword,number)
    filename = "Google_Scholar.csv"
    search_results_df.to_csv(filename, encoding="utf-8")

def get_search_results_df(keyword,number):
    columns = ["title", "writer", "year", "citations", "url", "pdf"]
    df = pd.DataFrame(columns=columns) #表の作成
    html_doc = requests.get("https://scholar.google.co.jp/scholar?hl=ja&as_sdt=0%2C5&num=" + str(number) + "&q=" + keyword).text
    soup = BeautifulSoup(html_doc, "html.parser") # BeautifulSoupの初期化

    tags1 = soup.find_all("h3", {"class": "gs_rt"})  # title&url
    tags2 = soup.find_all("div", {"class": "gs_a"})  # writer&year
    tags3 = soup.find_all(text=re.compile("引用元"))  # citation
    tags4 = soup.find_all("div", {"class": "gs_or_ggsm"}) # pdf

    for tag1, tag2, tag3, tag4 in zip(tags1, tags2, tags3, tags4):
        title = tag1.text.replace("[HTML]","")
        url = tag1.select("a")[0].get("href")
        writer = re.sub(r'\d', '', tag2.text)
        year = tag2.text
        year = re.sub(r'\D', '', year)
        citations = tag3.replace("引用元","")
        pdf = tag4.select("a")[0].get("href")
        se = pd.Series([title, writer, year, citations, url, pdf], columns)
        df = df.append(se, columns)
    return df


if __name__ == '__main__':
    main()