#!/bin/bash
# Put your command below to execute your program.
# Replace "./my-program" with the command that can execute your program.
# Remember to preserve " $@" at the end, which will be the program options we give you.

usage="\
naivebayes.sh -i data-dir -o outputfile [-n labeled-data size]
where:
  -h, help
    show this help text.
  -i, data-dir
    path od data containing 3 directory, train, unlabeled and test.
  -o, outputfile
    the output file name.
  [ -n labeled-data size] 
    the number of labeled document in each class the program uses."

while getopts ':h:i:o:n:' option
do
  case $option in
    h) echo "$usage"
       exit
       ;;
    i) input=$OPTARG
       ;;
    o) output=$OPTARG
       ;;
    n) labeled_size=$OPTARG
       ;;
    \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done

if [ -z "$input" ]; then
    echo "missing data-dir"
    echo "$usage" >&2
	exit 1
fi

string="$input $output $labeled_size"
echo $string
python3 naivebayes.py $string
