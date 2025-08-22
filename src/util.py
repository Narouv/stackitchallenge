import os

def getEnv(varname: str) -> str:
    envvar = os.environ.get(varname)
    if envvar is None:
        raise ValueError("Environment variable \"" + str(varname) + "\" does not exist")
    else:
        return envvar
