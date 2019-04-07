# `history`

Collects IYT game history

The script:
  1. Logs into IYT
  2. Opens the game status page to learn the user's IYT user id
  3. Opens the user's _user profile_
  4. For Regular, Tournament, and Ladder games:  
     1. For the wins, losses, and draws for each game:
        1. Opens all summary pages and collects information about each game: opponent, win/loss, etc.

## Isn't this already available?
Well, yes... the tool actually just parses information off the normal pages on the site.  It doesn't do anything that you can't do but the script does a thorough job much easier and without human error or frustration.

There are basically two choices for history on IYT:
  1. Recently completed games.  This is very useful but still can be awkward for some purposes
    1. It's just a snapshot of recent games
    2. It's not easy collate the games for various purposes.  How about all your games against a specific user?  You can't sort the columns and you're stuck with chronological lists that are organized by wins, losses, or draws.  When I look, I often lose my place and wonder _ok, I see this completed game from the user - was this a win or a loss?_.  No thanks!
  2. You can look at the entire history of all your games but it's organized by category (regular, tournament, ladder), type of game, and win/loss/draw.  Plus, there can be up to ten pages for a particular category, type of game, and outcome.
 
The script uses the second method of looking at your entire history but automates navigation through the pages and collection of the information.  I'm a strong believer that computers are meant to make things easier for people!
 
Bottom line, the tool is useful to me, it makes sense to me, and I will use it.  If others find it useful, great.  If you don't find a use for it, that's cool too.

## Usage

## Requirements

### Unix-y Environment

