__author__ = 'kacprzakp'
import platform


class EditModule():
    def __init__(self):
        self.pathToTheLibrary = "Resource   ${BASEDIR}/src/robot/suite/MigrationLibrary.txt\n"
        self.incompatibleKeywords = ['open browser',
                                     'start selenium server',
                                     'stop selenium server',
                                     'double click element',
                                     'click element',
                                     'choose file',
                                     'click button',
                                     'click image',
                                     'click link',
                                     'go back',
                                     'open context menu',
                                     'press key',
                                     'select all from list',
                                     'select radio button',
                                     'submit form',
                                     'add location strategy',
                                     'call selenium api',
                                     'capture screenshot',
                                     'drag and drop',
                                     'press key native',
                                     'wait until page loaded',
                                     'check whether selenium is stopped']

        self.seleniumKeywords = ['close all browsers',
                                 'set selenium timeout',
                                 'go to',
                                 'delete all cookies',
                                 'wait until page contains element',
                                 'input text',
                                 'page should not contain element']

        if platform.system() == 'Windows':
            self.newLineChar = '\n'
        else:
            self.newLineChar = '\r\n'

    def writeFile(self, path, content):
        # TODO exception
        updated_file = open(path, "w")
        updated_file.writelines(content)
        updated_file.close()

    def edit(self, path):
        newContent = []
        content = self.takeContentFromFile(path)
        sectionsOrder = ['settings','variables','testCases','keywords']
        sections = self.splitToSections(content)

        if sections['settings'] is not None:
            sections['settings'] = self.changeSettings(sections['settings'])

        if sections['variables'] is not None:
            sections['variables'] = self.changeVariables(sections['variables'])

        if sections['testCases'] is not None:
            sections['testCases'] = self.changeKeywords(sections['testCases'])

        if sections['keywords'] is not None:
            sections['keywords'] = self.changeKeywords(sections['keywords'])

        for section in sectionsOrder:
            if sections[section] is not None:
                newContent.extend(sections[section])

        return newContent

    def takeContentFromFile(self, path):
        # TODO exception
        new_file = open(path, "r")
        content = new_file.readlines()
        new_file.close()
        return content

    def splitToSections(self,content):
        sections = {'settings':None,'variables':None, 'testCases':None,'keywords':None}
        availableSections = self.availableSectionsInContent(content)

        iterNumber = 0
        for section in availableSections:
            sections[self.createKey(section)] = content[content.index(section):self.endIndex(availableSections, content, iterNumber)]
            iterNumber+=1
        return sections

    def availableSectionsInContent(self, content):
        sections = []
        listWithSectionsNames = ["*** Settings ***" + self.newLineChar,
                                 '*** Variables ***' + self.newLineChar,
                                 '*** Test Cases ***' + self.newLineChar,
                                 '*** Keywords ***' + self.newLineChar]
        for section in listWithSectionsNames:
            if section in content:
                sections.append(section)
        return sections

    def createKey(self, section):
        tmp = section.replace('*', '').replace(self.newLineChar, '').replace(' ', '')
        return tmp[0].lower() + tmp[1:]

    def endIndex(self, availableSections, content, iterNumber):
        if iterNumber == len(availableSections) - 1:
            indexOfEnd = len(content)
        else:
            indexOfEnd = content.index(availableSections[iterNumber + 1])
        return indexOfEnd

    def changeSettings(self, settings):
        # TODO lambda
        settings = self.addSelenium2Library(settings)
        settings = self.addMigrationLibrary(settings)
        return settings

    def addSelenium2Library(self, settings):
        for line in settings:
            if 'SeleniumLibrary' in line:
                index = settings.index(line)
                settings[index] = 'Library    Selenium2Library' + self.newLineChar
        return settings

    def addMigrationLibrary(self, settings):
        if self.pathToTheLibrary not in settings:
            settings.insert(len(settings) - 1, self.pathToTheLibrary)
        return settings

    def changeKeywords(self, keywords):
        lineNumber = 0
        for line in keywords:
            if self.notMigratedLine(line):
                words = [tmpWord for tmpWord in line.split('  ') if len(tmpWord)>0]
                for word in words:
                    word = word.replace('\n','').replace('\t','')
                    if len(word) > 0 and word[0]==' ':
                        word = word[1:]
                    if len(word) > 0 and word.lower() in self.incompatibleKeywords:
                        keywords = self.migrateLine(word, lineNumber, keywords)
                        break
                    elif 'SeleniumLibrary' in word:
                        keywords[lineNumber] = line.replace('SeleniumLibrary','Selenium2Library')
                        break
            lineNumber += 1
        return keywords

    def notMigratedLine(self,line):
        return 'MigrationLibrary.' not in line and line[0] != '#' and line[0] != '\n' and (
                            line[0] == ' ' or line[0] == '\t')

    def migrateLine(self, keyword, lineNumber, keywords,libraryName='MigrationLibrary.'):
        line = keywords[lineNumber]
        if keyword.lower() == 'start selenium server' or keyword.lower() == 'stop selenium server' or keyword.lower()== 'check whether selenium is stopped':
            updatedLine = '#' + line
        else:
            if keyword.lower() == 'open browser':
                line = line.replace('firefox','${BROWSER}')
            updatedLine = line.replace(keyword,libraryName+keyword)
        keywords[lineNumber] = updatedLine
        return keywords

    def changeVariables(self, variables):
        for line in variables:
            if 'firefox' in line.lower():
                variables[variables.index(line)] = '#' + line
                break
        return variables