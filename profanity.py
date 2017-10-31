''''
A bot to retrive github commit messages with profanity and tweet it. 


https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}


'''

import requests
import datetime
import json
import time
import os
#import sys
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
		#print(r.status_code)
		i +=1

		if i == 9 or i == 18:
			print("sleeping") # Sleep one minute to avoid API rejection by Github (status 403)
			time.sleep(60)

		for num in range(len(x['items'])):
			with open("commits/{}.txt".format(now), 'a+') as f:
				msg = x['items'][num]['commit']['message']
				msg.strip()
				if 10<len(msg) and len(msg)<141:
					if "\n" or "\n\n" in msg:
						msg = msg.replace("\n"," ").replace("\n\n"," ")  ##TODO fix new line bug
					f.write(msg+ "\n") # Write all relevent commit msgs to a file
	return

def tweet(now, today):
	print("Ready to tweet")
	NotDuplicate = True
	count =0
	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
	auth.set_access_token(config.access_token, config.access_token_secret)

	api = tweepy.API(auth)
	

	#print(api.me().name) #If the authentication was successful, you should see the name of the account print out
	
	commit_msg = []
	with open("commits/{}.txt".format(now), 'r') as f:
		commit_msg = f.read().split('\n')
	

	while (NotDuplicate == True):
		draft = random.choice(commit_msg)
		print(draft)
		past_tweets_today = []
		if os.path.exists("drafts/{}.txt".format(today)) != True:
			open("drafts/{}.txt".format(today), "a").close()
		with open("drafts/{}.txt".format(today), 'r+') as f: # When i use append mode it don't find duplicates ! Now i have to create file it don't exist already 
			if os.path.getsize("drafts/{}.txt".format(today)) > 0:
				past_tweets_today = f.read().split("\n")
			if not draft in past_tweets_today:
				f.write(draft+ "\n")
				status = api.update_status(status= draft)
				print("Status id:" + str(status.id)) # print id of the tweet
				NotDuplicate = False
				print("NotDuplicate:"+ str(NotDuplicate))
			else:
				count +=1
				print("NotDuplicate:"+ str(NotDuplicate))
				if count>10: break # To break possible infinate loop 

	return



def main():
	#reload(sys)
	#sys.setdefaultencoding('utf-8')

	now = datetime.datetime.now()
	today = datetime.date.today()
	
	word_list = ["fuck", "bitch", "shit", "suck", "arsehole", "cocksucker", "cunt", "hell", "tits", "asshole", " sperm", " dildo", "douche", " testicle", " twat", " bastard", " wanker", "prick", "penis", "vagina", "whore", "boner"]
	getCommits(word_list, now, today)
	tweet(now, today)


if __name__ == '__main__':
	main()