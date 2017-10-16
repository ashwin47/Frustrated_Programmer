''''
A bot to retrive github commit messages with profanity and tweet it. 


https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}

TODO

try catch
duplicate tweet detection 
new line bug

'''

import requests
import datetime
import json
import time
import tweepy
import config
import random

def getCommits(word_list, now):
	today = datetime.date.today()
	print("Now:"+ str(today))
	i = 0
	for word in word_list:
		url="https://api.github.com/search/commits?q={}+committer-date:{}".format(word, today)
		headers={'accept':'application/vnd.github.cloak-preview'}
		r = requests.get(url, headers=headers)
		x = json.loads(r.text)
		#print(r.status_code)
		i +=1

		if i == 9 or i == 18:
			print("sleeping") # Sleep one minute to avoid API rejection by Github (status 403)
			time.sleep(60)

		for num in range(len(x['items'])):
			with open("{}.txt".format(now), 'a') as f:
				msg = x['items'][num]['commit']['message']
				msg.strip()
				if 10<len(msg) and len(msg)<141:
					if "\n" or "\n\n" in msg:
						msg.replace("\n","")
						msg.replace("\n\n","")  ##TODO
						#print(msg)
					f.writelines(msg+ "\n")
	return

def tweet(now):
	print("Ready to tweet")
	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
	auth.set_access_token(config.access_token, config.access_token_secret)

	api = tweepy.API(auth)
	# If the authentication was successful, you should see the name of the account print out

	#print(api.me().name)
	
	commit_msg = []
	with open("{}.txt".format(now), 'r') as f:
		commit_msg = f.read().split('\n')
	
	print(random.choice(commit_msg))

	status = api.update_status(status= random.choice(commit_msg))
	print (status.id) # print id if ts tweeted 

	return



def main():
	now = datetime.datetime.now()
	
	word_list = ["fuck", "bitch", "shit", "tits", "asshole", "arsehole", "cocksucker", "cunt", "hell", "douche", " testicle", " twat", " bastard", " sperm", " dildo", " wanker", "prick", "penis", "vagina", "whore", "boner", "suck"]
	getCommits(word_list, now)
	tweet(now)


if __name__ == '__main__':
	main()