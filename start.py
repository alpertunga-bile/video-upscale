from subprocess import run, DEVNULL
from logging import Logger, getLogger, INFO, StreamHandler, Formatter
from sys import stdout
from platform import system
from os.path import exists, join
from os import mkdir

def SetLogger(logger : Logger):
    logger.setLevel(INFO)

    handler = StreamHandler(stdout)
    handler.setLevel(INFO)
    formatter = Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)   

def GetInstallCommand(package : str, env : str):
    returnCommand = ""
    if env == "Windows":
        returnCommand += "venv\\Scripts\\activate.bat && "
        returnCommand += f"venv\\Scripts\\pip.exe install {package} && "
        returnCommand += "venv\\Scripts\\deactivate.bat"
    elif env == "Linux":
        returnCommand += f"source venv/bin/activate && pip3 install {package}"

    return returnCommand

def RunInstallCommand(packageName : str, env : str):
    logger.log(INFO, f"Installing {packageName.upper()}")
    run(GetInstallCommand(packageName, env), shell=True, stdout=DEVNULL, stderr=DEVNULL)

def CreateEnvironment(logger : Logger, env : str):
    if exists("venv"):
        logger.log(INFO, "Virtual Environment Is Already Created")
        return
    
    if exists("inputs") is False:
        mkdir("inputs")

    if exists("outputs") is False:
        mkdir("outputs")

    logger.log(INFO, "Creating Virtual Environment")
    run("python -m venv venv", shell=True)

    logger.log(INFO, "Cloning Repository")
    run("git clone https://github.com/xinntao/Real-ESRGAN.git", shell=True, stdout=DEVNULL, stderr=DEVNULL)

    RunInstallCommand("basicsr", env)
    RunInstallCommand("facexlib", env)
    RunInstallCommand("gfpgan", env)

    logger.log(INFO, "Installing Requirements")
    run(GetInstallCommand(f"-r {join('Real-ESRGAN', 'requirements.txt')}", env), shell=True, stdout=DEVNULL, stderr=DEVNULL)
    
    logger.log(INFO, "Setup Is Started")
    command = ""
    if env == "Windows":
        command += "venv\\Scripts\\activate.bat && cd Real-ESRGAN && "
        command += "..\\venv\\Scripts\\python.exe setup.py develop && "
        command += "cd .. && venv\\Scripts\\deactivate.bat"
    elif env == "Linux":
        command += "source venv/bin/activate && cd Real-ESRGAN && python3 setup.py develop && cd .."

    run(command, shell=True, stdout=DEVNULL, stderr=DEVNULL)

    logger.log(INFO, "Virtual Environment Is Created")

if __name__ == "__main__":
    osEnv = system()
    logger = getLogger()
    SetLogger(logger)    

    CreateEnvironment(logger, osEnv)

    command = ""
    if osEnv == "Windows":
        command += "venv\\Scripts\\activate.bat && venv\\Scripts\\python.exe main.py && venv\\Scripts\\deactivate.bat"
    elif osEnv == "Linux":
        command += "source venv/bin/activate && python3 main.py"
    
    logger.log(INFO, "Running Application")
    run(command, shell=True)