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

def getCommits(word_list, now, today):
	print("Now:"+ str(today))
	i = 0
	for word in word_list:
		url="https://api.github.com/search/commits?q={}+committer-date:{}".format(word, today)
		headers={'accept':'application/vnd.github.cloak-preview'}
		r = requests.get(url, headers=headers)
		x = json.loads(r.text)
		print(r.text)
		i +=1

		if i == 9 or i == 18:
			print("sleeping") # Sleep one minute to avoid API rejection by Github (status 403)
			time.sleep(60)

		for num in range(len(x['items'])):
			print("In")
			with open("{}.txt".format(now), 'a') as f:
				msg = x['items'][num]['commit']['message']
				msg.strip()
				print("msg")
				if 10<len(msg) and len(msg)<141:
					if "\n" or "\n\n" in msg:
						msg.replace("\n","")
						msg.replace("\n\n","")  ##TODO fix new line bug
						print(msg)
					f.writelines(msg+ "\n") # Write all relevent commit msgs to a file
	return

def tweet(now, today):
	print("Ready to tweet")
	Found = False
	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
	auth.set_access_token(config.access_token, config.access_token_secret)

	api = tweepy.API(auth)
	

	#print(api.me().name) #If the authentication was successful, you should see the name of the account print out
	
	commit_msg = []
	with open("commits/{}.txt".format(now), 'r') as f:
		commit_msg = f.read().split('\n')
	

	while (Found == False):
		draft = random.choice(commit_msg)
		print(draft)
		with open("drafts/{}.txt".format(today), 'a') as f:
			past_tweets_today = f.read().split('\n')
			if not past_tweets_today == draft:
				f.writelines(draft+ "\n")
				status = api.update_status(status= draft)
				print (status.id) # print id if ts tweeted 
				Found = True

	return



def main():
	now = datetime.datetime.now()
	today = datetime.date.today()
	
	word_list = ["fuck", "bitch", "shit", "tits", "asshole", "arsehole", "cocksucker", "cunt", "hell", "douche", " testicle", " twat", " bastard", " sperm", " dildo", " wanker", "prick", "penis", "vagina", "whore", "boner", "suck"]
	getCommits(word_list, now, today)
	tweet(now, today)


if __name__ == '__main__':
	main()