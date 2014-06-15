__author__ = 'kacprzakp'
import platform


class EditModule():
    def __init__(self):
        # TODO configfile
        self.pathToTheLibrary = "Library   C:\\svn\\SP0012\\uat\\trunk\\automatic\\uat_services\\src\\robot\\suite\\" \
                                + "MigrationLibrary.txt\n"
        self.incompatibleKeywords = ['Open Browser',
                                     'Start Selenium Server',
                                     'Stop Selenium Server',
                                     'Click Element',
                                     'Double Click Element']
        if platform.system() == 'Windows':
            self.newLineChar = '\n'
        else:
            self.newLineChar = '\r\n'

    def addMigrationLibrary(self, settings):
        if self.pathToTheLibrary not in settings:
            settings.insert(len(settings) - 1, self.pathToTheLibrary)
        return settings

    def addSelenium2Library(self, settings):
        for line in settings:
            if 'SeleniumLibrary' in line:
                index = settings.index(line)
                settings[index] = 'Library    Selenium2Library' + self.newLineChar
        return settings

    def changeSettings(self, settings):
        # TODO lambda
        settings = self.addSelenium2Library(settings)
        settings = self.addMigrationLibrary(settings)
        return settings

    def edit(self, path):
        newContent = []
        content = self.takeContentFromFile(path)
        # TODO dictionary
        settings = self.takeSettings(content)
        variables = self.takeVariables(content)
        tests = self.takeTests(content)
        keywords = self.takeKeywords(content)

        settings = self.changeSettings(settings)
        keywords = self.changeKeywords(keywords)

        # consolidate
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
        indexOfSettings = content.index('*** Settings ***' + self.newLineChar)
        indexOfVariables = content.index('*** Variables ***' + self.newLineChar)
        return content[indexOfSettings:indexOfVariables]

    def takeVariables(self, content):
        indexOfVariables = content.index('*** Variables ***' + self.newLineChar)
        indexOfTestCases = content.index('*** Test Cases ***' + self.newLineChar)
        return content[indexOfVariables:indexOfTestCases]

    def takeTests(self, content):
        indexOfTestCases = content.index('*** Test Cases ***' + self.newLineChar)
        indexOfKeywords = content.index('*** Keywords ***' + self.newLineChar)
        return content[indexOfTestCases:indexOfKeywords]

    def takeKeywords(self, content):
        indexOfKeywords = content.index('*** Keywords ***' + self.newLineChar)
        return content[indexOfKeywords:len(content)]

    def writeFile(self, path, content):
        # TODO exception
        updated_file = open(path, "w")
        updated_file.writelines(content)
        updated_file.close()

    def changeKeywords(self, keywords):
        lineNumber=0
        for line in keywords:
            if 'MigrationLibrary.' not in line and line[0] != '#':
                for incompatibleKeyword in self.incompatibleKeywords:
                    if  incompatibleKeyword in line:
                        keywords = self.migrateLine(lineNumber,incompatibleKeyword, line, keywords)
            lineNumber+=1
        return keywords

    def migrateLine(self, lineNumber,keyword, line, keywords):
        if keyword == 'Start Selenium Server' or keyword == 'Stop Selenium Server':
            updatedLine = '#' + line
        else:
            firstChars = line[0:line.index(keyword)]
            updatedLine = firstChars \
                          + 'MigrationLibrary.' \
                          + keyword \
                          + line[(len(firstChars + keyword)):len(line)]
        keywords[lineNumber] = updatedLine
        return keywords


path = "/Users/paverell/tests/Client_Review_Tool/3.2 Comments/SP0012_3.2.5_View_Comments.txt"
# newFile = "C:\\svn\\SP0012\\uat\\trunk\\automatic\\uat_services\\src\\robot\\suite\\Client_Review_Tool\\3.2 Comments\\SP0012_3.2.5_View_Comments_new.txt"
new_object = EditModule()
editedContent = new_object.edit(path)
new_object.writeFile(path, editedContent)
