#!/usr/bin/python

###############################################################################################################
# Language     :  Python
# Filename     :  check_es_index.py
# Autor        :  https://github.com/Puller23
# Description  :  Skript to check elasticsearch indicies stats
# Repository   :  https://github.com/Puller23/check_es_index
###############################################################################################################


import urllib2
from optparse import OptionParser
import base64
import sys
import ssl
import os.path
from json import dumps, loads, load

VERSION = 0.1

# NAGIOS return codes
OK       = 0
WARNING  = 1
CRITICAL = 2
UNKNOWN  = 3

def main():
  message = ''
  parser = OptionParser(usage='%prog -u user -p password -H cloud.example.com -i indexname -c [store|indexing|get|search|merges|refresh|flush|warmer|query_cache|fielddata|completion|segments|translog|request_cache|recovery|]')
  parser.add_option('-v', '--version', action='store_true', dest='version', default=False, help='Print the version of this script')
  parser.add_option('-H', '--host', dest='host', type='string', help='The hostname of elasticsearch database')
  parser.add_option('-u', '--user', dest='user', type='string', help='The user which has access to elasticsearch database')
  parser.add_option('-p', '--password', dest='password', type='string', help='Password of the user')
  parser.add_option('-i', '--index', dest='index', type='string', help='Index Name')
  parser.add_option('-c', '--check', dest='check', choices=['docs','store','indexing','get','search','merges','refresh','flush','warmer','query_cache','fielddata','completion','segments' 'translog','request_cache','recovery'], help='check')
  parser.add_option('-P', '--port', type=int, dest='port', default='9200', help='The port of elasticsearch database')
  parser.add_option('--ignore-sslcert', dest='ignore_sslcert', default=False, action='store_true', help='Ignore ssl certificate (default="false")')

  (options, args) = parser.parse_args()

  # Print the version of this script
  if options.version:
    print('Version {}'.format(VERSION))
    sys.exit(0)

  # Validate the user input...
  if not options.user and not options.password and not options.host and not options.index:
    parser.print_help()
    sys.exit(3)

  if not options.user:
    parser.error('Username is required, use parameter [-u|--username].')
    sys.exit(3)

  if not options.password:
    parser.error('Password is required, use parameter [-p|--password].')
    sys.exit(3)

  if not options.host:
    parser.error('Hostname is required, use parameter [-H|--hostname]')
    sys.exit(3)

  if not options.index:
    parser.error('Indexname is required, use parameter [-i|--index]')
    sys.exit(3)
  
  if not options.check:
    parser.error('Check is required, use parameter [-c|--check]')
    sys.exit(3)

  # Create the url to access the api
  url = "https://{}:{}/{}/_stats".format(options.host, options.port, options.index)
  
  # Encode credentials as base64
  credential = base64.b64encode(options.user + ':' + options.password)

  try:
    # Create the request
    request = urllib2.Request(url)
    # Add the authentication and api request header
    request.add_header('Authorization', "Basic %s" % credential)

    ctx = ssl.create_default_context()

    if(options.ignore_sslcert):
      ctx.check_hostname = False
      ctx.verify_mode = ssl.CERT_NONE

    response = urllib2.urlopen(request, context=ctx)

    # Read the content
    content = response.read()

  except urllib2.HTTPError as error:      # User is not authorized (401)
    print 'ERROR - [WEBREQUEST] {0} {1}'.format(error.code, error.reason)
    sys.exit(3)

  except urllib2.URLError as error:	# Connection has timed out (wrong url / server down)
    print 'ERROR - [WEBREQUEST] {0}'.format(str(error.reason).split(']')[0].strip())
    sys.exit(3)

  try:
    # Convert response to json
    json = loads(content)
    
  except ValueError, e:
    print 'ERROR - [JSON] {0}'.format(str(error.reason).split(']')[0].strip())
    sys.exit(3)

  get_json_data(json, options.index, options.check)
  

def get_json_data(json, index, check):
    message = []
    for key in json["indices"][index]["total"][check]:
      value = json["indices"][index]["total"][check][key]
      message.append("{}={}".format(key, value))
    msg = ', '.join(map(str, message))
    print ("OK | " + msg)

if __name__ == '__main__':
    main()
