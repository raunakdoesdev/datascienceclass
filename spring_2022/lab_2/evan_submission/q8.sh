# Strategy: 
# First remove all " from input file
# Then build out a CSV line by l ine, printing on the DJ lines and resetting on the Date lines
# Splitting each line into a prefix and suffix
# NOTE: some lines contain multipl : characters, so I have to join the suffix together
cat ../data/wmbr.txt | 
sed "s/\"//g" |
awk '
BEGIN {print("Date,Artist,Song,Album,Label,Show,DJ")}
{split($0, arr, ":");
prefix = arr[1];
suffix = arr[2];
for (i = 3; i <= length(arr); i++) {
    suffix = suffix ":" arr[i];
}
if (prefix == "Date") {
    line = "\"" suffix "\"";
}
else{
    line = line ",\"" suffix "\"";
}
if (prefix == "DJ"){
    print line;
}
}
' > q8.csv