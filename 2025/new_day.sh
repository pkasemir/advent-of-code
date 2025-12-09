if [ $# != 1 ]; then
    echo "USAGE: new_day.sh <dayN>"
    exit 1
fi

mkdir -p $1
cp -v day_template.py $1/$1.py
touch $1/example1.txt $1/input1.txt
tree $1