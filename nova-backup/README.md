OpenStack Nova Backup with Fission
=

<h2> Single Instance Backup</h2>

Creates a backup of VMs with provided hostname.

<h3>Create task</h3>

Setup the environment:

```
fission env create --name python-openstack --image quay.io/jmarhee/python-openstack-tools
```

create the route, and upload the script:

```
fission fn create --name novabackup --method POST --url /nova-backup --code nova-backup-fission.py --env python-openstack
```

<h3>Run task</h3>

```
curl -X POST -H "Content-Type: application/json" -d '{"hostname":"test04"}' $FISSION_ROUTER/nova-backup
```

<h2> Automated Instance Backups</h2>

Using the `fission-nova-backup-all.py` script, Fission cron can be used to create an automated backup of instances.

```
fission fn create --name backup-all --env python-openstack --code fission-nova-backup-all.py
```

and a cronjob defined with:

```
fission tt create --function backup-all --cron '0 3 * * 1'
```

to trigger this function at, for example, 3 AM every Monday. 