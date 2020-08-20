# Nagios Plugin

Nagios Plugin to get stats from an Index

## Syntax / Usage
```
Usage: check_es_index.py -u <user> -p <password> -H <host> -i <indexname> -c [store|indexing|get|search|merges|refresh|flush|warmer|query_cache|fielddata|completion|segments|translog|request_cache|recovery|]

Options:
  -h, --help            show this help message and exit
  -v, --version         Print the version of this script
  -H HOST, --host=HOST  The hostname of elasticsearch database
  -u USER, --user=USER  The user which has access to elasticsearch database
  -p PASSWORD, --password=PASSWORD
                        Password of the user
  -i INDEX, --index=INDEX
                        Index Name
  -c CHECK, --check=CHECK
                        check
  -P PORT, --port=PORT  The port of elasticsearch database
  --ignore-sslcert      Ignore ssl certificate (default="false")
 
```
