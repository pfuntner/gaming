# `history`

Collects IYT game history

The script:
  1. Logs into IYT
  2. Opens the game status page to learn the user's IYT user id
  3. Opens the user's _user profile_
  4. For Regular, Tournament, and Ladder games:
    1. For the wins, losses, and draws for each game:
      1. Opens all summary pages and collects information about each game: opponent, win/loss, etc.

## Syntax

## Requirements

###

The script works best on a Unix system or a Unix-like environment such as [Cygwin](https://www.cygwin.com/) on Windoze.

### Credentials

The script must use your IYT and user and password to login to the site and collect information.  I have another script to save this information to a file in a secure manner so it's not available in the clear.  The secure store is encrypted by your private ssh key and and the actual password and userid are not echoed to the screen when you type them.

To set up the credentials:

| Step number | Description | Command |
| - | - | - |
| 1 | Download the script.  This is part of my [toys repo](https://github.com/pfuntner/toys) but all you need is one script | `$ wget https://raw.githubusercontent.com/pfuntner/toys/master/bin/SecureKeyValues.py > SecureKeyValues.py`<br/>`$ chmod +x SecureKeyValues.py` |
| 2 | Start the script to create a secure store | `$ ./SecureKeyValues.py --ssh --store iyt --operation set` |
| 3 | Enter the key names of the values you will enter next | `user`<br/>`password` |
| 4 | Signal the end of names of values | Press `Ctrl-D` |
| 5 | Respond to the prompt of entering the user | Type your IYT user - remember, it is not echoed to the screen |
| 6 | Respond to the prmopt of entering the password | Type your IYT password - again, it is not echoed to the screen |

### Options

| Option | Description | Default |
| ------ | ----------- | ------- |
| `-c` or `--csv` | Renders history in [CSV (_comma separated values_) format](https://www.wikiwand.com/en/Comma-separated_values) | The default is to use this method |
| `-j` or `--json` | Renders history in [JSON format](https://www.wikiwand.com/en/JSON) | The default is to render in CSV format |

## Examples

```
$ ./history | headtail
There are 54,916 total games
       1 Category,Game,GameID,User,UserID,WinLoss,Moves,Color,Date,Time
       2 Regular,Anti-Backgammon,15300064812762,Donna D,15200000663034,Win,189,white,12/16/18,16:58:00
       3 Regular,Anti-Backgammon,15300065319531,Danny Bad Boy,15200000782400,Win,31,black,08/28/18,08:53:00
       4 Regular,Anti-Backgammon,15300064893256,supermanwuvsme,15200003044703,Win,290,black,07/05/18,22:28:00
       5 Regular,Anti-Backgammon,15300064965692,pandagirl,15200003408150,Win,11,white,05/20/18,17:58:00
         .
         .
         .
   54913 Ladder,Triple Boatzee,15300058626606,Grand Poobah,15200003015255,Draw,40,black,08/08/14,17:59:00
   54914 Ladder,Triple Boatzee,15300055564644,Gingy,15200000357493,Draw,40,black,03/16/13,08:03:00
   54915 Ladder,Triple Boatzee,15300062382383,Henning,15200003362723,Draw,40,white,09/21/16,15:50:00
   54916 Ladder,Triple Boatzee,15300058626606,Grand Poobah,15200003015255,Draw,40,black,08/08/14,17:59:00
   54917 Ladder,Triple Boatzee,15300055564644,Gingy,15200000357493,Draw,40,black,03/16/13,08:03:00
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

## Notes

- The script only collects the overall infomation of a game.  It does not collect information about individual moves.
- You will probably want to redirect stdout to a file that will store your history.
- CSV might be the easiest method to use to import into a database.  One of the things on my _to do list_ is to write a tool to import the data
- The IYT history pages may not include all your games.  For instance, I've played 1,279 Anti-Backgammon games but only the most recent 1000 are available in the history pages.  I've played a total of 55,171 games at the time of writing this page but only 54,916 are avaiable in the history pages.
