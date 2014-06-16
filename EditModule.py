__author__ = 'kacprzakp'
import platform


class EditModule():
    def __init__(self):
        # TODO configfile
        self.pathToTheLibrary = "Library   C:\\svn\\SP0012\\uat\\trunk\\automatic\\uat_services\\src\\robot\\suite\\" \
                                + "MigrationLibrary.txt\n"
        # double click element must be before click element
        self.incompatibleKeywords = ['open browser', 'start selenium server', 'stop selenium server', 'double click element', 'click element', 'choose file', 'click button', 'click image', 'click link', 'go back', 'open context menu', 'press key', 'select all from list', 'select radio button', 'submit form', 'add location strategy', 'call selenium api', 'capture screenshot', 'drag and drop', 'press key native', 'wait until page loaded']

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
        lineNumber = 0
        for line in keywords:
            if self.notMigratedLine(line):
                word = [tmpWord for tmpWord in line.split('  ') if len(tmpWord)>0][0].replace('\n','').replace('\t','')
                if word[0]==' ':
                    word = word[1:]
                if len(word) > 0 and word.lower() in self.incompatibleKeywords:
                    keywords = self.migrateLine(word, lineNumber, keywords)
            lineNumber += 1
        return keywords

    def notMigratedLine(self,line):
        return 'MigrationLibrary.' not in line and line[0] != '#' and line[0] != '\n' and (
                            line[0] == ' ' or line[0] == '\t')

    def migrateLine(self, keyword, lineNumber, keywords):
        line = keywords[lineNumber]
        if keyword.lower() == 'start selenium server' or keyword.lower() == 'stop selenium server':
            updatedLine = '#' + line
        else:
            updatedLine = line[0:line.index(keyword)] \
                          + 'MigrationLibrary.' \
                          + keyword \
                          + line[(len(line[0:line.index(keyword)] + keyword)):len(line)]
        keywords[lineNumber] = updatedLine
        return keywords
