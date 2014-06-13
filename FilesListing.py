__author__ = 'kacprzakp'
from os import listdir
from os.path import isfile, join, isdir


class FilesListing():
    def __init__(self):
        pass

    def listing(self, path):
        files_from_svn = []
        for f in listdir(path):
            if isfile(join(path, f)) and '.xml' not in f and '.html' not in f:
                files_from_svn.append(path+'\\'+f)
            elif isdir(join(path, f)):
                tmp = self.listing(path + '\\' + f)
                for t in tmp:
                    files_from_svn.append(t)
        return files_from_svn


files = FilesListing().listing('C:\\svn\\SP0012\\uat\\trunk\\automatic\\uat_services\\src\\robot\\suite\\Client_Review_Tool')
for f in files:
    print f
