# Set RabbitMQ Reconnet Delay
# By Zach Cutberth

from subprocess import Popen
from glob import glob
import winreg
from pyrabbit.api import Client
import config

# Open the key and return the handle object.
rabbitMQServerHKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                          "Software\\Wow6432Node\\VMware, Inc.\\RabbitMQ Server")
                          
# Read the value.                      
rabbitMQServerInstallDir = winreg.QueryValueEx(rabbitMQServerHKey, "Install_Dir")
winreg.CloseKey(rabbitMQServerHKey)

# Path to rabbitmqctl
sbinDir = glob(rabbitMQServerInstallDir[0] + '\\rabbitmq_server*' + '\\sbin\\')

# RabbitMQ connection
cl = Client('localhost:15672', config.username, config.password, timeout=100)

# Get queue names
queues = [q['name'] for q in cl.get_queues()]

# Get reconnect delay to set in seconds
delay = input('Enter the RabbitMQ Reconnect Delay in seconds: ')

# Find queues with 'day2day' in the name, if they have messages then purge them.
for queue in queues:
    if 'Prism.day2day' in queue:
        queue_stripped = queue[:-14]
        Popen('rabbitmqctl set_parameter federation-upstream ' + 'V9-' + queue_stripped + '-upstream ' + '"{""uri"":""amqp://prismrs:M3ssag1ngR0cks@' + queue_stripped + '?heartbeat=120"",""reconnect-delay"":' + delay + '}"', cwd=sbinDir[0], shell=True).communicate()
        Popen('rabbitmqctl set_parameter federation-upstream ' + 'Prism-' + queue_stripped + '-upstream ' + '"{""uri"":""amqp://prismrs:M3ssag1ngR0cks@' + queue_stripped + '?heartbeat=120"",""reconnect-delay"":' + delay + '}"', cwd=sbinDir[0], shell=True).communicate()