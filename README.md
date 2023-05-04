# python-mysql-backupper

This Python script creates a backup of a MySQL database and posts a message about the backup process to a Slack channel. It also sets up a Sentry instance to capture and report any exceptions that occur during the backup process.

## Dependencies
* Python 3.5 or higher
* `json` module
* `os` module
* `subprocess` module
* `datetime` module
* `time` module
* `requests` module
* `yaml` module
* `sentry_sdk` module

## Configuration

The script requires a configuration file named `config.yml` which should be located in the same directory as the script. The `config.yml` file should have the following structure:
```
slack:
  token: <SLACK_API_TOKEN>
  channel: <SLACK_CHANNEL_NAME>

mysql:
  host: <MYSQL_HOST>
  user: <MYSQL_USER>
  passwd: <MYSQL_PASSWORD>
  database: <MYSQL_DATABASE_NAME>

sentry:
  dsn: <SENTRY_DSN>

name: <DATABASE_NAME>
```

* `SLACK_API_TOKEN`: The Slack API token for the bot.
* `SLACK_CHANNEL_NAME`: The name of the Slack channel where the backup process messages should be posted.
* `MYSQL_HOST`: The host name of the MySQL server.
* `MYSQL_USER`: The username for the MySQL account.
* `MYSQL_PASSWORD`: The password for the MySQL account.
* `MYSQL_DATABASE_NAME`: The name of the MySQL database to be backed up.
* `SENTRY_DSN`: The DSN (Data Source Name) for the Sentry instance. If no DSN is specified, Sentry will not be initialized.
* `DATABASE_NAME`: The name of the database.

## Usage

To use the script, simply run it using Python 3.5 or higher:
```
python main.py
```

The script will create a backup file of the specified MySQL database and post a message to the specified Slack channel when the backup is complete. The message will include the size of the backup file. The script will also check if the backup file exists and report any errors.

Note that the script uses the `mysqldump` command to create the backup file. Ensure that the `mysqldump` command is available in the system path before running the script.

## Sentry

The script uses Sentry to capture and report any exceptions that occur during the backup process. If the `SENTRY_DSN` configuration variable is not specified, Sentry will not be initialized.

## Slack

The `post_to_slack()` function in the script is responsible for posting messages to a Slack channel. It uses the Slack API to post the message. The `SLACK_API_TOKEN` configuration variable should be set to the API token for the bot. The `SLACK_CHANNEL_NAME` configuration variable should be set to the name of the channel where the message should be posted.
