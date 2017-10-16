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

def getCommits(word_list):
	today = datetime.date.today()
	now = datetime.datetime.now()
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
			print("sleeping")
			time.sleep(60)

		for num in range(len(x['items'])):
			with open("{}.txt".format(now), 'a') as f:
				msg = x['items'][num]['commit']['message']
				msg.strip()
				if 10<len(msg) and len(msg)<141:
					if "\n" or "\n\n" in msg:
						msg.replace("\n","")
						msg.replace("\n\n","")
						print(msg)
					f.writelines(msg+ "\n")
	return

def tweet():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)



def main():
	
	word_list = ["fuck", "bitch", "shit", "tits", "asshole", "arsehole", "cocksucker", "cunt", "hell", "douche", " testicle", " twat", " bastard", " sperm", " dildo", " wanker", "prick", "penis", "vagina", "whore", "boner", "suck"]
	getCommits(word_list)
	#tweet()


if __name__ == '__main__':
	main()