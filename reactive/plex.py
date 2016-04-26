import urllib.request
import subprocess
import os

from charmhelpers.core.hookenv import (
    status_set,
    open_port,
    relation_get,
)

from charmhelpers.core.host import (
    fstab_add,
    fstab_remove,
    mount,
    umount,
)

from charmhelpers.fetch import apt_install
from charms.reactive import when, when_not, hook
from charms.reactive import set_state, remove_state


@hook('install', 'upgrade-charm')
def install():
    # Automatically grab the latest version
    url = 'https://plex.tv/downloads/latest/1?channel=16&build=linux-ubuntu-x86_64&distro=ubuntu'
    status_set('maintenance', 'Downloading Plex Media Server...')
    urllib.request.urlretrieve(url, filename='/tmp/plexmediaserver.deb')
    status_set('maintenance', 'Installing Plex Media Server...')
    subprocess.check_call(['dpkg', '-i', '/tmp/plexmediaserver.deb'])

    os.remove('/tmp/plexmediaserver.deb')

    # Open port 32400
    status_set('maintenance', 'Opening port 32400')
    open_port(32400)
    status_set('active', 'Ready!')

@when('downloads.joined')
def install_nfs():
        os.mkdir('/mnt/plex')
        apt_install('nfs-common')

@when('downloads.changed')
def update_nfs():
    rhost = relation_get('private-address')
    mpath = relation_get('mountpath')
    if len(mpath):
        umount('/mnt/plex/')
        fstab_remove('/mnt/plex')

        fstab_add(
            '{}:{}'.format(rhost, mpath),
            '/mnt/plex',
            'nfs rw'
        )
        mount()
