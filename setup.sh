#!/bin/bash

echo "Installing Python package: pillow"
pip install --user pillow
echo "Installing Python package: pathlib"
pip install --user pathlib
echo "Extrating Images into ./img"
if [ ! -d ./img ]
then
	mkdir img
fi
unzip portraits2.zip
mv portraits2 img

