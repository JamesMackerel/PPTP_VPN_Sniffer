#!/usr/bin/env bash

echo 'Going into ui directory...'
cd src/ui

for file in ./*
do
    if [ ${file##*.} = "ui" ]; then
        echo Removing ${file%.*}_ui.py
        rm ${file%.*}_ui.py
        echo Generating ${file%.*}_ui.py
        pyuic5 -x ${file} -o ${file%.*}_ui.py
    fi
done
