# We split overall on commas and then split each part on its delimiter.
# From there we print the definitions for each word.
awk -F ',' \
    '{split($2, words, " ")}
     {split($3, defs, ";")}
     {for (i=1; i<=length(words); i++){
         for (j=1; j<=length(defs); j++){
             print(words[i] "," defs[j])
            }
        }
    }' ../data/synsets.txt > q1.csv