# `history`

Imports IYT game history into a MySQL database

The game history should have been created with the [`history`](history.md) script.


## Usage

## Requirements

###

The script works best on a Unix system or a Unix-like environment such as [Cygwin](https://www.cygwin.com/) on Windoze.

### Credentials

MySQL credentials are stored in a secure store called `iyt` and are managed by my `SecureKeyValues.py` tool (see the `Credentials` section of [`history`](history.md) for more information).  The following steps assumes that you've already downloaded the `SecureKeyValues.py`.



### Options

| Option | Description | Default |
| ------ | ----------- | ------- |
| `-S` or `--server` | MySQL server | The option is required and there is no default |
| `-u` or `--user` | MySQL user | The option is required and there is no default |
| `-d` or `--database` | MySQL database | The default is `iyt`. |
| `-v` or `--version` | Enables more debugging.  One instance of the option enable `INFO` messages.  Two instances enable `DEBUG` messages.  | The default is to display `WARNING`, `ERROR`, and `CRITICAL` messages |

## Examples

```
$ ./history2mysql -vv -S mrbruno.org -d mrbrunoo_iyt -f /home/mrbruno/tmp/iyt-history.csv
2019-03-30 21:12:02,321 DEBUG /home/mrbruno/repos/iyt/history2mysql:17 dynaload Fetching https://raw.githubusercontent.com/https://raw.githubusercontent.com/pfuntner/toys/master/bin/SecureKeyValues.py
2019-03-30 21:12:17,500 DEBUG /home/mrbruno/repos/iyt/history2mysql:55 <module> Obtained secure key/values
2019-03-30 21:12:17,606 INFO /home/mrbruno/repos/iyt/history2mysql:59 <module> Loaded 54917 games
2019-03-30 21:12:17,606 INFO /home/mrbruno/repos/iyt/history2mysql:63 <module> Connecting to mrbrunoo_root@mrbruno.org
2019-03-30 21:12:23,106 DEBUG /home/mrbruno/repos/iyt/history2mysql:73 <module> Connected to mysql
2019-03-30 21:12:24,484 DEBUG /home/mrbruno/repos/iyt/history2mysql:95 <module> Executing insert
2019-03-30 21:12:26,066 DEBUG /home/mrbruno/repos/iyt/history2mysql:101 <module> Executed insert
2019-03-30 21:12:26,165 INFO /home/mrbruno/repos/iyt/history2mysql:105 <module> Changes committed, 54916 games were added
$
```

## Notes

- The script requires the `mysql-connector` Python package to interface with MySQL
- The script assumes a table called `history` created with a schema such as:

    ```
    CREATE TABLE history (
        category varchar(16) NOT NULL,
        game_name varchar(32) NOT NULL,
        user_id int(11) NOT NULL,
        user_name varchar(64) NOT NULL,
        game_id int(11) NOT NULL,
        winloss varchar(8) NOT NULL,
        moves int(11) NOT NULL,
        color varchar(16) NOT NULL,
        end_datetime datetime NOT NULL
    ); 
    ```
 - I've used the script to upload 55,000 games and it only takes about 2 seconds to do the update.  A single SQL `INSERT` is formed and my statement was about 6.5MB.