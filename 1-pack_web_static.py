#!/usr/bin/python3
"""
Generates a .tgz archive from the contents of the web_static folder
of your AirBnB Clone repo, using the function do_pack.
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    fmt_date = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    file_name = "versions/web_static_{}".format(fmt_date)
    command = "mkdir -p versions"

    if local(" {} && tar -cvzf {} webstatic"
             .format(command, file_name)).succeeded:
        return file_name

    return None
