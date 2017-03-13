from flask import Flask, request, render_template, jsonify, g, send_file, redirect, url_for
import pymongo
import json
import datetime

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


class Database:
    conn = pymongo.MongoClient()
    _cache = None

    @classmethod
    def connect(cls, database_name):
        cls._cache = cls.conn[database_name]
        return cls._cache

    @classmethod
    def get(cls):
        return cls._cache

Database.connect("project")


# Get all votes
@app.route("/api/vote", methods=['GET'])
def get_votes():
    # return cursor to votes
    entries = Database.get().votes.find()
    # fetch all data from cursor to list
    entries = list(entries)
    # dump into json and send as string
    response = str(json.dumps(entries))
    return response, 200


@app.route("/api/candidates", methods=['GET'])
def get_candidates():
    return str(json.dumps(["candidate1", "candidate2", "candidate3", "candidate4", "candidate5"]))
    
    
# Post a vote
@app.route("/api/vote", methods=['POST'])
def post_votes():
    try:
        data = request.get_json()
    except Exception as e:
        print(str(e))
        return "Not a json", 400

    voted_for = data.get("votedFor")
    user = data.get("user")

    if voted_for is None or user is None:
        return "Invalid arguments", 400
    elif voted_for not in ["candidate1", "candidate2", "candidate3", "candidate4", "candidate5"]:
        return "Invalid Canditate", 400

    # fetch the first match from the returned cursor into entry
    entry = Database.get().users.find_one({"user": user}, {"_id": False})
    if entry is None:
        entry = {}
    count_votes = entry.get("countVotes", 0)
    count_votes += 1
    is_valid = not (count_votes > 3)

    Database.get().votes.insert({
        "votedFor": voted_for,
        "user": user,
        "timestamp": datetime.datetime.now().timestamp(),
        "isValid": is_valid
    })

    Database.get().users.update({"user": user}, {
        "$set": {
            "countVotes": count_votes
        }
    }, upsert=True)

    return str(is_valid), 200


# Get all valid votes
@app.route("/api/vote/calculate", methods=['GET'])
def get_votes_calculates():
    entries = Database.get().votes.aggregate([
        {"$match": {"isValid": True}},
        {
            "$group": {
                "_id": "$votedFor",
                "votes": {"$sum": 1}
            }
        }
    ])
    entries = list(entries)

    total = 0
    for entry in entries:
        total += entry["votes"]

    response = {
        "candidates": entries,
        "total": total
    }
    response = str(json.dumps(response))
    return response, 200

# Delete Database
@app.route("/api/vote", methods=["DELETE"])
def delete_votes():
    Database().get().votes.remove({"_id": {"$exists": True}})
    Database().get().user.remove({"_id": {"$exists": True}})
    return "Ok", 200


@app.route("/", methods=["GET"])
def get_front_end():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(threaded=True, debug=True)