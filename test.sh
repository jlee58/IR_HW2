#!/bin/bash
# Put your command below to execute your program.
# Replace "./my-program" with the command that can execute your program.
# Remember to preserve " $@" at the end, which will be the program options we give you.
usage="\

execute.sh [-r] -i query-file -o ranked-list -m model-dir -d NTCIR-dir

where:

  -h, help
	show this help text.
  -r, relevance feedback
	If specified, turn on the relevance feedback in program.
  -i, query-file
	The input query file.
  -o, ranked-list
	The output ranked list file.
  -m, model-dir
	The input model directory, which includes three files:
	┌model-dir/vocab.all
	├model-dir/file-list
	└model-dir/inverted-index
  -d, NTCIR-dir
	The directory of NTCIR documents, which is the path name of CIRB010 directory.
	ex. If the directory's pathname is /tmp2/CIRB010, it will be \"-d /tmp2/CIRB010\"."

while getopts ':h:ri:o:m:d:' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
    i) input=$OPTARG
       ;;
    o) output=$OPTARG
       ;;
    m) model=$OPTARG
       ;;
    d) ntcdir=$OPTARG
       ;;
    r) feedback='feedback'
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done

if [ -z "$input" ]; then
    echo "$usage" >&2
	exit 1
fi
if [ -z "$output" ]; then
    echo "$usage" >&2
	exit 1
fi
if [ -z "$model" ]; then
    echo "$usage" >&2
	exit 1
fi
if [ -z "$ntcdir" ]; then
    echo "$usage" >&2
	exit 1
fi

string="$input $output $model $ntcdir $feedback"
python3 process.py $string
