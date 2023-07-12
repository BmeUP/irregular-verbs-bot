#!/bin/sh
cd src/
python db_init.py
cd ../
python main.py