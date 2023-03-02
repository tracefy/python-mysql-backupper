import json
import os
import subprocess
import datetime
from time import sleep

import requests
import yaml
import sentry_sdk

config = yaml.safe_load(open(os.path.dirname(__file__) + '/config.yml'))


def post_to_slack(text, channel, blocks=None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': config['slack']['token'],
        'channel': channel,
        'text': text,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()


def setup_sentry():
    sentry_dsn = config['sentry']['dsn'],
    if sentry_dsn:
        sentry_sdk.init(
            str(sentry_dsn),
            traces_sample_rate=1.0,
        )
    else:
        print("No sentry DSN configured")


def create_backup(backup_file):
    if os.path.exists(backup_file):
        os.remove(backup_file)
    else:
        print("Can not delete the file as it doesn't exists")

    cmd = "mysqldump -h {host} -u {user} -p {dbname} --password={pswd} --no-tablespaces | gzip -c > {backup_file} ".format(
        backup_file=backup_file,
        user=config['mysql']['user'],
        host=config['mysql']['host'],
        pswd=config['mysql']['passwd'],
        dbname=config['mysql']['database'],
    )
    print(cmd)

    subprocess.Popen(cmd, shell=True)

    print("Backup file created: %s" % backup_file)


def get_file_name(current_path):
    return "{path}/backups/{hour}.gz".format(
        path=str(current_path),
        hour=datetime.datetime.now().hour
    )


if __name__ == '__main__':
    post_to_slack(':terminator-abbo: Start backup for {name}'.format(
        name=config['name']
    ), config['slack']['channel'])
    current_path = os.path.dirname(__file__)

    backup_file = get_file_name(current_path)
    create_backup(backup_file)

    sleep(10)
    print("Checking if backup file exists")
    file_size = os.path.getsize(backup_file) / (1024 * 1024)
    post_to_slack(':terminator-abbo: Created a backup with size {file_size} mb for {name}'.format(
        name=config['name'],
        file_size=format(file_size, ".2f")),
        config['slack']['channel'])
