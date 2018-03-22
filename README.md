# Labeling Stage1
## Overview
Select 5%-15% favored images. The labeling result is saved in *logs* folder with the naming convention as *userid-date.txt*,
which means it would creat a file for earch rater per rating day.
## Setup and Run
1. Create a soft linking from source image folder to the project main directory and name it as imgs.
```
cd \project\directory
ln -s \source\image\folder imgs
```
Or modify the variable *img_folder_checklist_file* in main.py to source image folder

2. Modifiy or create the *img-folder-checklist.txt* as the schedule of the labeling task of group folders. The checklist file is edited with
```
groupfolder1 0
groupfolder2 1
groupfolder3 1
```
where the second string is the mark mearning whether the groupfolder has been labeled.

3. Run the program `python main.py`

## Note
The program has been tested with python3.6 under MacOS.
