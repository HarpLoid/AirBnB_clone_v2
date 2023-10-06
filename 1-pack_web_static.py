#!/usr/bin/python3
"""
Generates a .tgz archive from the contents of the web_static folder
of your AirBnB Clone repo, using the function do_pack.
"""
from fabric.api import task, local
from datetime import datetime


@task
def do_pack():
    """
    creates a .tgz archive from the contents of the web_static folder
    """
    fmt_date = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    folder = "web_static"
    archive_name = "versions/{}_{}.tgz".format(folder, fmt_date)
    command = "mkdir -p versions"

    print("Packing {} to {}".format(folder, archive_name))

    if local("{} && tar -cvzf {} {}"
             .format(command, archive_name, folder)).succeeded:
        return archive_name

    return None
