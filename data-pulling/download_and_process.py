"""Downloads and unzips reddit post and comment data by month
    before running parsing script and storing results in a folder"""

import requests
import shutil
import sys
import os

__author__ = "Gayatri Gopavajhala"
__email__ = "gayatri924@gmail.com"

#all dates are in year, month format
date = [int(sys.argv[1]), int(sys.argv[2])]
if len(sys.argv) > 3:
  end_date = [int(sys.argv[3]), int(sys.argv[4])]
else:
  end_date = [2021, 6]

#loop through the months
while True:
  #id the file extension for comment data
  if date[0] >= 2018 and date[1] >= 10:
    end_string = ".zst"
    unzip_comment = "unzstd RC_" + str(date[0]) + "-" + str(date[1]) + ".zst"
  elif date[0] > 2017:
    end_string = ".xz"
    unzip_comment = "xz -d RC_" + str(date[0]) + "-" + str(date[1]) + ".xz"
  else:
    end_string = ".bz2"
    unzip_comment = "bzip2 -d RC_" + str(date[0]) + "-" + str(date[1]) + ".bz2"

  comment_link = "https://files.pushshift.io/reddit/comments/RC_" \
                 + str(date[0]) + "-" + '{:02d}'.format(date[1]) + end_string
  comment_save = "RC_" + str(date[0]) + "-" + str(date[1]) + end_string
  post_link = "https://files.pushshift.io/reddit/submissions/RS_" \
              + str(date[0]) + "-" + '{:02d}'.format(date[1]) + ".zst"
  post_save = "RS_" + str(date[0]) + "-" + str(date[1]) + ".zst"

  try:
    os.mkdir("Linked_JSON_Files")
  except OSError as error:
    pass

  #download files
  r = requests.get(comment_link, stream=True)
  with open(comment_save, 'wb') as f:
    f.write(r.content)
    shutil.copyfileobj(r.raw, f)
  r = requests.get(post_link, stream=True)
  with open(post_save, 'wb') as f:
    f.write(r.content)
    shutil.copyfileobj(r.raw, f)

  #unzip files
  os.system(unzip_comment)
  unzip_post = "unzstd RS_" + str(date[0]) + "-" + str(date[1]) + ".zst --memory=2048MB"
  os.system(unzip_post)
  os.remove(post_save)

  #run parsing code and save to folder (not fully tested yet)
  os.system("./parse.sh " + post_save[:-4] + " " + comment_save[:-4])
  shutil.move("linked.json", "Linked_JSON_Files/" + str(date[0]) + "-" + str(date[1]) + ".json")

  #increment month
  if date[0] == end_date[0] and date[1] == end_date[1]:
    break;
  date[1] += 1
  if date[1] == 13:
    date[0] += 1
    date[1] = 1