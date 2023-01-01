# `history2mysql`

Imports IYT game history into a MySQL database

The game history should have been created with the [`history`](history.md) script.


## Usage

## Requirements

###

The script works best on a Unix system or a Unix-like environment such as [Cygwin](https://www.cygwin.com/) on Windoze.

### Credentials

The script needs the userid and password to the MySQL database you're using.  You have two choices:

1. Save the information in a _secure store_ just like `history`.

   - Secure store name: `mysql`
   - Userid key: _`{SERVER_NAME}`_/_`{DATABASE_NAME}`_/`user`
   - Password key: _`{SERVER_NAME}`_/_`{DATABASE_NAME}`_/`password`

   See that script for tips on setting up the secure store for `history2mysql`
   
 2. Specify the userid via the `--user` option on the command line and let the script prompt for the password

### Options

| Option | Description | Default |
| - | - | - |
| `-S` or `--server` | MySQL server | The option is required and there is no default |
| `-u` or `--user` | MySQL user if the script should not look in the secure store.  The script will prompt for the password but will not echo what you write to the screen. | There is no default but if you specify `--user`, the secure store will be ignored |
| `-d` or `--database` | MySQL database | The default is `iyt`. |
| `-f` or `--file` | Option to provide IYT history file.  Alternatively, you can redirect the file to stdin | There is no default but you have to use one of the methods.  If you **do** specify `--file`, the script ignores stdin |
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

Note: I'm using the MySQL server that my web hosting company provides and they prefixe MySQL users and databases with the host company user (`mrbrunoo` for `mrbruno.org` in my case) so that's why I had to override the database name.  Otherwise, I probably would have just used the default name `iyt`.

## Applications
Once the history is in the database, there are a lot of things you can do with it.  I started to add examples of applications the database here but it was becoming very cluttered.  Check out [these posts](http://itsyourturn.freeforums.net/board/4/sql-queries).  If you find some good queries, feel free to contribute!

## Notes

- The script requires the `mysql-connector` Python package to interface with MySQL
- A sort of companion to this script is [`pmysql`](https://github.com/pfuntner/toys/blob/master/bin/pmysql) - there's no help page for it... yet!  I plan to put some examples in the [IYT SQL queries message board](http://itsyourturn.freeforums.net/board/4/sql-queries)
- The script assumes a table called `history` created with a schema such as:

    ```
    CREATE TABLE history (
        category varchar(16) NOT NULL,
        game_name varchar(32) NOT NULL,
        user_id bigint(11) NOT NULL,
        user_name varchar(64) NOT NULL,
        game_id bigint(11) NOT NULL,
        winloss varchar(8) NOT NULL,
        moves int(11) NOT NULL,
        color varchar(16) NOT NULL,
        end_datetime datetime NOT NULL
    ); 
    ```
    
 - I've used the script to upload 55,000 games and it only takes about 2 seconds to do the update.  A single SQL `INSERT` is formed and my statement was about 6.5MB.
