# TermNovel: LN from terminal
TermNovel is a made to download light novels in text (.txt) format. The downloaded chapters can be opened using nano, vim or a word processing software. 

# Features 
- Interactive 
- Set custom file extensions
- Files can be viewed using any text editor
- Resume downloads

# Getting Started
First of all, clone this repository and then

Run
```sh
chmod u+x install.sh
```

And then
```sh
./install.sh
```

Now you can run commands:

- for help:
```sh
python -m termnovel
```

- to download:
```sh
python -m termnovel download
```

**All downloaded files are stored in /termshared/downloads directory**

# TODOs
- ~~Be able to change the file extension during downloads~~ (DONE)
- Be able to change the download directory