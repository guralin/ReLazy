#ReLazy
## エレベーターピッチ
英単語を努力せずに覚えたい私向けのReLazyというプロダクトは英単語暗記アプリです。調べた英単語を記録してリマインドすることができ、これは従来の暗記アプリと違って、単語帳を自分で作ることなく英単語を覚えることができます。

## きっかけ
英単語を検索する際に、ブラウザを開くと何故かTwitterやYoutubeなどが一緒に開かれてしまい、やらなければいけないことが全てストップする不具合が発生したためコンソール上で英単語を検索して履歴を保存できるプログラムを作りました。

## 動作環境
- Ubuntu18.04で作成(VMware Workstation 15 Playerで確認)


## 導入
~~~
git clone https://github.com/guralin/ReLazy.git
cd ReLazy/
~~~

pyenvを用いた仮想環境を構築します
~~~
. pyenv_install.sh
~~~
pyenvを構築したくない方は単に
~~~
pip3 install -r requirements.txt
~~~
を実行してください。


relazyコマンドとsqlite3のデータベースを作成します。
~~~
. set_command.sh
python create_db.py
~~~

コンソール上でrelazyコマンドを使用できるようになりました。
~~~
relazy
~~~

## コマンド集
- `relazy`:入力待ち状態になり英単語を入力するたびに、和訳が表示される。
    - 入力待ち状態で`exit()`またはCtrl+Cで入力待ち状態から脱出

- `relazy {検索したい英単語}`:検索したい英単語の和訳を表示する

- `relazy -l {表示したい履歴の数}`:検索の履歴を表示する。

- `relazy -d {表示したい期間}` : 設定した数字の日にちの間の履歴を表示。

