__author__ = 'kacprzakp'
import platform
from os import listdir
from os.path import isfile, join, isdir


class FilesListing():
    def __init__(self):
        if platform.system() == 'Windows':
            self.separationChar = '\\'
        else:
            self.separationChar = '/'

    def listing(self, path):
        files_from_svn = []
        for f in listdir(path):
            fileExtension = f.split('.')[-1]
            if isfile(join(path, f)) and fileExtension=='txt':
                files_from_svn.append(path+'\\'+f)
            elif isdir(join(path, f)) and ('test'+self.separationChar+'resources') not in join(path,f):
                tmp = self.listing(path + self.separationChar + f)
                for t in tmp:
                    files_from_svn.append(t)
        return files_from_svn

