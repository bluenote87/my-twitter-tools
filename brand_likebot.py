# This program depends upon twitter.com's API and sixohsix's Python Twitter Tools at the following repo: https://github.com/sixohsix/twitter
from twitter import *
import os.path

# An array of blacklisted vendor & competitor screen_names to never add to your favorites
blacklist = ["Insert", "screen_names", "of", "brands", "to", "not", "like", "here"]

# This will like any tweets liked by the screennames inserted into 'brands'
def main():
    #This app has Read and Write permissions
    MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("Your LikeBot App Name Here", consumer_key="XXXXX", consumer_secret="XXXXX",
                    token_filename=MY_TWITTER_CREDS)
    oauth_token, oauth_secret = read_token_file(filename=MY_TWITTER_CREDS)
    t = Twitter(auth=OAuth(token=oauth_token, token_secret=oauth_secret, 
    	consumer_key="XXXXX", consumer_secret="XXXXX"))

    brands = ["Screen_names", "of", "brands", "to", "like", "here"]

    for idx in range(0, len(brands)):
    
        result = t.favorites.list(screen_name = brands[idx], count=10)
    
        liked_tweets = list()

        for x in range(0, len(result)):
            flagged = False
            mentions = result[x]['entities']['user_mentions']
            for y in range(0, len(mentions)):
                if mentions[y]['screen_name'] in blacklist:
                    flagged = True
            if result[x]['in_reply_to_screen_name'] in blacklist:
                flagged = True
            if result[x]['user']['screen_name'] in blacklist:
                flagged = True
            if flagged == False:
                liked_tweets.append(result[x]['id_str'])

        print(liked_tweets)

        for z in range(0, len(liked_tweets)):
            favorite = liked_tweets[z]
            try:
                t.favorites.create(_id=favorite)
            except TwitterHTTPError as e:
                print("Can't like tweet #" + str(favorite) + " due to " + str(e.e))
                continue
            else:
                print("Added tweet #" + str(favorite) + " to favorites!")
         print("Liked " + str(likes) + " tweets with brand " + str(brands[idx]))

if __name__ == "__main__":
    main()
