#!/usr/bin/python3.8

import os,sys
from boilerplate_factory import BoilerplateFactory


if len(sys.argv) != 4:
    print("Invalid number of arguments")
    exit(1)

type=sys.argv[1]
path=sys.argv[2]
name=sys.argv[3]

boilerplate=BoilerplateFactory().fromInput(type,path,name)

boilerplate.build()
