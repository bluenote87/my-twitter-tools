# This program depends upon twitter.com's API and sixohsix's Python Twitter Tools at the following repo: https://github.com/sixohsix/twitter
from twitter import *
import os.path

# This will follow back any account currently following you and send them a welcoming direct message
def main():
    #This app has Read, Write and Access direct messages permissions
    MY_TWITTER_CREDS = os.path.expanduser('~/.my_message_app_credentials')
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("Your DM App Name Here", consumer_key="XXXXX", consumer_secret="XXXXX",
                    token_filename=MY_TWITTER_CREDS)
    oauth_token, oauth_secret = read_token_file(filename=MY_TWITTER_CREDS)
    t = Twitter(auth=OAuth(token=oauth_token, token_secret=oauth_secret, 
    	consumer_key="XXXXX", consumer_secret="XXXXX"))

    my_followers = t.followers.list(screen_name="your_screen_name_here", include_user_entities=False, count=15)

    new_followers = list()

    for i in range(0, len(my_followers['users'])):
        if my_followers['users'][i]['following'] == False and my_followers['users'][i]['muting'] == False:
            # Any follower you have 'muted' is effectively blacklisted from this app
            new_followers.append(my_followers['users'][i]['screen_name'])

    for x in range(0, len(new_followers)):
        try:
            t.friendships.create(screen_name=str(new_followers[x]))
        except TwitterHTTPError as e:
            print("Can't add " + str(new_followers[x]) + " due to " + str(e.e))
            continue
        else:
            print(str(new_followers[x]) + " has been added to your friends list!")
        try:
            t.direct_messages.new(user=str(new_followers[x]), text="👋 This is where your welcome message goes.")
        except TwitterHTTPError as e:
            print("Can't message " + str(new_followers[x]) + " due to " + str(e.e))
            continue
        else:
            print("Successfully sent a welcome message to " + str(new_followers[x]) + "!")

if __name__ == "__main__":
    main()
