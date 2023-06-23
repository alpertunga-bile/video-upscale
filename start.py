from Utilities.Utility import SetLogger, RemoveDirectory, CreateDirectory
from subprocess import run, DEVNULL
from logging import getLogger, Logger, INFO
from platform import system
from os.path import exists, join
from argparse import ArgumentParser

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
    logger.log(INFO, f"Installing {packageName}")
    run(GetInstallCommand(packageName, env), shell=True, stdout=DEVNULL, stderr=DEVNULL)

def CreateEnvironment(logger : Logger, env : str):
    if exists("venv"):
        logger.log(INFO, "Virtual Environment Is Already Created")
        return
    
    CreateDirectory("inputs")
    CreateDirectory("outputs")

    logger.log(INFO, "Creating Virtual Environment")
    run("python -m venv venv", shell=True)

    logger.log(INFO, "Cloning Repository")
    if exists("Real-ESRGAN") is False:
        run("git clone https://github.com/xinntao/Real-ESRGAN.git", shell=True, stdout=DEVNULL, stderr=DEVNULL)

    RunInstallCommand("basicsr", env)
    RunInstallCommand("facexlib", env)
    RunInstallCommand("gfpgan", env)

    if env == "Windows":
        RunInstallCommand("pyreadline3", env)

    logger.log(INFO, "Installing Requirements")
    run(GetInstallCommand(f"-r {join('Real-ESRGAN', 'requirements.txt')}", env), shell=True, stdout=DEVNULL, stderr=DEVNULL)
    
    logger.log(INFO, "Setup Is Started")
    command = ""
    if env == "Windows":
        command += "venv\\Scripts\\activate.bat && cd Real-ESRGAN && "
        command += "..\\venv\\Scripts\\python.exe setup.py develop && "
        command += "..\\venv\\Scripts\\pip.exe uninstall torch torchvision --yes && "
        command += "cd .. && venv\\Scripts\\deactivate.bat"
    elif env == "Linux":
        command += "source venv/bin/activate && cd Real-ESRGAN && python3 setup.py develop && pip3 uninstall torch torchvision --yes && cd .."

    run(command, shell=True, stdout=DEVNULL, stderr=DEVNULL)

    RunInstallCommand("torch torchvision --index-url https://download.pytorch.org/whl/cu118", env)
    RunInstallCommand("xformers", env)
    RunInstallCommand("accelerate", env)

    logger.log(INFO, "Virtual Environment Is Created")

if __name__ == "__main__":
    osEnv = system()
    logger = getLogger()
    SetLogger(logger)

    parser = ArgumentParser("video-upscale", "Upscale videos with Real-ESRGAN")
    parser.add_argument("--reinstall", action="store_true", help="Reinstall environment")
    parser.add_argument("--update", action="store_true", help="Update the Real-ESRGAN repository")
    args = parser.parse_args()    

    if args.reinstall:
        logger.log(INFO, "Deleting environment")
        RemoveDirectory("venv")

    CreateEnvironment(logger, osEnv)

    if args.update:
        logger.log(INFO, "Updating Real-ESRGAN repository")
        run("cd Real-ESRGAN && git pull && cd ..", shell=True, stdout=DEVNULL, stderr=DEVNULL)

    command = ""
    if osEnv == "Windows":
        command += "venv\\Scripts\\activate.bat && venv\\Scripts\\python.exe main.py && venv\\Scripts\\deactivate.bat"
    elif osEnv == "Linux":
        command += "source venv/bin/activate && python3 main.py"
    
    logger.log(INFO, "Running Application")
    run(command, shell=True)