# This is a straightforward use of uniq to get the uniq words and wc-l to count.
cat q1.csv |
awk -F ',' \
    '{print($1)}'|
uniq |
wc -l > q2.csv