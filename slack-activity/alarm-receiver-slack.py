import json
import requests
from flask import request, redirect
from urllib.parse import urlparse
from urllib.parse import urlencode
import urllib
import novaclient
from novaclient import client
from keystoneauth1.identity import v2
from keystoneauth1 import session
from keystoneclient.v2_0 import kclient
from aodhclient.v2 import aclient

#Platform 9 Credentials
USERNAME=""
PASSWORD=""
PROJECT_NAME="service"
AUTH_URL=""
ALARM_ID=""
#Slack
CHANNEL_NAME=""
SLACK_INCOMING_WEBHOOK_URL=""

auth = v2.Password(username=USERNAME, password=PASSWORD,tenant_name=PROJECT_NAME, auth_url=AUTH_URL)
sess = session.Session(auth=auth)
aodh = aclient.Client(session=sess,service_type="alarming")
nova = client.Client(novaclient.API_MIN_VERSION, username=USERNAME, password=PASSWORD, project_name=PROJECT_NAME, auth_url=AUTH_URL)

def slack_callout(response):
    try:
        response = { "text" : "%s" %(response), "channel": "#%s" % (CHANNEL_NAME), "username": "PF9-Activity-Bot", "icon_url": ""}
        slack_response = requests.post(SLACK_INCOMING_WEBHOOK_URL,json=response, headers={'Content-Type': 'application/json'})
        return slack_response.status_code
    except:
        return "Slack Callout Failed."

def queryNova(instance_id_in):
	output = []
	for server in nova.servers.list():
		if server.id == instance_id_in:
			output.append({
				'Name': server.name,
				'Networking': [
					server.networks
				],
				'Date': server.updated,
				'Status': server.status,
				'User': server.user_id
			})
	return json.dumps(output)

def alarm_reset():
	response = aodh.alarm.set_state(ALARM_ID,"ok")
	return response

def main():
	response = json.loads(str(request.get_data(), "utf-8"))
	for t in response['reason_data']['event']['traits']:
		if t[0] == "instance_id":
			instance_id_in = str(t[2])
			result = queryNova(instance_id_in)
			slack_callout(result)
			alarm_reset()
			return result

