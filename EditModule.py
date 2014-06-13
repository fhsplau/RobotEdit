__author__ = 'kacprzakp'


class EditModule():
    def __init__(self):
        self.pathToTheLibrary = "Library   C:\\svn\\SP0012\\uat\\trunk\\automatic\\uat_services\\src\\robot\\suite\\MigrationLibrary.txt\n"

    def addMigrationLibrary(self, settings):
        settings.insert(len(settings) - 1, self.pathToTheLibrary)
        return settings

    def addSelenium2Library(self,settings):
        for line in settings:
            if 'SeleniumLibrary' in line:
                index = settings.index(line)
                settings[index] = 'Library    Selenium2Library\n'
        return settings

    def changeSettings(self, settings):
        # add migration library
        # TODO configfile
        # TODO lambda
        settings = self.addSelenium2Library(settings)
        settings = self.addMigrationLibrary(settings)
        return settings

    def edit(self, path):
        newContent = []
        content = self.takeContentFromFile(path)
        #TODO dictionary
        settings = self.takeSettings(content)
        variables = self.takeVariables(content)
        tests = self.takeTests(content)
        keywords = self.takeKeywords(content)

        settings = self.changeSettings(settings)

        #consolidate
        newContent.extend(settings)
        newContent.extend(variables)
        newContent.extend(tests)
        newContent.extend(keywords)

        return newContent

    def takeContentFromFile(self, path):
        # TODO exception
        new_file = open(path, "r")
        content = new_file.readlines()
        new_file.close()
        return content

    def takeSettings(self, content):
        indexOfSettings = content.index('*** Settings ***\n')
        indexOfVariables = content.index('*** Variables ***\n')
        return content[indexOfSettings:indexOfVariables]

    def takeVariables(self, content):
        indexOfVariables = content.index('*** Variables ***\n')
        indexOfTestCases = content.index('*** Test Cases ***\n')
        return content[indexOfVariables:indexOfTestCases]

    def takeTests(self, content):
        indexOfTestCases = content.index('*** Test Cases ***\n')
        indexOfKeywords = content.index('*** Keywords ***\n')
        return content[indexOfTestCases:indexOfKeywords]

    def takeKeywords(self, content):
        indexOfKeywords = content.index('*** Keywords ***\n')
        return content[indexOfKeywords:len(content)]

    def writeFile(self, path, content):
        # TODO exception
        updated_file = open(path, "w")
        updated_file.writelines(content)
        updated_file.close()


path = "C:\\svn\\SP0012\\uat\\trunk\\automatic\\uat_services\\src\\robot\\suite\\Client_Review_Tool\\3.2 Comments\\SP0012_3.2.5_View_Comments.txt"
newFile = "C:\\svn\\SP0012\\uat\\trunk\\automatic\\uat_services\\src\\robot\\suite\\Client_Review_Tool\\3.2 Comments\\SP0012_3.2.5_View_Comments_new.txt"
new_object = EditModule()
editedContent = new_object.edit(path)
new_object.writeFile(path, editedContent)
