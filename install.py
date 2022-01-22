import os, platform, subprocess, re, sys


def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command = "sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line, 1)
    return ""

loca = os.path.join(os.path.dirname(__file__))

if "Intell" in get_processor_name():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", loca + '\mrequ-i.txt'])

else:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", loca + '\mrequ-a.txt'])

