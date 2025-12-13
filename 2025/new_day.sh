DAYS=$(find -maxdepth 1 -name "day*" -type d | wc -w )
DAY=day$((DAYS + 1))
echo "Making $DAY"

mkdir -p $DAY
echo "day_template.py updated to $DAY/$DAY.py"
sed "s/^from util_template/from util$DAY/" day_template.py > $DAY/$DAY.py
cp -v util_template.py $DAY/util$DAY.py
touch $DAY/example1.txt $DAY/input1.txt
git add $DAY/$DAY.py $DAY/util$DAY.py
tree $DAY
