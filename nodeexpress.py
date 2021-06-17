from boilerplate import Boilerplate
import os


class ExpressjsBoilerplate(Boilerplate):
    dirTree = {
        "projectBase": {
            "app": {
                "api": {
                    "controllers": {},
                    "middleware": {},
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
    }

    dependencyList = ['bcrypt', 'express', 'cors', 'envfile', 'passport', 'passport-jwt', 'pg',
                      'pg-hstore', 'multer', 'nodemailer', 'nodemon', 'sequelize', 'sequelize-cli', 'mysql2',
                      'mongoose']

    def dependencies(self):
        appDir = os.path.join(self.path, self.projectName, "app")
        os.chdir(appDir)
        os.system("npm init -y")
        for dependency in self.dependencyList:
            os.system(f"npm install {dependency} --save")
        if 'sequelize' in self.dependencyList:
            os.system("npx sequelize-cli init")

    def code(self):
        pass
