# `history`

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
   
 2. Let the script prompt for the MySQL userid and password

### Options

| Option | Description | Default |
| ------ | ----------- | ------- |
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

## Applications
Once the history is in the database, there are a lot of things you can do with it.

### Who have I played _the most often_?
```
> select user_name, count(*) from history group by user_name order BY count(*) DESC
 1 sht10                             349
 2 ~~Princess~~                      325
 3 Steve in NY                       303
 4 Hedonist - Alain                  269
 5 Nucifer                           249
 6 Don                               241
 7 joanie                            230
 8 mike                              228
 9 Trina                             227
10 Gregory                           206
11 Dave                              191
12 ...CASINO DEALER...               186
13 Joshua                            172
14 carouselhorse                     169
15 moose 3:O)                        165
16 codeslave                         163
17 Melissa                           161
18 Kerry                             158
19 Maid Marian                       156
20 Rebecca                           154
21 urantian                          146
22 Andy                              144
23 LIL RHODI GAL                     142
24 Paul                              136
25 Karen                             133
```

### Is there an advantage to who moves first?
Sometimes I hear that a player has an advantage if they move first or second, especially with reversi/othello.  Honestly I've never really seen that and don't even remember who is supposed to have an advantage.  But I can look at my history:

```
SELECT game_name, winloss, color, count(*) FROM `history` WHERE game_name like '%reversi%' group by game_name, winloss, color
```
| Game | Win/loss | Color | Count |
| - | - | - | - |
| Anti-Reversi | Loss | black | 6 |
| Anti-Reversi | Win | white | 6 |
| Anti-Reversi (10x10) | Loss | black | 6 |
| Anti-Reversi (10x10) | Win | black | 6 |
| Reversi | Draw | black | 168 |
| Reversi | Draw | white | 213 |
| Reversi | Loss | black | 1439 |
| Reversi | Loss | white | 1485 |
| Reversi | Win | black | 1796 |
| Reversi | Win | white | 1753 |
| Reversi 10x10 | Draw | black | 45 |
| Reversi 10x10 | Draw | white | 42 |
| Reversi 10x10 | Loss | black | 1016 |
| Reversi 10x10 | Loss | white | 783 |
| Reversi 10x10 | Win | black | 1954 |
| Reversi 10x10 | Win | white | 1582 |
| Reversi 6x6 | Loss | black | 18 |
| Reversi 6x6 | Loss | white | 21 |
| Reversi 6x6 | Win | black | 21 |
| Reversi 6x6 | Win | white | 15 |
| Reversi Blackhole | Draw | white | 9 |
| Reversi Blackhole | Loss | black | 804 |
| Reversi Blackhole | Loss | white | 770 |
| Reversi Blackhole | Win | black | 1494 |
| Reversi Blackhole | Win | white | 1322 |
| Reversi Blackhole (10x10) | Draw | white | 6 |
| Reversi Blackhole (10x10) | Loss | black | 588 |
| Reversi Blackhole (10x10) | Loss | white | 352 |
| Reversi Blackhole (10x10) | Win | black | 1388 |
| Reversi Blackhole (10x10) | Win | white | 969 |

I've won much more often when I played black.  Shockingly, I don't even remember which color moves first!  That's what IYT is for!  FWIW, black moves first so it seems like I have an advantage when I move first.

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
