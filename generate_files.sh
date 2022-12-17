# /bin/bash
if [ $# != 3 ]
  then
    echo "\033[31mERROR: Incorrect arguments supplied\033[0m"
    echo "Usage: generate_files {year} {day} {name}"
    exit 1;
fi

echo "Generating files for Problem \"\033[34m$3\033[0m\" on Day \033[34m$2\033[0m of Year \033[34m$1\033[0m..."
rm -rf $(pwd)/$1/"day"$2
mkdir -p $(pwd)/$1/"day"$2/"data"
echo "DATA_FILE = 'data/data_test.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()" > $(pwd)/$1/"day"$2/$3"_1.py"
echo "DATA_FILE = 'data/data_test.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()" > $(pwd)/$1/"day"$2/$3"_2.py"
touch $(pwd)/$1/"day"$2/"data/data_test.txt"
touch $(pwd)/$1/"day"$2/"data/data.txt"
