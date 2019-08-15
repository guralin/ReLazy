#!/bin/bash
is_relazy_command=`cat ~/.bashrc | grep "alias relazy" | wc -l`
if [[ $is_relazy_command -eq 0 ]]; then
    relazy_path=`pwd`
    echo "alias relazy='python ${relazy_path}/scraping.py'" >> ~/.bashrc
    source ~/.bashrc
else
    echo "設定済み"
fi
