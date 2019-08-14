#!/bin/bash

# dpkgを覗いて、なかったらインストール。
#実行後にdkpgを覗いても、まだ無い場合はインストール失敗とみなして強制終了

# --------------前提パッケージのインストール ----------------------

is_zlib1g=`dpkg -l | grep zlib1g-dev | wc -l`
is_libssl=`dpkg -l | grep libssl-dev | wc -l`
is_libsqlite3=`dpkg -l | grep libsqlite3-dev | wc -l`
is_sqlite3=`dpkg -l | grep " sqlite3 " | wc -l`
is_make=`dpkg -l | grep " make     " | wc -l`
is_gcc=`dpkg -l | grep " gcc     " | wc -l`


if [[ $is_zlib1g -eq 0 ]]; then
    sudo apt -y install zlib1g-dev
    is_zlib1g=`dpkg -l | grep zlib1g-dev | wc -l`
    if [[ $is_zlib1g -eq 0 ]]; then
        echo "うまくインストールできなかったようです。終了します。"
        read
        exit 1
    fi
fi
if [[ $is_libssl -eq 0 ]]; then
    sudo apt -y install libssl-dev
    is_libssl=`dpkg -l | grep libssl-dev | wc -l`
    if [[ $is_libssl -eq 0 ]]; then
        echo "うまくインストールできなかったようです。終了します。"
        read
        exit 1 
    fi
fi
if [[ $is_sqlite3 -eq 0 ]]; then
    sudo apt -y install sqlite3
    is_sqlite3=`dpkg -l | grep " sqlite3 " | wc -l`
    if [[ $is_sqlite3 -eq 0 ]]; then
        echo "うまくインストールできなかったようです。終了します。"
        read
        exit 1
    fi
fi
if [[ $is_libsqlite3 -eq 0 ]]; then
    sudo apt -y install libsqlite3-dev
    is_libsqlite3=`dpkg -l | grep libsqlite3-dev | wc -l`
    if [[ $is_libsqlite3 -eq 0 ]]; then
        echo "うまくインストールできなかったようです。終了します。"
        read
        exit 1
    fi
fi

# pyenv install 3.6.6 の際にmakeが無いと失敗する
if [[ $is_make -eq 0 ]]; then
    sudo apt -y install make
    is_make=`dpkg -l | grep " make     " | wc -l`
    if [[ $is_make -eq 0 ]]; then
        echo "うまくインストールできなかったようです。終了します。"
        read
        exit 1
    fi
fi
if [[ $is_gcc -eq 0 ]]; then
    sudo apt -y install gcc
    is_gcc=`dpkg -l | grep " gcc    " | wc -l`
    if [[ $is_gcc -eq 0 ]]; then
        echo "うまくインストールできなかったようです。終了します。"
        read
        exit 1
    fi
fi
# 対話型インタープリタが使いやすくなる(なくても動く)
sudo apt -y install libbz2-dev libreadline-dev

# ------------------------------------------------------------------

# --------------python仮想環境の整備 -------------------------------

is_pyenv_path=`cat ~/.profile | grep "export PYENV_ROOT=$HOME/.pyenv" | wc -l`
if type "pyenv" > /dev/null 2>&1; then
    echo "pyenvはすでに存在します"     #コマンドが存在する時の処理
else
    git clone https://github.com/yyuu/pyenv.git ~/.pyenv

    if [[ $is_pyenv_path -eq 0 ]]; then
        echo 'export PYENV_ROOT=$HOME/.pyenv' >> ~/.profile
        echo 'export PATH=$PYENV_ROOT/bin:$PATH'>> ~/.profile
        echo 'eval "$(pyenv init -)"'>> ~/.profile
        source ~/.profile
    fi
fi

# pyenvコマンドはここまでで出てくる
is_python366=`pyenv versions | grep " 3.6.6$" | wc -l`
if [[ $is_python366 -eq 0 ]]; then
    echo "pyenvのpython3.6.6をインストールします"
    pyenv install 3.6.6
    is_python366=`pyenv versions | grep " 3.6.6$" | wc -l`
    if [[ $is_python366 -eq 0 ]]; then
        echo "pyenvのpython3.6.6をインストール出来ませんでした。終了します。"
        read
        exit 1
    fi
else
    echo "pyenvのpython3.6.6は既に存在します"
fi

is_virtualenv_path=`cat ~/.profile | grep "eval $(pyenv virtualenv-init -)" | wc -l`
if [[ $is_virtualenv_path -eq 0 ]]; then
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.profile
fi

is_relazy=`pyenv version | grep relazy3.6.6 | wc -l`
if [[ $is_relazy -eq 0 ]]; then
    git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
    pyenv virtualenv 3.6.6 relazy3.6.6
    pyenv local relazy3.6.6
    source ~/.profile
fi
# ------------------------------------------------------------------

# --------------pipモジュールのインストール ------------------------

is_pyenv=`pyenv version | grep "relazy3.6.6" | wc -l`
echo $is_pyenv
if [[ $is_pyenv -eq 1 ]]; then
    echo "使用モジュールのインストールを行います"
    pip3 install -r requirements.txt
else
    echo "pyenvがうまくインストールされていないようです。pyenvを確認してみてください。"
fi

# -----------終了------------
