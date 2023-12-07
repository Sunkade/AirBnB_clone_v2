#!/usr/bin/python3
"""
Fabric script for creating and distributing an archive to web servers.

Usage: fab -f deploy_script.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['100.27.14.93', '54.162.87.128']


def create_archive():
    """Generates a tgz archive."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir versions")
        archive_name = f"versions/web_static_{date}.tgz"
        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except Exception as e:
        print(f"Error creating archive: {e}")
        return None


def deploy_archive(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        print(f"Archive not found: {archive_path}")
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        base_name = archive_name.split(".")[0]
        remote_path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')
        run(f'mkdir -p {remote_path}{base_name}/')
        run(f'tar -xzf /tmp/{archive_name} -C {remote_path}{base_name}/')
        run(f'rm /tmp/{archive_name}')
        run(f'mv {remote_path}{base_name}/web_static/* {remote_path}{base_name}/')
        run(f'rm -rf {remote_path}{base_name}/web_static')
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s {remote_path}{base_name}/ /data/web_static/current')
        return True
    except Exception as e:
        print(f"Error deploying archive: {e}")
        return False


def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = create_archive()
    if archive_path:
        return deploy_archive(archive_path)
    else:
        return False

