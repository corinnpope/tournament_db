# Swiss Pairings in SQL

## Introduction

> No one likes to end their tournament play after their first loss. This swiss pairings style tournament generator will allow all players or teams play the same number of matches – while ensuring that teams and players are appropriately matched and one player or team emerges victorious. 

This project was built to meet the following requirements:
- The module passes the included unit tests.
- Tables have meaningful names.
- Tables are normalized (no redundant data, data dependancies are properly defined).
- Table columns have proper data types.
- Table columns have meaningful names.
- Primary and secondary keys are properly defined.
- Code makes use of query parameters to protect against SQL injection.
- Code is ready for personal review and is neatly formatted.
- Comments are present and effectively explain longer code procedures.
- A README file is included detailing all steps required to successfully run the application.

## Code Samples

> This project uses SQL to pair up users and views to make pairing easier for the user

This project uses view...such as a standings view where users can easily see who is in the lead

    CREATE VIEW standings AS
    SELECT players.id AS id, players.name AS name,
    (SELECT count(*) FROM matches WHERE matches.winner = players.id) AS wins,
    (SELECT count(*) FROM matches WHERE players.id in (winner, loser)) AS matches
    FROM players GROUP BY players.id ORDER BY wins DESC;

and a simple way of pairing up players 

    def swissPairings():    
    standings = playerStandings()
    # empty array for pairings
    swiss_pairings = []

    # for each set of pairs **range([start], stop[, step])**
    for i in range(0, countPlayers(), 2):
        # pair up the players who have the same ranking (next to one another)
        # [0] is id, [1] is name, [i] is first player in range,
        # [i+1] is 2nd player in range
        new_matches = (
            standings[i][0], standings[i][1],
            standings[i+1][0], standings[i+1][1]
            )
        swiss_pairings.append(new_matches)

    # return a list of pairings (id1, name1, id2, name2)
    return swiss_pairings

## Installation

> The installation instructions are low priority in the readme and should come at the bottom. The first part answers all their objections and now that they want to use it, show them how.

1. If you do not already have Vagrant and VirtualBox, install them from the links below:
  * Install Vagrant from https://www.vagrantup.com/
  * Install VirtualBox from https://www.virtualbox.org/
2. Clone this repo to your local machine & cd to  the directory of the cloned repo
3. Run `vagrant up` to get your virtual machine up and running and `vagrant ssh` to connect
4. Change directories to the "tournament" directory
5. run `psql` to open the postgreSQL command prompt
6. run `\i tournament.sql` to create the database and tables
7. run `'\c` to connect

From here you can run `python tournament_test.py` to check to see if the code passes the unit tests. 
