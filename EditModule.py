__author__ = 'kacprzakp'


class EditModule():
    def __init__(self):
        pass

    def takeContentFromFile(self, path):
        #TODO exception
        new_file = open(path, "r")
        content = new_file.readlines()
        new_file.close()
        return content

    def edit(self, path):
        content = self.takeContentFromFile(path)
        content.append("\nChange!!!\n")
        return content

    def writeFile(self,path,content):
        #TODO exception
        updated_file = open(path,"w")
        updated_file.writelines(content)
        updated_file.close()



path = "C:\\svn\\SP0012\\uat\\trunk\\automatic\\uat_services\\src\\robot\\suite\\Client_Review_Tool\\3.2 Comments\\SP0012_3.2.5_View_Comments.txt"
newFile = "C:\\svn\\SP0012\\uat\\trunk\\automatic\\uat_services\\src\\robot\\suite\\Client_Review_Tool\\3.2 Comments\\SP0012_3.2.5_View_Comments_new.txt"
new_object = EditModule()
editedContent = new_object.edit(path)
new_object.writeFile(path,editedContent)