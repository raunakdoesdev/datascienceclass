# First we need to print only up to the header (hence the 169)
# Then we remove those annoying prelimintary bars
# We then split on commas and keep a running count that gets reset with each new state we encounter

tail -n 169 ../data/worldcup-semiclean.txt |
sed 's/|//g' |
awk '
/^[A-Z]/ {state=$0; count=0}
/([0-9][0-9][0-9][0-9])/ {
    split($0, arr, ",");
    for (i=1; i<=length(arr); i++) {
        print(state "," arr[i] "," count);
    }
}
{count++}
' > q3.csv
