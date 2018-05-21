#!/usr/bin/python

import papi
import getpass
import json
import sys
import getopt

def getnamebysid (cluster,  provider, zone, sid, importr, password):
  path = "/platform/1/auth/users/SID:"+sid+"?zone="+zone+"&query_member_of=False&provider="+provider
  (status, reason, resp) = papi.call (cluster, '8080', 'GET', path, '', any, 'application/json', user, password)
  if status != 200:
    err_string = "ERROR: Bad Status: status"
    sys.stderr.write (err_string)
    exit (status)
  data = json.loads (resp)
  return (data['users'][0]['id'])

def usage ():
  sys.stderr.write ("Usage: getuserbysid.py {-c | --cluster=cluster} {-s | --sid=sid} [{-p | --provider=provider}] [{-z | --zone=zone}]\n")
  sys.stderr.write ("	{-c | --cluster} : Specify cluster Name/IP\n")
  sys.stderr.write ("	{-s | --sid} : Specify SID to resolve\n")
  sys.stderr.write (" 	[{-p | --provider}] : Specify a Provider (default = ads)\n")
  sys.stderr.write ("	[{-z | --zone}] : Specify an Access Zone (default = System\n")
  sys.stderr.write ("	[{-h | --help}] : Display Usage\n")

provider = "ads"
zone = "System"
sid = ""
cluster = ""

optlist, args = getopt.getopt (sys.argv[1:], 's:c:p:z:h', ['sid=', 'cluster=', 'provider=', 'zone=', 'help'])
for opt, a, in optlist:
  if opt in ('-s', '--sid'):
    sid = a
  if opt in ('-s', '--cluster'):
    cluster = a
  if opt in  ('-p', '--provider'):
    provider = a
  if opt in ('-z', '--zone'):
    zone = a
  if opt in ('-h', '--help'):
    usage ()
    exit (0)

if sid == "" or cluster == "":
  sys.stderr.write ("SID and cluster must be specified\n")
  usage()
  exit (1)
user = raw_input ("User: ")
password = getpass.getpass ("Password: ")
name = getnamebysid (cluster, provider, zone, sid, user, password)
print name
