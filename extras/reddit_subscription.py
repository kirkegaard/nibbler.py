import requests
import praw
import time
import sqlite3

from urllib.request import pathname2url

# Stupid hack because folder structure.. Should fix at some point!
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from utils import config


class Subscriptions():

    subscriptions = []
    endpoint = None
    auth = None
    client_id = None
    client_secret = None
    db = None

    conn = None
    reddit = None

    def __init__(self, endpoint, auth, client_id, client_secret, db='pusher.db'):
        self.endpoint = endpoint
        self.auth = auth
        self.client_id = client_id
        self.client_secret = client_secret
        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.conn.row_factory = sqlite3.Row
        self.reddit = praw.Reddit(client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  user_agent='python:com.lowpoly.nibbler.feed:v0.1 (by /u/ranzadk)')

    def update_subscriptions(self):
        self.subscriptions = []
        c = self.conn.cursor()
        c.execute('SELECT * FROM subscriptions')
        for s in c.fetchall():
            self.subscriptions.append(Subscription(**s))

    def check_subscriptions(self):
        for subscription in self.subscriptions:
            print('Checking: {}'.format(subscription.subreddit))
            try:
                submissions = self.reddit.subreddit(subscription.subreddit).hot()
                for submission in submissions:
                    sid = int(submission.id, 36)
                    if sid > subscription.sid and not self.__link_exists(subscription.channel, submission.url):
                        self.__save_link(subscription.channel, submission.url)
                        self.__update_sid(sid, subscription.subreddit)
                        self.__post(subscription, submission)
            except Exception as e:
                print('Error {e}')

    def __link_exists(self, channel, link):
        c = self.conn.cursor()
        c.execute('SELECT * FROM links WHERE channel=? AND link=?', [channel, link])
        if c.fetchone() == None:
            return False
        return True

    def __save_link(self, channel, link):
        c = self.conn.cursor()
        c.execute('INSERT INTO links VALUES (?,?)', [channel, link])
        self.conn.commit()

    def __update_sid(self, sid, subreddit):
        c = self.conn.cursor()
        c.execute('UPDATE subscriptions SET sid=? WHERE subreddit=?', [sid, subreddit])
        self.conn.commit()

    def __post(self, subscription, submission):
        msg = '[{}] **{}:** {}'.format(subscription.subreddit, submission.title, submission.url)
        res = requests.post(self.endpoint, json={'channel': subscription.channel,
                                                 'msg': msg}, headers={'Authorization': self.auth})
        print('Posting: %s' % msg)


class Subscription():

    sid = None
    channel = None
    subreddit = None

    def __init__(self, sid, channel, subreddit):
        self.sid = sid
        self.channel = channel
        self.subreddit = subreddit

config = config.Config('config/bot.json')
sub = Subscriptions(endpoint=config.get('bot_endpoint'),
                    auth=config.get('bot_auth'),
                    client_id=config.get('reddit_id'),
                    client_secret=config.get('reddit_secret'),
                    db=config.get('subscription_db'))

while True:
    sub.update_subscriptions()
    sub.check_subscriptions()
    time.sleep(300)
