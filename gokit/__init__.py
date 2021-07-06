from typing import List

from boilerplate import Boilerplate
import os


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

    # replace -> key=to be replaced , value=array of values

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
        replace = {
            "endpoints": self._templateComposite(endpointTemplate, {"endpoint": endpoints}, "\n\t", ""),
            "endpointfactories": self._templateComposite(endpointFactoryTemplate, {"endpoint": endpoints}, "\n\t\t", "")
        }
        components: List[str] = [
            self._templateFromFile(scriptDir, "endpoint/head.go", {"module": self.projectName}),
            "\n\n",
            self._templateFromFile(scriptDir, "endpoint/set.go", replace),
            "\n\n",
            self._templateCompositeFromFile(scriptDir, "endpoint/factorymethod.go", {"endpoint": endpoints}, "\n")
        ]
        self._templateCompose(projectDir,"internal/service/endpoints/endpoints.go",components)


        # requestsAndResponses
        components = [
            self._templateFromFile(scriptDir, "requestsAndResponses/head.go", {}),
            "\n\n",
            self._templateCompositeFromFile(scriptDir, "requestsAndResponses/reqres.go", {"endpoint": endpoints}, "\n"),
            "\n\n",
            self._templateCompositeFromFile(scriptDir, "requestsAndResponses/decoderequest.go", {"endpoint": endpoints},
                                            "\n"),
            "\n\n",
            self._templateFromFile(scriptDir, "requestsAndResponses/encoderesponse.go", {})
        ]
        self._templateCompose(projectDir,"/internal/service/endpoints/requestsAndResponses.go",components)

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
