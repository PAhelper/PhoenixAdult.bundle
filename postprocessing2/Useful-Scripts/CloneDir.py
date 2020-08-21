import os
import shutil

## Put source directory (where sub-directories are) and destination directory (where you want the tree directory to be matched). Use \\ ! For example Z:\\Folder1\\Subfolder1
source= ""
destination= ""

subdirectories = os.listdir(source)
for directory in subdirectories:
    newdir = (destination+'\\'+directory)
    if(os.path.exists(newdir)):
        print ("Path already exists!")
    else:
        os.mkdir(newdir)
        print ("Path created: " +newdir)
