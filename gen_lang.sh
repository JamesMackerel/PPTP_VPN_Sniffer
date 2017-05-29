#!/usr/bin/env bash

cd src/ui/ui_files

for file in ./*
do
    filename=${file##./*/}
    pylupdate5 ${file} -ts ${filename%.*}_zh_CN.ts
done