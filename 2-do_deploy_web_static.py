#!/usr/bin/python3
"""
Fabric script for deploying an archive to web servers using do_deploy function.

Usage: fab -f 2-do_deploy_web_static.py do_deploy:archive_path=<path to archive> -i <SSH private key> -u <username>
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['100.27.14.93', '54.162.87.128']
env.user = 'ubuntu'


def do_deploy(archive_path):
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
        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Error deploying archive: {e}")
        return False

