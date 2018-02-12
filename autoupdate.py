# -*- coding: utf-8 -*-
"""
Automatically update the program if needed.
"""

import urllib3
import json
import shutil

from __version__ import __int_version__

# oops...
AGENT = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}

def has_update():
    http = urllib3.PoolManager(headers=AGENT)
    versions = http.request('GET',
            "https://api.github.com/repos/mishaturnbull/PySpeedTest/releases")
    data = json.loads(versions.data)
    latest_version = data[0]['tag_name']
    latest_int_version = int(''.join(latest_version[1:].split('.')))
    return latest_int_version > __int_version__

def get_download_url():
    http = urllib3.PoolManager(headers=AGENT)
    versions = http.request('GET',
            "https://api.github.com/repos/mishaturnbull/PySpeedTest/releases")
    data = json.loads(versions.data)
    exe_url = data[0]['assets'][0]['browser_download_url']
    return exe_url

# this is shamefully stolen from:
# https://stackoverflow.com/a/27389016/4612410
# because I don't know how to use urllib3 
def download_file(url):
    local_filename = url.split('/')[-1]
    http = urllib3.PoolManager()

    with http.request('GET', url, preload_content=False) as r, open(local_filename, 'wb') as out_file:       
        shutil.copyfileobj(r, out_file)
    return local_filename

def download_update():
    download_file(get_download_url())
