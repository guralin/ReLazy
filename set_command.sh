# !/bin/bash

relazy_path=`pwd`

echo "alias relazy='python ${relazy_path}/scraping.py'" >> ~/.bashrc
source ~/.bashrc
