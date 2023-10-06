#!/usr/bin/python3
"""
Distributes an archive to your web servers,
using the function do_deploy
"""
import os
from fabric.api import task, local, run, env, put
from datetime import datetime


env.hosts = ['52.91.117.92',
             '100.25.111.11']


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


@task
def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not os.path.exists(archive_path):
        return False
    filename_ext = os.path.basename(archive_path)
    filename = os.path.splitext(filename_ext)
    dir_path = "/data/web_static/releases/"

    put(archive_path, "/tmp/")
    run("rm -rf {}{}/".format(dir_path, filename))
    run("mkdir -p {}{}".format(dir_path, filename))
    run("tat -xzf /tmp/{} -C {}{}".format(filename_ext,
                                          dir_path, filename))
    run("rm -rf /tmp/{}".format(filename_ext))
    run("mv {0}{1}/web_static/* {0}{1}/".format(dir_path,
                                                filename))
    run("rm -rf {}{}/web_static".format(dir_path, filename))
    run("rm -rf /data/web_static/current")
    run("ln -s {}{}/ /data/web_static/current".format(dir_path,
                                                      filename))
    print("New version deployed!")
    return True
