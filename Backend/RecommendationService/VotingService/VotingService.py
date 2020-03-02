#!flask/bin/python
from flask import Flask
import Backend.RecommendationService.ClusteringService.clustering as cl

app = Flask(__name__)


@app.route('/')
@app.route('/upvote/')
def index():
    cl.writeVotingResult(vote = "up")
    return "You have just successfully executed the Upvoting Service!"


@app.route('/downvoting/')
def index2():
    cl.writeVotingResult(vote = "down")
    return "You have just successfully executed the Downvoting Service!"

if __name__ == '__main__':
    app.run(debug=True, port=5010)
