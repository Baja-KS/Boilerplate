from typing import Optional, List

from boilerplate import Boilerplate
import os
from string import Template
import shutil


class GoKitBoilerplate(Boilerplate):
    dirTree = {
        "cmd": {
            "server": {
                "main.go": {}
            }
        },
        "internal": {
            "database": {
                "database.go": {},
                "migration.go": {}
            },
            "service": {
                "endpoints": {
                    "endpoints.go": {},
                    "requestsAndResponses.go": {},
                },
                "middlewares": {
                    "logging.go": {},
                    "instrumenting.go": {}
                },
                "transport": {
                    "http.go": {},
                    "grpc.go": {}
                },
                "service.go": {}
            }
        },
        "docker-compose.yml": {},
        "Dockerfile": {},
        ".env": {},
        ".env.example": {}
    }
    type = 'go-kit'

    def __init__(self, path: str, projectName: str):
        super().__init__(path, projectName)

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

    # replace -> key=to be replaced , value=array of values
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

    # def _templateCompose(self):

    def code(self) -> None:
        endpointTemplate: str = "${endpoint}Endpoint endpoint.Endpoint"
        endpointFactoryTemplate: str = "${endpoint}Endpoint:    Make${endpoint}Endpoint(svc),"
        serviceMethodTemplate: str = "${endpoint}(ctx context.Context) ()"
        httpHandlerTemplate: str = "${endpoint}Handler:=httptransport.NewServer(ep.${endpoint}Endpoint," \
                                   "endpoints.Decode${endpoint}Request,endpoints.EncodeResponse) "
        httpRouterHandleTemplate: str = 'router.Handle("/${endpoint}",${endpoint}Handler).Methods(http.MethodGet)'
        endpoints = []
        while True:
            new = input('Insert an endpoint name or / if done:')
            if new == '/':
                break
            endpoints.append(new)
        scriptDir = os.path.dirname(__file__)
        projectDir = os.path.join(self.path, self.projectName)

        toCopy = {
            "env": [".env", ".env.example"],
            "Dockerfile": ["Dockerfile"],
            "docker-compose.yml": ["docker-compose.yml"],
            "database.go": ["internal/database/database.go"],
            "migration.go": ['internal/database/migration.go'],
            "instrumenting.go": ['internal/service/middlewares/instrumenting.go']
        }
        self._copyFiles(toCopy, scriptDir, projectDir)

        service = input('Enter service name:')


        # main
        self._templateFromTo(scriptDir,"main.go",projectDir,"cmd/server/main.go",{'service': service, 'module': self.projectName})

        # logging
        self._templateFromTo(scriptDir,"logging.go",projectDir,"internal/service/middlewares/logging.go", {'module': self.projectName})

        # endpoints
        components: List[str] = []
        pathDst = os.path.join(projectDir, "internal", "service", "endpoints", "endpoints.go")
        components.append(self._templateFromFile(scriptDir,"endpoint/head.go", {"module": self.projectName}))
        components.append("\n\n")

        replace = {
            "endpoints": self._templateComposite(endpointTemplate, {"endpoint": endpoints}, "\n\t",""),
            "endpointfactories": self._templateComposite(endpointFactoryTemplate, {"endpoint": endpoints}, "\n\t\t","")
        }
        components.append(self._templateFromFile(scriptDir,"endpoint/set.go", replace))
        components.append("\n\n")

        # pathSrc = os.path.join(scriptDir, 'endpoint', 'factorymethod.go')
        components.append(self._templateCompositeFromFile(scriptDir,"endpoint/factorymethod.go", {"endpoint": endpoints}, "\n"))
        components.append("\n\n")
        with open(pathDst, "w") as f:
            f.write(''.join(components))

        # requestsAndResponses
        components: List[str] = []
        pathDst = os.path.join(projectDir, "internal", "service", "endpoints", "requestsAndResponses.go")
        components.append(self._templateFromFile(scriptDir,"requestsAndResponses/head.go", {}))
        components.append("\n\n")

        components.append(self._templateCompositeFromFile(scriptDir,"requestsAndResponses/reqres.go", {"endpoint": endpoints}, "\n"))
        components.append("\n\n")

        components.append(self._templateCompositeFromFile(scriptDir,"requestsAndResponses/decoderequest.go", {"endpoint": endpoints}, "\n"))
        components.append("\n\n")

        components.append(self._templateFromFile(scriptDir,"requestsAndResponses/encoderesponse.go", {}))

        with open(pathDst, "w") as f:
            f.write(''.join(components))

        # service
        replace = {
            "service": service,
            "endpoints": self._templateComposite(serviceMethodTemplate, {"endpoint": endpoints}, "\n\t")
        }
        self._templateFromTo(scriptDir,"service.go",projectDir,"internal/service/service.go",replace)

        # transport-http
        replace = {
            "handlers": self._templateComposite(httpHandlerTemplate, {"endpoint": endpoints}, "\n\t"),
            "router": self._templateComposite(httpRouterHandleTemplate, {"endpoint": endpoints}, "\n\t"),
            "module": self.projectName
        }
        self._templateFromTo(scriptDir,"transport/http.go",projectDir,"internal/service/transport/http.go",replace)

    def dependencies(self) -> None:
        os.system(f"go mod init {self.projectName}")
        os.system("go mod vendor")

    def build(self) -> None:
        print("===================================")
        print("Boilerplate code script by BajaKS ;)")
        print("===================================")
        print("=======INITIALIZING PROJECT STRUCTURE=========")
        self.init()
        print("=======CREATING DIRECTORIES AND FILES=========")
        self.directoriesAndFiles()
        print("=======WRITING CODE=========")
        self.code()
        print("=======INSTALLING DEPENDENCIES=========")
        self.dependencies()
        print("===================================")
        print("Project initialized.Make something awesome <3")
        print("===================================")
