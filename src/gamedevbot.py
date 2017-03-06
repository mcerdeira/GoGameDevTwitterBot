# -*- coding: utf-8 -*-
import sys
import configparser, os
from pathlib import Path
import sched
import time
import twitter

MEDIA_PATH = '.'
SCHED = sched.scheduler(time.time, time.sleep)
SECS = 3

def _main(argv):
    cfg_file = Path("twitter.cfg")
    if not cfg_file.is_file():
        ask_config()
    api = read_config()
    check_for_media(api)

def check_for_media(api):
    print('Checking for media in %s... (every %d secs)' % (MEDIA_PATH, SECS))
    for file in os.listdir(MEDIA_PATH):
        fname, fext = os.path.splitext(file)
        if fext in ('.jpg', '.gif', '.png'):
            print('%s found, posting on twitter...' % file)
            status = post_media(os.path.join(MEDIA_PATH, file), api)
            print(status.text)
            media_archive(file)
    SCHED.enter(SECS, 1, check_for_media, (api, ))
    SCHED.run()

def media_archive(file):
        os.makedirs(os.path.join(MEDIA_PATH, 'hist\\'))
    os.rename(os.path.join(MEDIA_PATH, file), os.path.join(MEDIA_PATH, 'hist\\' + file))

def post_media(media, api):

def ask_config():
    consumer_key = input('Consumer Key:')
    consumer_secret = input('Consumer Secret: ')
    access_token_key = input('Access Token Key: ')
    access_token_secret = input('Access Token Secret: ')
    global MEDIA_PATH
    global SECS
    MEDIA_PATH = input('Media Path: ')
    SECS = input('Check media path every N seconds: ')
    save_config(consumer_key, consumer_secret, access_token_key, access_token_secret)

def save_config(consumer_key, consumer_secret, access_token_key, access_token_secret):
    config = configparser.RawConfigParser()
    config.add_section('Main')
    config.set('Main', 'consumer_key', consumer_key)
    config.set('Main', 'consumer_secret', consumer_secret)
    config.set('Main', 'access_token_key', access_token_key)
    config.set('Main', 'access_token_secret', access_token_secret)
    config.set('Main', 'media_path', MEDIA_PATH)
    config.set('Main', 'secs', SECS)
    with open('twitter.cfg', 'w') as configfile:
        config.write(configfile)

def read_config():
    config = configparser.ConfigParser()
    _consumer_key = ''
    _consumer_secret = ''
    _access_token_key = ''
    _access_token_secret = ''

    if config.read('twitter.cfg'):
        _consumer_key = config.get('Main', 'consumer_key')
        _consumer_secret = config.get('Main', 'consumer_secret')
        _access_token_key = config.get('Main', 'access_token_key')
        _access_token_secret = config.get('Main', 'access_token_secret')
        global MEDIA_PATH
        global SECS
        MEDIA_PATH = config.get('Main', 'media_path')
        SECS = float(config.get('Main', 'secs'))

    return twitter.Api(consumer_key = _consumer_key,
                      consumer_secret = _consumer_secret,
                      access_token_key = _access_token_key,
                      access_token_secret = _access_token_secret)

if __name__ == '__main__':
    _main(sys.argv)
