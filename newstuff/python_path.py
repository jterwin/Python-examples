#from os.path import expanduser

def full_path(name):
    import os
    
    if (name[0]=="/"):
        fullname = name
    elif (name[:2]=="~/"):
        prefix = os.path.expanduser("~")
        fullname = prefix+"/"+name[2:]
    else:
        prefix = os.getcwd()
        fullname = prefix+"/"+name

    return fullname


file = "/test.txt"
fullfile = full_path(file)
print file+"  -->  "+fullfile

file = "~/test.txt"
fullfile = full_path(file)
print file+"  -->  "+fullfile

file = "test.txt"
fullfile = full_path(file)
print file+"  -->  "+fullfile

file = "../test.txt"
fullfile = full_path(file)
print file+"  -->  "+fullfile
