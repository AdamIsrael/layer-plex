# Introduction

Plex is a media player that works wherever you are.

This charm makes it easy to deploy a Plex server.

# Barebones instructions:

- Deploy charm
- Browse to https://ip:32400/web
- Signin to your plex account
- Make sure server is remotely accessible (see firewall info below)

# Firewall/Routing
You'll need to route traffic from your local machine to the Plex container.
There isn't an automated way of doing this (yet), so I've resorted to creating
a bash script to run the routing commands manually.

Note: this should be rewritten to loop through an array of ports to be opened.

```bash
#####################
# Plex Media Server #
#####################
PLEX_IP=10.0.3.22
iptables -t nat -A PREROUTING -p tcp -m tcp --dport 32400 -j DNAT --to-destination $PLEX_IP:32400

# Plex Companion
iptables -t nat -A PREROUTING -p tcp -m tcp --dport 3005 -j DNAT --to-destination $PLEX_IP:3005

# Roku
iptables -t nat -A PREROUTING -p tcp -m tcp --dport 8324 -j DNAT --to-destination $PLEX_IP:8324

# Plex DNLA server
iptables -t nat -A PREROUTING -p tcp -m tcp --dport 32469 -j DNAT --to-destination $PLEX_IP:32469
iptables -t nat -A PREROUTING -p udp -m udp --dport 1900 -j DNAT --to-destination $PLEX_IP:1900

# For bonjour/avahi
iptables -t nat -A PREROUTING -p udp -m udp --dport 5353 -j DNAT --to-destination $PLEX_IP:5353

# GDM network discovery
iptables -t nat -A PREROUTING -p udp -m udp --dport 32410 -j DNAT --to-destination $PLEX_IP:32410
iptables -t nat -A PREROUTING -p udp -m udp --dport 32412 -j DNAT --to-destination $PLEX_IP:32412
iptables -t nat -A PREROUTING -p udp -m udp --dport 32413 -j DNAT --to-destination $PLEX_IP:32413
iptables -t nat -A PREROUTING -p udp -m udp --dport 32414 -j DNAT --to-destination $PLEX_IP:32414

# Plex DLNA (discoverability)
iptables -t nat -A PREROUTING -p tcp -m tcp --dport 32469 -j DNAT --to-destination $PLEX_IP:32469
iptables -t nat -A PREROUTING -p udp -m udp --dport 32469 -j DNAT --to-destination $PLEX_IP:32469
```

# NFS

TODO: Fully document this. And make it easier.

NFS allows you to share media across multiple servers. Work needs to be done
to automate this process. Right now, you'll need to `juju ssh` to the Plex unit
and manually configure `/etc/fstab` with your nfs mount point(s).


# Upgrading
Simply run `juju upgrade-charm plex` and the charm will automatically download
and install the latest version of Plex.

# Contact
Maintained by Adam Israel - adam@adamisrael.com
[Bug reports](https://github.com/AdamIsrael/plex/issues) and
[pull requests](https://github.com/AdamIsrael/plex/pulls) welcome!
