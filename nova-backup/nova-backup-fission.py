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

def findInstance(instance):
	for i in nova.servers.list():
		if i.name == instance:
			return str(i.id)

def novaBackup(hostname):
	now = datetime.datetime.now()
	bktime = now.strftime("%Y%m%d-%H%M")
	instanceId = findInstance(hostname)
	if instanceId == None or instanceId == "":
		return "No server ID matching hostname %s" % (hostname)
	else:
		nova.servers.backup(instanceId,"%s-%s" % (hostname, bktime),BACKTYPE,ROTATION)
		return "Backup initiated for %s (%s)" % (hostname, instanceId)

def main():
	hostname = json.loads(request.get_data().decode('utf-8'))['hostname']
	return novaBackup(str(hostname))