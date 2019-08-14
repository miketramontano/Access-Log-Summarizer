"""Helper methods for:
   https://github.com/miketramontano/Access-Log-Summarizer
"""

"""Return dictionary

Initialize key in dictionary to default
"""
def init_index(dict, key, default=0):
    if key not in dict:
        dict[key] = default
    return dict

"""Return dictionary

Initialize data group for non-None arguments
"""
def init_group(dict, ip, request, agent):
    dict['total'] = 1
    if ip:
        dict['ips'] = {ip: 1}
    if request:
        dict['requests'] = {request: 1}
    if agent:
        dict['agents'] = {agent: 1}
    return dict

"""Return dictionary

Increment data group for non-None arguments
"""
def increment_group(dict, ip, request, agent):
    dict['total'] += 1
    if ip:
        init_index(dict['ips'], ip)
        dict['ips'][ip] += 1
    if request:
        init_index(dict['requests'], request)
        dict['requests'][request] += 1
    if agent:
        init_index(dict['agents'], agent)
        dict['agents'][agent] += 1
    return dict
