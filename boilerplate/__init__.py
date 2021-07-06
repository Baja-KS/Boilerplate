import os
import shutil
from abc import ABC, abstractmethod
from string import Template
from typing import List


def touch(file: str, path: str = os.getcwd()) -> None:
    os.chdir(path)
    f = open(file, "w")
    f.close()


def dirOrTouch(name: str) -> None:
    if '.' in name or name == 'Dockerfile':
        f = open(name, "w")
        f.close()
    else:
        os.mkdir(name)
        os.chmod(name, 0o777)


def isDir(name: str) -> bool:
    if '.' in name or name == 'Dockerfile':
        return False
    return True


class Boilerplate(ABC):
    path: str
    projectName: str
    dirTree: dict = {}
    dependencyList: [str]

    type: str = None

    def __init__(self, path: str, projectName: str):
        self.path = path
        self.projectName = projectName

    @classmethod
    def isOfType(cls, type: str) -> bool:
        return cls.type == type

    def init(self) -> None:
        projectDir = os.path.join(self.path, self.projectName)
        if os.path.exists(projectDir):
            print("Project already exists")
            proceed = input('Do you want to continue? [y/N] ').lower() == 'y'
            if proceed:
                return
            exit(1)
        os.mkdir(projectDir)
        os.chmod(projectDir, 0o777)

    def __subDirs(self, node: dict) -> None:
        for name in node.keys():
            if isDir(name):
                oldDir = os.getcwd()
                dirOrTouch(name)
                os.chdir(name)
                self.__subDirs(node[name])
                os.chdir(oldDir)
            else:
                dirOrTouch(name)

    def directoriesAndFiles(self) -> None:
        projectDir = os.path.join(self.path, self.projectName)
        os.chdir(projectDir)
        self.__subDirs(self.dirTree)

    @abstractmethod
    def dependencies(self) -> None:
        pass

    @abstractmethod
    def code(self) -> None:
        pass

    def build(self) -> None:
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

    def _copyFiles(self, fromTo: dict, srcDir: str, dstDir: str):
        for fileFrom in fromTo.keys():
            pathFrom = fileFrom.split('/')
            for fileTo in fromTo[fileFrom]:
                pathTo = fileTo.split('/')
                shutil.copyfile(os.path.join(srcDir, *pathFrom), os.path.join(dstDir, *pathTo))

    def _templateFromFile(self,rootDir:str ,src: str, replace: dict) -> str:
        path=os.path.join(rootDir,*src.split('/'))
        with open(path, "r") as f:
            return Template(f.read()).substitute(**replace)

    def _templateFromTo(self,rootSrc:str, src: str, rootDst:str,dst: str, replace: dict) -> None:
        path = os.path.join(rootDst, *dst.split('/'))
        with open(path, "w") as f:
            f.write(self._templateFromFile(rootSrc,src, replace))

    def _templateComposite(self, templateStr: str, replace: dict, delimiter: str, delimiterLast: str = "\n") -> str:
        components: List[str] = []
        componentCount = len(list(replace.values())[0])
        for i in range(componentCount):
            keys = replace.keys()
            values = list(map(lambda x: x[i], replace.values()))
            componentDict = dict(zip(keys, values))
            components.append(Template(templateStr).substitute(**componentDict))
            if i == componentCount - 1:
                components.append(delimiterLast)
            else:
                components.append(delimiter)

        return ''.join(components)

    def _templateCompositeFromFile(self, rootDir:str,src: str, replace: dict, delimiter: str) -> str:
        path = os.path.join(rootDir, *src.split('/'))
        with open(path, "r") as f:
            return self._templateComposite(f.read(), replace, delimiter)

    def _templateCompose(self,rootDir:str,dst:str,components:List[str])->None:
        path = os.path.join(rootDir, *dst.split('/'))
        with open(path,"w") as f:
            f.write(''.join(components))