The script works best on a Unix system or a Unix-like environment such as [Cygwin](https://www.cygwin.com/) on Windoze.  I imagine it will work well from Mac machines since Mac OS X is a Unix OS.  It might just use a little more TLC to get working on a Windoze machine that doesn't have Python or a decent command shell.

### Python Requirements

#### Python 2.7+ (pre-Python 3)

I know the script requires at least Python 2.7:

```
$ python --version
Python 2.7.15
$
```

It will not work with Python 3 but I could probably make it work with Python 3.  I usually don't have a need to use Python 3.

#### requests package

The script uses the `requests` package which does not come with Python by default.  If it's not available, you might have to install it:

```
$ pip install requests
```

### Credentials

The script must use your IYT and user and password to login to the site and collect 
rmation.  There are two choices:

1. You can have the script prompt you for the information each time you run it.
2. You can set up the userid and password in a _secure store_ so that you don't have to be prompted every time.

#### Credentials in a secure store 

I have another script to save this information to a file in a secure manner so it's not available in the clear.  The secure store is encrypted by your private ssh key and and the actual password and userid are not echoed to the screen when you type them.  Unless you're a very good on Unix, I suggest you don't try to put your credentials in a secure store.

To set up the credentials:

| Step number | Description | Command |
| - | - | - |
| 1 | Download the script.  This is part of my [toys repo](https://github.com/pfuntner/toys) but all you need is one script | `$ wget https://raw.githubusercontent.com/pfuntner/toys/master/bin/SecureKeyValues.py`<br/>`$ chmod +x SecureKeyValues.py` |
| 2 | Start the script to create a secure store | `$ ./SecureKeyValues.py --ssh --store iyt --operation set` |
| 3 | Enter the key names of the values you will enter next | `user`<br/>`password` |
| 4 | Signal the end of names of values | Press `Ctrl-D` |
| 5 | Respond to the prompt of entering the user | Type your IYT user - remember, it is not echoed to the screen |
| 6 | Respond to the prompt of entering the password | Type your IYT password - again, it is not echoed to the screen |

### Options

| Option | Description | Default |
| ------ | ----------- | ------- |
| `-u` or `--user` | Specifies your IYT user if the script should not look in the secured store.  The script will prompt for the password but will not echo what you write to the screen. | There is no default |
| `-c` or `--csv` | Renders history in [CSV (_comma separated values_) format](https://www.wikiwand.com/en/Comma-separated_values) | The default is to use this method |
| `-j` or `--json` | Renders history in [JSON format](https://www.wikiwand.com/en/JSON) | The default is to render in CSV format |
| `-v` or `--version` | Enables more debugging.  One instance of the option enable `INFO` messages.  Two instances enable `DEBUG` messages.  | The default is to display `WARNING`, `ERROR`, and `CRITICAL` messages |

## Examples

```
$ ./history | headtail
There are 54,916 total games
       1 Category,Game,GameID,User,UserID,WinLoss,Moves,Color,Date,Time
       2 Regular,Anti-Backgammon,15300064812762,Donna D,15200000663034,Win,189,white,18/12/16,16:58:00
       3 Regular,Anti-Backgammon,15300065319531,Danny Bad Boy,15200000782400,Win,31,black,18/08/28,08:53:00
       4 Regular,Anti-Backgammon,15300064893256,supermanwuvsme,15200003044703,Win,290,black,18/07/05,22:28:00
       5 Regular,Anti-Backgammon,15300064965692,pandagirl,15200003408150,Win,11,white,18/05/20,17:58:00
         .
         .
         .
   54913 Ladder,Triple Boatzee,15300058626606,Grand Poobah,15200003015255,Draw,40,black,14/08/08,17:59:00
   54914 Ladder,Triple Boatzee,15300055564644,Gingy,15200000357493,Draw,40,black,13/03/16,08:03:00
   54915 Ladder,Triple Boatzee,15300062382383,Henning,15200003362723,Draw,40,white,16/09/21,15:50:00
   54916 Ladder,Triple Boatzee,15300058626606,Grand Poobah,15200003015255,Draw,40,black,14/08/08,17:59:00
   54917 Ladder,Triple Boatzee,15300055564644,Gingy,15200000357493,Draw,40,black,13/03/16,08:03:00
$ ./history --json | json | headtail
There are 54,916 total games
       1 [
       2   {
       3     "category": "Regular", 
       4     "color": "white", 
       5     "end": {
         .
         .
         .
  988486       "name": "Gingy"
  988487     }, 
  988488     "win": false
  988489   }
  988490 ]
$ 
```

[`headtail`](https://github.com/pfuntner/toys/blob/master/doc/headtail.md) and [`json`](https://github.com/pfuntner/toys/blob/master/doc/json.md) are both tools of mine from another repository.

## Docker instructions
[Docker](https://www.docker.com/) is kind of way to start a lightweight virtual machine and if you have the luxury of having it installed and can't get the script working on your native machine, try my procedure for running the script inside a Docker container:

```
$ make
... make & docker churn for a minute or two - have a drink and come back ...
$ docker exec -it history bash -c '/tmp/history --u YOUR_IYT_USERID > /tmp/history.csv'
$ docker exec -it history cat /tmp/history.csv > history.csv
```

## Notes

- The script only collects the overall information of a game.  It does not collect information about individual moves.
- The IYT history pages may not include all your games.  For instance, I've played 1,279 Anti-Backgammon games but only the most recent 1000 are available in the history pages.  I've played a total of 55,266 games at the time of writing this page but only 39,836 (72%) are available in the history pages.  

  A familiar catch phrase in software development is: _Garbage in, Garbage out_. I only have access to 39,836 gamesI wish there was more data available but there isn't and I can't create data out of nothing.
- You will probably want to redirect stdout to a file that will store your history.
- See [`history2mysql`](history2mysql.md) for a script to load a CSV into MySQL.
- I've been able to load a CSV into a _LibreOffice Calc_ spreadsheet (that's what my Linux machine has instead of Excel).  When the file loaded, I had to make sure that it **only** used commas as a field separator.
- Depending on how many games you have, the script could take several seconds to run.  On my machine, it takes slightly less than a minute to collect the history for 54,916 games.  By enabling `INFO` messages, you will see the script progress through your history.
- IYT reports dates in `mm/dd/yy` format, which is commonly used in the USA but makes sorting very problematic.  The script normalizes the dates by using `yy/mm/dd` format, even though the year looks a little funny without the century.
- I've also written some scripts that only deal with the CSV file and those scripts can be powerful too.
