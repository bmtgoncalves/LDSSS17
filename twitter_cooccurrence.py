import twitter
from twitter_accounts import accounts
import networkx as NX
import itertools

app = accounts["social"]

auth = twitter.oauth.OAuth(app["token"], 
                           app["token_secret"], 
                           app["api_key"], 
                           app["api_secret"])

stream_api = twitter.TwitterStream(auth=auth)

query = "music"

stream_results = stream_api.statuses.filter(track = query)

G = NX.Graph()

try:
    for tweet in stream_results:
    
        if len(tweet["entities"]["hashtags"]) > 1:
            tags = set([tag["text"].lower() for tag in tweet["entities"]["hashtags"]])
            G.add_edges_from(itertools.combinations(tags, 2))
            print(tags)
except KeyboardInterrupt:
    pass

print("Found", G.number_of_nodes(), "#tags")
print("\n".join(G.nodes()))