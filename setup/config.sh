#!/bin/bash

export ENV_DIR="/Users/newberry/Desktop/game/"
virtualenv="VirtEn"

red='\e[1;31m'
purple='\e[1;35m'
green='\e[1;32m'
cyan='\e[1;36m'
NC='\033[0m' # No Color

if [ ! -d $virtualenv ]; then
        echo ""
        echo -e "${green}Creating a virtualenv environment${NC}"
        #virtualenv --system-site-packages $virtualenv
        virtualenv -p python $ENV_DIR/$virtualenv
fi

echo ""
echo -e "${green}Activating the virtualenv environment${NC}"
echo ""
source $ENV_DIR/$virtualenv/bin/activate

echo ""
echo -e "${green}[virtualenv] Installing Python packages${NC}"
echo ""
pip install -r $ENV_DIR/setup/requirements.txt
