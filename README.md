# ReLazy
## エレベーターピッチ
英単語を努力せずに覚えたい私向けのReLazyというプロダクトは
英単語暗記アプリです。
調べた英単語を記録してリマインドすることができ、
これは従来の暗記アプリと違って
単語帳を自分で作ることなく英単語を覚えることができます。

## きっかけ
英単語を検索する際に、ブラウザを開くと何故かTwitterやYoutubeなどが一緒に開かれてしまいやらなければいけないことが全てストップする不具合が発生したためコンソール上で英単語を検索して履歴を保存できるプログラムを作りました。

## 動作環境
- Ubuntu18.04で作成
- sqlite3を使用 (`sudo apt install sqlite3` が必要になるかもしれません)
- Python3のモジュール
    - sqlite3
    - click
    - BeautifulSoup

## 導入
~~~
git clone https://github.com/guralin/search_english_word.git
cd search_english_word/
pip install -r requirements.txt
python create_db.py
python scraping.py
~~~
## コマンド集
- `python scraping.py`:入力待ち状態になり英単語を入力すると和訳が表示されます。
    - 入力待ち状態で`exit()`またはCtrl+Cで入力待ち状態から脱出


- `python scraping.py -l {表示したい履歴の数}`:検索の履歴を表示します。


