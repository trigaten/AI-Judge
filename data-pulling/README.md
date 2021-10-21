# Setup instructions

## Required tools
- Python 3.6+
- C++ compiler supporting C++11
- Unix shell

## Steps
1. Download the comment and post file for a certain month from [Pushshift](https://files.pushshift.io/reddit "Pushshift")
	- Posts are available at https://files.pushshift.io/reddit/submissions/
	- Comments are available at https://files.pushshift.io/reddit/comments/
	- Posts and comments should be from the **same month and same year.**
		- e.g. `RC_2021-06.zst` and `RS_2021-06.zst`
	- **The earliest usable month/year is November 2018 (RS_2018-11 and RC_2018-11)**
2. Decompress the compressed comment and post files
	- Pushshift is very inconsistent with its compression method for files, but will almost always be ZStandard (.zst extension) for files from November 2018 onward.
	- If the compression format is ZStandard (.zst file extension), unzip with `unzstd`
		- e.g. `unzstd RC_2021-06.zst`
	- If the compression format is BZip2 (.bz2 file extension), unzip with `bzip2 -d`
		- e.g. `bzip2 -d RC_2021-06.bz2`
	- If the compression format is XZ (.xz file extension), unzip with `xz -d`
		- e.g. `xz -d RC_2021-06.xz`
	- For the purposes of this project, the relevant files (November 2018 onward, as previously mentioned) *should* only be in .zst format on Pushshift.
3. Run the bash script to compile and run the parsers and linkers:
	- `./parse.sh <post file> <comment file>`
	- `<post file>`: Decompressed post file from Pushshift, typically in the format `RS_YYYY-MM`
		- e.g. `RS_2021-06`
	- `<comment file>`: Decompressed comment file from Pushshift, typically in the format `RC_YYYY-MM`
		- e.g. `RC_2021-06`
	- e.g. `./parse.sh RS_2021-06 RC_2021-06`
4. Done! Final output is in the file `linked.json` and can be used for training.