import subprocess
from utils.utils import *


def create_private_keys(client_name):
    command = f'{WG_GENKEY} | {SUDO_TEE} {WORK_DIR}{client_name}{END_PRIVATE_KEY}'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_private_key, stderr = process.communicate()
    return(stdout_private_key)


def create_pub_keys(private_key, client_name):
    command = f"{ECHO} '{private_key}' | {WG_PUBKEY} | {SUDO_TEE} {client_name}{END_PUBLIC_KEY}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_pub_key, stderr = process.communicate()
    return(stdout_pub_key)