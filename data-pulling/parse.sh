#!/usr/bin/bash

# Author: Avik Rao
# Email: avik.rao@gmail.com

# Compile comment parser
echo "BASH: Compiling processcomments.cpp"
clang++ processcomments.cpp -std=c++20 -O3 -march=native -o processcomments
if [ $? -ne 0 ]
then
    exit 1
fi
echo "BASH: Done."

# Compile post parser
echo "BASH: Compiling processposts.cpp"
clang++ processposts.cpp -std=c++20 -O3 -march=native -o processposts
if [ $? -ne 0 ]
then
    exit 1
fi
echo "BASH: Done."

# Parse posts to JSON
echo "BASH: Parsing posts"
./processposts $1
if [ $? -ne 0 ]
then
    exit 1
fi
echo "BASH: Done parsing posts."

# Parse comments to JSON
echo "BASH: Parsing comments"
./processcomments $2
if [ $? -ne 0 ]
then
    exit 1
fi
echo "BASH: Done parsing comments."

# Link posts and comments 
echo "BASH: Linking posts and comments."
python link.py 
if [ $? -ne 0 ]
then
    exit 1
fi
echo "BASH: Script complete."
