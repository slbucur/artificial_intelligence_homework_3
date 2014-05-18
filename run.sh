#!/bin/bash

echo "Spam/Ham"
echo ""
eval python spam.py $1 $3

echo "Rotten Tomatoes"
echo ""
eval python rotten-tomatoes.py $1 $2 $3
