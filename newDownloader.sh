#!/bin/sh
dir_temp=$2
dir_finished=$3
cd $dir_temp
for i in `seq 1 40`; do
  timeout 15 curl -O -L -J -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36" -C - $1
  res=$?
  if test "$res" != "0"; then
    continue
  else
    mv $dir_temp/* $dir_finished
    exit 1
  fi
  echo "Test #$i"
done
rm $dir_temp/*
cd -
exit 10
