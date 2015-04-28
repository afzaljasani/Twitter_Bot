from twython import Twython
from lxml import html
from secret import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
import sys 
import requests 
import random
import urllib2
import time

BASE_URL = "http://azlyrics.com/"
ARTISTS_LIST = ["Nas", "Jayz", "ti"]

def pick_artist(ARTISTS_LIST):
    selected_artist = random.choice(ARTISTS_LIST)
    return selected_artist

def form_url(selected_artist):
    url = BASE_URL + selected_artist[0].lower() + "/" + selected_artist.lower() + ".html"
    page = requests.get(url)
    tree = html.fromstring(page.text)
    songs = tree.xpath('//*[@id="listAlbum"]/a/@href')
    return songs 

def pick_song(songs):
	random_song = random.choice(songs)
	edited_url = random_song.replace("../","")
	final_url = BASE_URL + edited_url
	return final_url

def pull_lyrics(final_url):
	page = requests.get(final_url)
	tree = html.fromstring(page.text)
	text = tree.xpath('/html/body/div[3]/div/div[2]/div[6]/text()')
	text = [each.strip('\r\n') for each in text]
	new = []
	for each in text:
		if each and each.strip():
			new.append(each)
	lyrics_text = random.choice(new)
	while len(lyrics_text) > 120:
		return lyrics_text
	return lyrics_text

def clean(lyrics_line):
	cleaned = lyrics_line.strip('\n')
	return cleaned 


def assign_philosopher(lyrics_text):
	philosophers = ["Aristotle", "Plato", "Paul of Tarsus", "Rene Descartes",
	        "Confucius", "Thomas Aquinas", "Epicurus", "Nietzsche", "Kafka"]
	random_philosopher = random.choice(philosophers)
	assigned_tweet = lyrics_text + " - " + random_philosopher
	return assigned_tweet

def tweet(polished_tweet):
    bot_api = Twython(
        APP_KEY ,
        APP_SECRET,
        OAUTH_TOKEN,
        OAUTH_TOKEN_SECRET)

    bot_api.update_status(status=polished_tweet)

def main():
	while True:
		artist = pick_artist(ARTISTS_LIST)
		url = form_url(artist)
		song = pick_song(url)
		lyrics = pull_lyrics(song)
		cleaned_lyrics = clean(lyrics)
		polished_tweet = assign_philosopher(cleaned_lyrics)
		tweet(polished_tweet)
		time.sleep(4000)

if __name__ == '__main__':
    main()

