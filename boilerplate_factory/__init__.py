from laravel import LaravelBoilerplate
from node_express import NodeExpressBoilerplate

def BoilerplateFactory(type:str, path:str, name:str):
    if type == 'node-express':
        orm=input('Which ORM will you use,sequelize or mongoose?  ')
        return NodeExpressBoilerplate(path, name, orm.lower())
    if type == 'laravel':
        return LaravelBoilerplate(path,name)
    return None