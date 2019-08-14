#!/bin/bash
is_zlib1g=`dpkg -l | grep zlib1g-dev | wc -l`
is_libssl=`dpkg -l | grep libssl-dev | wc -l`
is_libsqlite3=`dpkg -l | grep libsqlite3-dev | wc -l`
is_sqlite3=`dpkg -l | grep " sqlite3 " | wc -l`

if [[ $is_zlib1g -eq 0 ]]; then
    sudo apt -y install zlib1g-dev
    is_zlib1g=`dpkg -l | grep zlib1g-dev | wc -l`
    if [[ $is_zlib1g -eq 0 ]]; then
        echo "うまくインストールできなかったようです。終了します。"
        read
        exit 0
    fi
fi
if [[ $is_sqlite3 -eq 0 ]]; then
    sudo apt -y install sqlite3
    is_sqlite3=`dpkg -l | grep " sqlite3 " | wc -l`
    if [[ $is_sqlite3 -eq 0 ]]; then
        echo "うまくインストールできなかったようです。終了します。"
        read
        exit 0
    fi
fi
if [[ $is_libsqlite3 -eq 0 ]]; then
    sudo apt -y install libsqlite3-dev
    is_libsqlite3=`dpkg -l | grep libsqlite3-dev | wc -l`
    if [[ $is_libsqlite3 -eq 0 ]]; then
        echo "うまくインストールできなかったようです。終了します。"
        read
        exit 0
    fi
fi
if [[ $is_libssl -eq 0 ]]; then
    sudo apt -y install libssl-dev
    is_libssl=`dpkg -l | grep libssl-dev | wc -l`
    if [[ $is_libssl -eq 0 ]]; then
        echo "うまくインストールできなかったようです。終了します。"
        read
        exit 0 
    fi
fi

is_pyenv_path=`cat ~/.profile | grep "export PYENV_ROOT=$HOME/.pyenv" | wc -l`
if type "pyenv" > /dev/null 2>&1; then
    echo "pyenvはすでに存在します"     #コマンドが存在する時の処理
else
    git clone https://github.com/yyuu/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT=$HOME/.pyenv' >> ~/.profile
    echo 'export PATH=$PYENV_ROOT/bin:$PATH'>> ~/.profile
    echo 'eval "$(pyenv init -)"'>> ~/.profile
    source ~/.profile
    pyenv install 3.6.6

    git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
    echo 'eval "$(pyenv virtualenv-init -)"'
    pyenv virtualenv 3.6.6 relazy3.6.6
    pyenv local relazy3.6.6
    source ~/.profile
fi
is_pyenv=`pyenv version | grep "relazy3.6.6" | wc -l`

if [[ $is_pyenv -eq 1 ]]; then
    echo "使用モジュールのインストールを行います"
    pip3 install -r requirements.txt
else
    echo "pyenvがうまくインストールされていないようです。pyenvを確認してみてください。"
fi
