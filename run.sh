#!/bin/bash

FLASK=/home/alex/code/playground/flashcard/.pyvenv/bin/flask

sudo $FLASK --app verify run --host 0.0.0.0 --port 80 --debug
