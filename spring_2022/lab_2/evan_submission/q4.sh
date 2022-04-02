# This is also a straightforward use of uniq and awk to reformat lines.
awk -F ',' \
    '{if($3==1){print($1)}}' q3.csv |
    uniq -c|
    awk -F ' ' '{print($2 "," $1)}' > q4.csv