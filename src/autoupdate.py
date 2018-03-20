# -*- coding: utf-8 -*-
"""
Automatically update the program if needed.
"""

import json
import shutil
import platform
import os
import urllib3

from __version__ import __version__, is_version_greater

# give github a user-agent so they don't block our requests
AGENT = {'user-agent': 'Python-urllib/3.0'}


def get_filetype():
    """Determine the appropriate file type for your operating system."""
    p = platform.platform(terse=True)
    if 'Windows' in p:
        return 'exe'
    elif 'Linux' in p:
        return 'tarball'
    elif 'Darwin' in p:
        return 'zipball'  # i think... do Macs do .zip?
    else:
        return 'tarball'  # most things can open tarballs


def has_update():
    http = urllib3.PoolManager(headers=AGENT)
    versions = http.request('GET',
                            "https://api.github.com/repos/mishaturnbull/"
                            "PySpeedTest/releases")
    data = json.loads(versions.data)
    latest_version = data[0]['tag_name']
    return is_version_greater(latest_version, __version__)


def get_download_url(filetype):
    if filetype not in ['exe', 'zipball', 'tarball']:
        raise ValueError("I don't know where to download a {}".format(
            filetype))
    http = urllib3.PoolManager(headers=AGENT)
    versions = http.request('GET',
                            "https://api.github.com/repos/mishaturnbull/"
                            "PySpeedTest/releases")
    data = json.loads(versions.data)

    if filetype == 'exe':
        url = data[0]['assets'][0]['browser_download_url']
    elif filetype == 'tarball':
        url = data[0]['tarball_url']
    elif filetype == 'zipball':
        url = data[0]['zipball_url']
    return url


# this is shamefully stolen from:
# https://stackoverflow.com/a/27389016/4612410
# because I don't know how to use urllib3
def download_file(url):
    local_filename = url.split('/')[-1]
    http = urllib3.PoolManager(headers=AGENT)
    with http.request('GET', url, preload_content=False) as r:
        with open(local_filename, 'wb') as out_file:
            shutil.copyfileobj(r, out_file)
    return local_filename


def download_update():
    download_file(get_download_url(get_filetype()))
    # remove the config file, and allow the new version to extract its new
    # default.  resolves #17
    os.remove('config.ini')
