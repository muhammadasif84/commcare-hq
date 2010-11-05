from datetime import datetime, date, timedelta
from bhoma.utils.render_to_response import render_to_response
from django.http import HttpResponse
from bhoma.utils.couch.database import get_db
import logging
import itertools
import re

def device_list(db):
    device_times = db.view('phonelog/device_log_first_last', group=True)
    device_users = db.view('phonelog/device_log_users', group=True)

    dev_users = {}
    for row in device_users:
        dev_id = row['key'][0]
        user = row['key'][1]
        if dev_id not in dev_users:
            dev_users[dev_id] = set()
        dev_users[dev_id].add(user)

    devices = []
    for row in device_times:
        dev = {
            'id': row['key'],
            'first': datetime.utcfromtimestamp(row['value'][0]),
            'last': datetime.utcfromtimestamp(row['value'][1]),
        }
        try:
            dev['users'] = dev_users[dev['id']]
        except KeyError:
            dev['users'] = set()
        devices.append(dev)
    return devices

def overview_list(db):
    devices = device_list(db)
    entries = []
    for dev in devices:
        users = dev['users'] if dev['users'] else set([None])
        for u in users:
            entry = {
                'user': u,
                'device': dev['id'],
                'first': dev['first'],
                'last': dev['last'],
                'other_users': sorted(list(users - set([u]))),
#                'overlaps_with': set(),
            }
            entries.append(entry)

    entries.sort(key=lambda e: (0, e['user'].upper(), e['first']) if e['user'] else (1, e['first']))

#    for u in set(e['user'] for e in entries):
#        user_entries = filter(lambda e: e['user'] == u, entries)
#        for a, b in itertools.combinations(user_entries, 2):
#            pass

    return entries

def devices(request):
    entries = overview_list(get_db())
    return render_to_response(request, 'phonelog/devicelist.html', {'entries': entries})

def device_log(request, device):
    try:
        limit = int(request.GET.get('limit'))
    except:
        limit = 1000

    try:
        skip = int(request.GET.get('skip'))
    except:
        skip = 0

    logdata = get_db().view('phonelog/device_logs',
                            limit=limit, skip=skip, 
                            descending=True, endkey=[device], startkey=[device, {}])
    num = len(logdata)
    logdata = reversed(list(logdata))

    more_prev = (num == limit)
    more_next = (skip > 0)
    overlap = 10
    earlier_skip = skip + (limit - overlap)
    later_skip = max(skip - (limit - overlap), 0)

    def get_short_version(version):
        match = re.search(' (?P<build>#[0-9]+) ', version)
        return match.group('build') if match else None

    def logs(logdata):
        for row in logdata:
            yield {
                'recvd': datetime.utcfromtimestamp(row['key'][1]),
                'date': datetime.strptime(row['value']['@date'][:19], '%Y-%m-%dT%H:%M:%S'),
                'type': row['value']['type'],
                'msg': row['value']['msg'],
                'version': get_short_version(row['value']['version']),
                'full_version': row['value']['version'],
            }

    return render_to_response(request, 'phonelog/devicelogs.html', {
        'logs': logs(logdata),
        'limit': limit,
        'more_next': more_next,
        'more_prev': more_prev,
        'earlier_skip': earlier_skip,
        'later_skip': later_skip,
    })
