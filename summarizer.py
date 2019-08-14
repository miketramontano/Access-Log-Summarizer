#!/usr/bin/python

"""Simple script to analyze a standard http log file (common log format).
   The script will finds most common IPs, user agents, and requests.
   This script was developed for academic/educational purposes.

   https://github.com/miketramontano/Access-Log-Summarizer
"""

import os
import re
import json
from time import strftime

from helper_functions import init_index, init_group, increment_group

# Settings

should_print_result = True
should_write_result = False
max_entries_per_type = 3
log_path = '/tmp/logs/access.log'
output_path = '/tmp/'
clf_regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) "?(.*?)"? "(.*?)" "(.*?)"'
ip_index = 0
request_index = 2
agent_index = 6

# Todo: check arguments to override settings

# Parsed data

ips = {}
requests = {}
agents = {}

# Process access log
with open(log_path, 'r') as log_file:
    for line in log_file:
        # Parse into tuple; note: this assumes a match!
        data = re.match(clf_regex, line).groups()
        ip = data[ip_index] or '(NOT SET)'
        request = data[request_index] or '(NOT SET)'
        agent = data[agent_index] or '(NOT SET)'

        # Collect per-IP data
        if ip not in ips:
            ips[ip] = {'ip': ip}
            init_group(ips[ip], None, request, agent)
        else:
            increment_group(ips[ip], None, request, agent)

        # Collect per-request data
        if request not in requests:
            requests[request] = {'request': request}
            init_group(requests[request], ip, None, agent)
        else:
            increment_group(requests[request], ip, None, agent)

        # Collect per-agent data
        if agent not in agents:
            agents[agent] = {'user-agent': agent}
            init_group(agents[agent], ip, request, None)
        else:
            increment_group(agents[agent], ip, request, None)

# Sort by totals and reduce to max number of entries
ips = sorted(ips.values(), key=lambda i: i['total'], reverse=True)[:max_entries_per_type]
requests = sorted(requests.values(), key=lambda i: i['total'], reverse=True)[:max_entries_per_type]
agents = sorted(agents.values(), key=lambda i: i['total'], reverse=True)[:max_entries_per_type]

# Print titles and pretty JSON
if should_print_result:
    print('*** IP Addresses ***')
    print(json.dumps(ips, indent=4))
    print('*** Requests ***')
    print(json.dumps(requests, indent=4))
    print('*** User Agents ***')
    print(json.dumps(agents, indent=4))

# Write analysis file
if should_write_result:
    stamp = strftime('%Y_%m_%dT%H_%M_%S')
    output_file = open(output_path + 'access_log_analysis_' + stamp + '.json', 'a')
    output_file.writelines(json.dumps(ips + requests + agents))
    output_file.close()
