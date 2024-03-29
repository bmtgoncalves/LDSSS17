import twitter
from twitter_accounts import accounts
import networkx as NX

app = accounts["social"]

auth = twitter.oauth.OAuth(app["token"], 
                           app["token_secret"], 
                           app["api_key"], 
                           app["api_secret"])

twitter_api = twitter.Twitter(auth=auth)

screen_name = "BarackObama"

args = { "count" : 200,
         "trim_user": "true",
         "include_rts": "true"}

tweets = twitter_api.statuses.user_timeline(screen_name=screen_name, **args)

tweets_new = tweets

while len(tweets_new) > 0:
    max_id = tweets[-1]["id"] - 1
    tweets_new = twitter_api.statuses.user_timeline(screen_name=screen_name, max_id=max_id, **args)
    tweets += tweets_new

user = tweets[0]["user"]["id"]
G = NX.DiGraph()

for tweet in tweets:
    if "retweeted_status" in tweet:
        G.add_edge(tweet["retweeted_status"]["user"]["id"], user)
    elif tweet["in_reply_to_user_id"]:
        G.add_edge(user, tweet["in_reply_to_user_id"])

print("Graph has", G.number_of_nodes(), "nodes,",\
                   G.number_of_edges(), "edges, and the maximum degree is",\
                   max(G.degree().values()))