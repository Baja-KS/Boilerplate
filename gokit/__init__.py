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

    def _templateFromFile(self, src: str, replace: dict) -> str:
        with open(src, "r") as f:
            return Template(f.read()).substitute(**replace)

    def _templateFromTo(self, src: str, dst: str, replace: dict) -> None:
        with open(dst, "w") as f:
            f.write(self._templateFromFile(src, replace))

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

    def _templateCompositeFromFile(self, src: str, replace: dict, delimiter: str) -> str:
        with open(src, "r") as f:
            return self._templateComposite(f.read(), replace, delimiter)

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
        pathSrc = os.path.join(scriptDir, 'main.go')
        pathDst = os.path.join(projectDir, "cmd", "server", "main.go")
        self._templateFromTo(pathSrc, pathDst, {'service': service, 'module': self.projectName})

        # logging
        pathSrc = os.path.join(scriptDir, 'logging.go')
        pathDst = os.path.join(projectDir, "internal", "service", "middlewares", "logging.go")
        self._templateFromTo(pathSrc, pathDst, {'module': self.projectName})

        # endpoints
        components: List[str] = []
        pathSrc = os.path.join(scriptDir, 'endpoint', 'head.go')
        pathDst = os.path.join(projectDir, "internal", "service", "endpoints", "endpoints.go")
        components.append(self._templateFromFile(pathSrc, {"module": self.projectName}))
        components.append("\n\n")

        pathSrc = os.path.join(scriptDir, 'endpoint', 'set.go')
        replace = {
            "endpoints": self._templateComposite(endpointTemplate, {"endpoint": endpoints}, "\n\t",""),
            "endpointfactories": self._templateComposite(endpointFactoryTemplate, {"endpoint": endpoints}, "\n\t\t","")
        }
        components.append(self._templateFromFile(pathSrc, replace))
        components.append("\n\n")

        pathSrc = os.path.join(scriptDir, 'endpoint', 'factorymethod.go')
        components.append(self._templateCompositeFromFile(pathSrc, {"endpoint": endpoints}, "\n"))
        components.append("\n\n")
        with open(pathDst, "w") as f:
            f.write(''.join(components))

        # requestsAndResponses
        components: List[str] = []
        pathSrc = os.path.join(scriptDir, 'requestsAndResponses', 'head.go')
        pathDst = os.path.join(projectDir, "internal", "service", "endpoints", "requestsAndResponses.go")
        components.append(self._templateFromFile(pathSrc, {}))
        components.append("\n\n")

        pathSrc = os.path.join(scriptDir, 'requestsAndResponses', 'reqres.go')
        components.append(self._templateCompositeFromFile(pathSrc, {"endpoint": endpoints}, "\n"))
        components.append("\n\n")

        pathSrc = os.path.join(scriptDir, 'requestsAndResponses', 'decoderequest.go')
        components.append(self._templateCompositeFromFile(pathSrc, {"endpoint": endpoints}, "\n"))
        components.append("\n\n")

        pathSrc = os.path.join(scriptDir, 'requestsAndResponses', 'encoderesponse.go')
        components.append(self._templateFromFile(pathSrc, {}))

        with open(pathDst, "w") as f:
            f.write(''.join(components))

        # service
        pathSrc = os.path.join(scriptDir, 'service.go')
        pathDst = os.path.join(projectDir, "internal", "service", "service.go")
        replace = {
            "service": service,
            "endpoints": self._templateComposite(serviceMethodTemplate, {"endpoint": endpoints}, "\n\t")
        }
        self._templateFromTo(pathSrc, pathDst, replace)

        # transport-http
        pathSrc = os.path.join(scriptDir, 'transport', 'http.go')
        pathDst = os.path.join(projectDir, "internal", "service", "transport", "http.go")
        replace = {
            "handlers": self._templateComposite(httpHandlerTemplate, {"endpoint": endpoints}, "\n\t"),
            "router": self._templateComposite(httpRouterHandleTemplate, {"endpoint": endpoints}, "\n\t"),
            "module": self.projectName
        }
        self._templateFromTo(pathSrc, pathDst, replace)

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
