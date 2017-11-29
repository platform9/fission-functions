import novaclient
from novaclient import client
from flask import request, redirect
import datetime
import json

USERNAME=""
PASSWORD=""
PROJECT_NAME="service"
AUTH_URL="" 
ROTATION=1 #how many backups to keep 
BACKTYPE="" #daily or weekly

nova = client.Client(novaclient.API_MIN_VERSION, username=USERNAME, password=PASSWORD, project_name=PROJECT_NAME, auth_url=AUTH_URL)

def instanceList():
	instances = []
	for i in nova.servers.list():
		instances.append(str(i.id))
	return instances

def main():
	now = datetime.datetime.now()
	bktime = now.strftime("%Y%m%d-%H%M")
	instances = instanceList()
	for instance in instances:
		nova.servers.backup(instance,"%s-%s" % (instance, bktime),BACKTYPE,ROTATION)
	return "Backups initiated for: \n" +'\n'.join('({}) {}'.format(*k) for k in enumerate(instances, 1))