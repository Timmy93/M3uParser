# M3uParser

## Requirements
  - Python 3.5 (or greater)
  - PyYAML library:
    - For local use: `pip3 install PyYAML`
  - Unix-like system (only for the downloader that consists in a sh script, can be substituted by a custom downloader using the settings file)

## Use
It allows to parse a m3u file and to filter, download, move and rename files.

## Software components
  - *M3uParser.py*: It's the real parser that applies filters and has other function
  - *RememberFile.py*: It stores information on the already downloaded files on disk
  - *main.py*: It's the main that read config files and executes the chosen commands
  - *newDownloader.sh*: It's a custom downloader
