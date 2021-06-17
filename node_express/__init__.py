from boilerplate import Boilerplate
import os


class NodeExpressBoilerplate(Boilerplate):
    dirTree = {
        "app": {
            "api": {
                "controllers": {},
                "middleware": {
                    "error.js":{}
                },
                "routes": {},
                "strategies": {
                    "strategyJwt.js": {}
                }
            },
            "resources": {
                "img": {}
            },
            "utils": {},
            "app.js": {},
            "Dockerfile": {},
            "server.js": {},
        },
        ".env": {},
        ".env.example": {},
        "docker-compose.yml": {}
    }

    def __init__(self, path, projectName, orm):
        if orm != 'mongoose' and orm != 'sequelize':
            return
        super().__init__(path, projectName)
        self.orm = orm
        if orm=='mongoose':
            self.dependencyList.append('mongoose')
            self.dirTree['app']['models']={}
        elif orm=='sequelize':
            self.dirTree['app']['.sequelizerc.js']={}
            # self.dirTree['app']['config']={}
            # self.dirTree['app']['config']['config.js']={}
            self.dependencyList.append('sequelize')
            self.dependencyList.append('sequelize-cli')
            self.dependencyList.append('pg')
            self.dependencyList.append('pg-hstore')
            self.dependencyList.append('mysql2')


    orm:str

    dependencyList = ['bcrypt', 'express', 'cors', 'envfile', 'passport', 'passport-jwt',
                      'multer', 'nodemailer', 'nodemon', ]

    def dependencies(self):
        scriptDir=os.path.dirname(__file__)
        print(scriptDir)
        appDir = os.path.join(self.path, self.projectName, "app")
        os.chdir(appDir)
        os.system("npm init -y")
        for dependency in self.dependencyList:
            os.system(f"npm install {dependency} --save")
        if self.orm=='sequelize':
            os.system("npx sequelize-cli init")
            os.chdir(os.path.join(appDir,"config"))
            os.remove("config.json")
            os.chdir(scriptDir)
            template=open('config.js','r')
            code=template.read()
            template.close()
            os.chdir(os.path.join(appDir, "config"))
            f=open("config.js","w")
            f.write(code)
            f.close()


    def code(self):
        scriptDir = os.path.dirname(__file__)
        os.chdir(scriptDir)
        server=None
        app=None
        config=None
        dockerfile=None
        error=None
        sequelizerc=None
        env=None
        try:
            with open("server.js","r") as file:
                server=file.read()
            with open("env", "r") as file:
                env = file.read()
            with open("error.js","r") as file:
                error=file.read()
            with open("Dockerfile", "r") as file:
                dockerfile=file.read()
            if self.orm=='sequelize':
                with open("app.js", "r") as file:
                    app=file.read()
                with open("sequelizerc.js", "r") as file:
                    sequelizerc = file.read()
            elif self.orm=='mongoose':
                with open("appMongoose.js", "r") as file:
                    app = file.read()
        except IOError:
            print("Error writing code")
            exit(1)

        os.chdir(os.path.join(self.path, self.projectName))
        with open(".env", "w") as file:
            file.write(env)
        with open(".env.example","w") as file:
            file.write(env)

        appDir = os.path.join(self.path, self.projectName, "app")
        os.chdir(appDir)

        with open("server.js","w") as file:
            file.write(server)
        with open("app.js", "w") as file:
            file.write(app)
        with open("Dockerfile", "w") as file:
            file.write(dockerfile)

        os.chdir(os.path.join(appDir,"api","middleware"))
        with open("error.js", "w") as file:
            file.write(error)
        os.chdir(appDir)

        if self.orm=='sequelize':
            with open(".sequelizerc.js", "w") as file:
                file.write(sequelizerc)



