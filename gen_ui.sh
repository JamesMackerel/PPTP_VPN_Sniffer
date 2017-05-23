#!/usr/bin/env bash

echo 'Going into ui directory...'
cd src/ui

for file in ./ui_files/*
do
    if [ ${file##*.} = "ui" ]; then
        filename=${file##./*/}
        echo Removing ./ui_py/${filename%.*}_ui.py
        rm ./ui_py/${filename%.*}_ui.py
        echo Generating ./ui_py/${filename%.*}_ui.py
        pyuic5 -x ./ui_files/${filename} -o ./ui_py/${filename%.*}_ui.py
    fi
done
