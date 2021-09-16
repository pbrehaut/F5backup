import paramiko
from scp import SCPClient
import time
import os
from datetime import datetime
import getpassword.getpasswordenc as getpasswordenc

DOUCS = False
UCSDAY = 5      # 5 == Saturday
BACKUPS = r'C:\ConfigBackups\F5\backups'
UCSPATH = '/var/'
TODAYSPATH = os.path.join(BACKUPS, datetime.strftime(datetime.today(),"%Y-%m-%d"))


def get_file(FileName):
    return os.path.join(TODAYSPATH, FileName + '.txt')


def get_config_paramiko(DeviceKwargs, CommandList):
    try:
        print(DeviceKwargs)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(DeviceKwargs['ip'], username=DeviceKwargs['username'], password=DeviceKwargs['password'])
        F = open(get_file(DeviceKwargs['ip']), 'w')
        for Command in CommandList:
            stdin, stdout, stderr = ssh.exec_command(Command)
            stdout.channel.recv_exit_status()
            Lines = stdout.readlines()
            for Line in Lines:
                F.write(Line)
        F.close()
        ssh.close()
    except Exception as e:
        print(str(e), ' - ', DeviceKwargs['ip'])


def run_command_paramiko(DeviceKwargs, CommandList):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(DeviceKwargs['ip'], username=DeviceKwargs['username'], password=DeviceKwargs['password'])
        for Command in CommandList:
            stdin, stdout, stderr = ssh.exec_command(Command)
            stdout.channel.recv_exit_status()
        ssh.close()
    except Exception as e:
        print(str(e), ' - ', DeviceKwargs['ip'])


def get_file_scp(DeviceKwargs, FileName, LocalPath):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(DeviceKwargs['ip'], username=DeviceKwargs['username'], password=DeviceKwargs['password'])
        scp = SCPClient(ssh.get_transport())
        scp.get(FileName, LocalPath)
        scp.close()
        ssh.close()
    except Exception as e:
        print(str(e), ' - ', DeviceKwargs['ip'])


def main():
    #create direcory for today's config
    if not os.path.exists(TODAYSPATH):
        os.makedirs(TODAYSPATH)

    F5s = [
        {'username': 'root', 'ip': 'f51.foo.net'},
        {'username': 'root', 'ip': 'f52.foo.net'},
        {'username': 'root', 'ip': 'f53.foo.net'},
    ]

    CommandList = [
        'tmsh -q -c "cd /;show running-config recursive"',
    ]

    for DeviceKwargs in F5s:
        DeviceKwargs['password'] = getpasswordenc.get_password(DeviceKwargs['ip'], DeviceKwargs['username'])
        r = get_config_paramiko(DeviceKwargs, CommandList)

        # Only run full backups on day specified
        # If you want to always get the UCS then set the DOUCS global to True
        if time.localtime().tm_wday == UCSDAY or DOUCS:
            ucs_file = UCSPATH + DeviceKwargs['ip'] + ".ucs"
            ucs_create = ["tmsh save sys ucs " + ucs_file]
            r = run_command_paramiko(DeviceKwargs, ucs_create)

            # Copy UCS file to local
            r = get_file_scp(DeviceKwargs, UCSPATH + DeviceKwargs['ip'] + '.ucs', TODAYSPATH)

            # Clear off UCS (no need for this unless you create a new UCS filename for each day.
            # If you just reuse the same filename it will overwrite it on the target F5.
            '''ucs_remove = ['rm ' + ucs_file]
            print(ucs_remove)
            r = run_command_paramiko(DeviceKwargs, ucs_remove)'''

if __name__=='__main__':
    main()
