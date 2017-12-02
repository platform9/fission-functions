Slack Alerts on Aodh Event Alarms
=

Sends a Slack message with instance details to a channel when compute activity (create/deletion) takes place in OpenStack, resets alarm after notifying users. 

<h2>Preparation</h2>

Requires an [Incoming Webhook](https://api.slack.com/incoming-webhooks). In the script, populate your Openstack credentials, the Incoming Webhook URL, and the alarm ID

<h2>Creating the Alarm</h2>

Create an aodh alarm to be triggered by an event like a VM creation or deletion:

```
aodh alarm create \                                             [
--name server_create \
--type event \
--description 'instance created' \
--alarm-action "http://$FISSION_ROUTER/create-notify-slack" \
--event-type "compute.instance.create.start"
```
Note the Alarm ID after this is created, and populate the `ALARM_ID` variable along with the rest of your information. 

<h2>Creating the Task</h2>

```
fission env create --name openstack-tools --image jmarhee/openstack-tools-2017-12-01
```
```
fission fn create --name slack-alert-compute --url /create-notify-slack --code alarm-receiver-slack.py --env openstack-tools --method POST
```
