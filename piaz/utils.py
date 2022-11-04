import ipaddress
from pathlib import Path
from urllib.parse import urlparse

from jinja2 import Template


def parse_remote(rhostport):
    """
    parses the given rhostport variable, looking like this:
            [username[:password]@]host[:port]
    if only host is given, can be a hostname, IPv4/v6 address or a ssh alias
    from ~/.ssh/config
    and returns a tuple (username, password, port, host)
    """
    # leave use of default port to ssh command to prevent overwriting
    # ports configured in ~/.ssh/config when no port is given
    if rhostport is None or len(rhostport) == 0:
        return None, None, None, None
    port = None
    username = None
    password = None
    host = rhostport

    if "@" in host:
        # split username (and possible password) from the host[:port]
        username, host = host.rsplit("@", 1)
        # Fix #410 bad username error detect
        if ":" in username:
            # this will even allow for the username to be empty
            username, password = username.split(":")

    if ":" in host:
        # IPv6 address and/or got a port specified

        # If it is an IPv6 address with port specification,
        # then it will look like: [::1]:22

        try:
            # try to parse host as an IP address,
            # if that works it is an IPv6 address
            host = str(ipaddress.ip_address(host))
        except ValueError:
            # if that fails parse as URL to get the port
            parsed = urlparse('//{}'.format(host))
            try:
                host = str(ipaddress.ip_address(parsed.hostname))
            except ValueError:
                # else if both fails, we have a hostname with port
                host = parsed.hostname
            port = parsed.port

    if password is None or len(password) == 0:
        password = None

    return username, password, port, host


def render_template(name, **kwargs):
    with open(Path(__file__).parent / 'templates' / name) as file_:
        template = Template(file_.read())
    print(f"Rendering template {name}")
    return template.render(**kwargs)
