DAYS=$(find -maxdepth 1 -name "day*" -type d | wc -w )
DAY=day$((DAYS + 1))
echo "Making $DAY"

mkdir -p $DAY
cp -v day_template.py $DAY/$DAY.py
touch $DAY/example1.txt $DAY/input1.txt
git add $DAY/$DAY.py
tree $DAY
