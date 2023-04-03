# pp_cmd_dtcd_read_graph
Postprocessing command "dtcd_read_graph"
## Description
Command reads graph from datacad

### Arguments
- name - positional argument, text, required graph name in datacad
- id - keyword argument, text, not required, first characters of graph id (if name not unique)

### Usage example
```
dtcd_read_graph graph_name
dtcd_read_graph graph_name, id=9df
```

## Getting started
### Installing
1. Create virtual environment with post-processing sdk 
```bash
    make dev
```
That command  
- downloads [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- creates python virtual environment with [postprocessing_sdk](https://github.com/ISGNeuroTeam/postprocessing_sdk)
- creates link to current command in postprocessing `pp_cmd` directory 

2. Configure `otl_v1` command. Example:  
```bash
    vi ./venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/otl_v1/config.ini
```
Config example:  
```ini
[spark]
base_address = http://localhost
username = admin
password = 12345678

[caching]
# 24 hours in seconds
login_cache_ttl = 86400
# Command syntax defaults
default_request_cache_ttl = 100
default_job_timeout = 100
```

3. Configure storages for `readFile` and `writeFile` commands:  
```bash
   vi ./venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/readFile/config.ini
   
```
Config example:  
```ini
[storages]
lookups = /opt/otp/lookups
pp_shared = /opt/otp/shared_storage/persistent
external_data = /opt/otp/external_data
```

### Run dtcd_read_graph
Use `pp` to run dtcd_read_graph command:  
```bash
pp
Storage directory is /tmp/pp_cmd_test/storage
Commmands directory is /tmp/pp_cmd_test/pp_cmd
query: | otl_v1 <# makeresults count=100 #> |  dtcd_read_graph 
```
## Deploy
1. Unpack archive `pp_cmd_dtcd_read_graph` to postprocessing commands directory
2. Configure config.ini. Config example:  
```ini
[dtcd_server]
address = http://localhost
username = admin
password = admin
```