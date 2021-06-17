#!/usr/bin/python3.8

# from boilerplate import Boilerplate
from node_express import NodeExpressBoilerplate
import os,sys

def boilerplate(type, path, name):
    if type == 'node-express':
        orm=input('Which ORM will you use,sequelize or mongoose?')
        return NodeExpressBoilerplate(path, name, orm.lower())
    return None

if len(sys.argv) != 4:
    print("Invalid number of arguments")
    exit(1)

type=sys.argv[1]
path=sys.argv[2]
name=sys.argv[3]

# boilerplate=Boilerplate.fromInput(type,path,name)
boilerplate=boilerplate(type,path,name)

boilerplate.build()
