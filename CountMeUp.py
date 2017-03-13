''' Main Scenario executes as requested'''

import numpy as np
import requests
import json


host = "http://localhost:5000"


class VotingMachine:
    def __init__(self):
        self._candidate1 = 0
        self._candidate2 = 0
        self._candidate3 = 0
        self._candidate4 = 0
        self._candidate5 = 0
        
    def candidate1(self):
        self._candidate1 += 1

    def candidate2(self):
        self._candidate2 += 1
        
    def candidate3(self):
        self._candidate3 += 1
        
    def candidate4(self):
        self._candidate4 += 1
        
    def candidate5(self):
        self._candidate5 += 1
    
    def vote_for(self, candidate):
        if vote == 'candidate1':
            self.candidate1()
        elif vote == 'candidate2':
            self.candidate2()
        elif vote == 'candidate3':
            self.candidate3()
        elif vote == 'candidate4':
            self.candidate4()
        elif vote == 'candidate5':
            self.candidate5()
            
    def get_votes_for(self, candidate):
        if vote == 'candidate1':
            return self._candidate1
        elif vote == 'candidate2':
            return self._candidate2
        elif vote == 'candidate3':
            return self._candidate3
        elif vote == 'candidate4':
            return self._candidate4
        elif vote == 'candidate5':
            return self._candidate5

# method used first to see the counting of votes for each candidate.
##    def result(self):
##        return("Candidate-1: " + str(self._candidate1) + "\n" + "Candidate-2: " + str(self._candidate2) + "\n" + "Candidate-3: " + str(self._candidate3) + "\n" + "Candidate-4: " + str(self._candidate4) + "\n" + "Candidate-5: " + str(self._candidate5)) 


    def __repr__(self):
        return(self.result())

voteChoice = VotingMachine()

totalOfVotes = 10000000

# for variation divide by a non integer 3.5 
userCount = int(totalOfVotes * 1.5)
users = list(range(0,userCount))

response = requests.get(host + "/api/candidates")
candidates = json.loads(response.text) # ["candidate1","candidate2","candidate3","candidate4","candidate5"]

# the only solution that I found was to put this votes limit
limitOfVotes = {
    "candidate1": int(500000),
    "candidate2": int(1000000),
    "candidate3": int(2000000),
    "candidate4": int(2000000),
    "candidate5": int(3000000)
}

while len(candidates):
    vote = np.random.choice(candidates, 1)[0]
    user = np.random.choice(users, 1)[0]
    print("user", user, "voted for", vote)
    if voteChoice.get_votes_for(vote) == limitOfVotes[vote]:    # Test if a candidate has reached the expected amount of votes
        candidates.remove(vote) # Remove it from the list, no more votes for him
        continue
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(host + "/api/vote", data=json.dumps({"user": str(user), "votedFor": str(vote)}), headers=headers)
    if response.text == 'True': # It was valid
        voteChoice.vote_for(vote)   # So sum up to control here
        print("Valid")
    else:
        print("Invalid")


