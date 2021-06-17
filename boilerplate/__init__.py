from abc import ABC, abstractmethod
import sys
import os
# from node_express import NodeExpressBoilerplate


def touch(file, path=os.getcwd()):
    os.chdir(path)
    f = open(file, "w")
    f.close()


def dirOrTouch(name: str):
    if '.' in name or name == 'Dockerfile':
        f = open(name, "w")
        f.close()
    else:
        os.mkdir(name)
        os.chmod(name, 0o777)


def isDir(name: str):
    if '.' in name or name == 'Dockerfile':
        return False
    return True


class Boilerplate(ABC):
    path: str
    projectName: str
    dirTree: dict = {}
    dependencyList: [str]

    # @staticmethod
    # def fromInput(type, path, name):
    #     if type == 'node-express':
    #         orm=input('Which ORM will you use,sequelize or mongoose?')
    #         return NodeExpressBoilerplate(path, name, orm.lower())
    #     return None

    def __init__(self, path, projectName):
        self.path = path
        self.projectName = projectName

    def init(self):
        projectDir = os.path.join(self.path, self.projectName)
        if os.path.exists(projectDir):
            print("Project already exists")
            exit(1)
        os.mkdir(projectDir)
        os.chmod(projectDir, 0o777)

    def __subDirs(self, node: dict):
        for name in node.keys():
            if isDir(name):
                oldDir = os.getcwd()
                dirOrTouch(name)
                os.chdir(name)
                self.__subDirs(node[name])
                os.chdir(oldDir)
            else:
                dirOrTouch(name)

    def directoriesAndFiles(self):
        projectDir = os.path.join(self.path, self.projectName)
        os.chdir(projectDir)
        self.__subDirs(self.dirTree)

    @abstractmethod
    def dependencies(self):
        pass

    @abstractmethod
    def code(self):
        pass

    def build(self):
        print("===================================")
        print("Boilerplate code script by BajaKS ;)")
        print("===================================")
        print("=======INITIALIZING PROJECT STRUCTURE=========")
        self.init()
        print("=======CREATING DIRECTORIES AND FILES=========")
        self.directoriesAndFiles()
        print("=======INSTALLING DEPENDENCIES=========")
        self.dependencies()
        print("=======WRITING CODE=========")
        self.code()
        print("===================================")
        print("Project initialized.Make something awesome <3")
        print("===================================")
