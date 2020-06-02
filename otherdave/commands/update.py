import subprocess
from otherdave.util import dlog

def do(client, message, args):
    dlog.log(client, "Updating to latest OtherDave...")
    subprocess.run("cd ~/OtherDave | git pull | forever restart 0")