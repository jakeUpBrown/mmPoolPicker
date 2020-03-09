import os
import json

from pool_simulator.utils.FilePathConstants import FilePathConstants

def generatePicks():

    picks = json.loads('{}')

    with open(os.path.abspath(FilePathConstants.get_data_file("2018-picks-list.csv")), "r") as infile:
        for aline in infile:
            items = aline.rstrip().split(',')

            pickObj = json.loads('{}')
            pickObj['name'] = items[1]
            pickObj['userId'] = items[2]
            pickObj['picks'] = items[3:]

            picks[items[2]] = pickObj

    with open(os.path.abspath(FilePathConstants.get_output_file("2018-picks.json")), "w") as outfile:
        outfile.write(json.dumps(picks, indent=2))



def generateUsers():
    users = json.loads('{}')

    with open(os.path.abspath(FilePathConstants.get_data_file("users-list.csv")), "r") as infile:
        for aline in infile:
            items = aline.rstrip().split(',')

            userObj = json.loads('{}')
            userObj['name'] = items[0]
            userObj['userId'] = items[1]

            users[items[1]] = userObj

    with open(os.path.abspath(FilePathConstants.get_output_file("users.json")), "w") as outfile:
        outfile.write(json.dumps(users, indent=2))


generatePicks()
generateUsers()