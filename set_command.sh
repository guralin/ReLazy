#!/bin/bash
is_relazy_command=`cat ~/.bashrc | grep "alias relazy" | wc -l`
if [[ $is_relazy_command -eq 0 ]]; then
    relazy_path=`pwd`
    echo "alias relazy='python ${relazy_path}/main.py'" >> ~/.bashrc
    source ~/.bashrc
else
    echo "relazy_pathは設定済み"
fi

count_deepl_environment=`cat ~/.bashrc | grep "export DEEPL_AUTH_KEY" | wc -l`

if [[ $count_depl_environment -eq 0 ]]; then
    echo "DEEPL_AUTH_KEYを入力してください＞"
    read AUTH_KEY
    echo "export DEEPL_AUTH_KEY=$AUTH_KEY" >> ~/.bashrc
    source ~/.bashrc
else
    echo "AUTH_KEYは設定済み"
fi
