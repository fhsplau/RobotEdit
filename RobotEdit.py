__author__ = 'kacprzakp'

import sys
import os
from EditModule import *
from FilesListing import *

def main(argv):
    if len(argv) < 2:
        sys.stderr.write("To less arguments. Usage: %s /path/to/the/svn/folder" % (argv[0],))
        return 1

    if not os.path.exists(argv[1]):
        sys.stderr.write("ERROR: Folder %r was not found!" % (argv[1],))
        return 1

    path = argv[1]

    files = FilesListing().listing(path)
    for f in files:
        new_object = EditModule()
        edited_content = new_object.edit(f)
        new_object.writeFile(f,edited_content)

if __name__ == "__main__":
    sys.exit(main(sys.argv))