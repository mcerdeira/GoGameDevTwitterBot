# -*- coding: utf-8 -*-
import sys
import configparser, os
from pathlib import Path
import sched
import random
import time
import twitter

SCHED = sched.scheduler(time.time, time.sleep)

class ConfigFileObj:
    def __init__(self):
        self.media_path = ''
        self.secs = 3
        self.twitter_api = None
        self.template_path = ''

def _main(argv):
    cfg_file = Path('twitter.cfg')
    if not cfg_file.is_file():
        ask_config()

    check_for_media(read_config())

def check_for_media(config_obj):
    print('Checking for media in %s... (every %d secs)' % (config_obj.media_path, config_obj.secs))
    for file in os.listdir(config_obj.media_path):
        fname, fext = os.path.splitext(file)
        if fext in ('.jpg', '.jpeg', '.gif', '.png'):
            print('%s found, posting on twitter...' % file)
            status = post_media(os.path.join(config_obj.media_path, file), config_obj)
            print('I posted %s' % status.text)
            media_archive(file, config_obj)
    SCHED.enter(config_obj.secs, 1, check_for_media, (config_obj, ))
    SCHED.run()

def media_archive(file, config_obj):
    if not os.path.exists(os.path.join(config_obj.media_path, 'hist\\')): #TODO: history folder must be configurable?
        os.makedirs(os.path.join(config_obj.media_path, 'hist\\'))
    os.rename(os.path.join(config_obj.media_path, file), os.path.join(config_obj.media_path, 'hist\\' + str(time.time()) + '_' + file))

def post_media(media, config_obj):
    text = get_tweet_text(config_obj)
    return config_obj.api.PostUpdate(text, media) #TODO: add logic for the tweet text

def get_tweet_text(config_obj):
    file = random.choice(os.listdir(config_obj.template_path))
    return open(os.path.join(config_obj.template_path, file)).read()

def ask_config():
    consumer_key = input('Consumer Key:')
    consumer_secret = input('Consumer Secret: ')
    access_token_key = input('Access Token Key: ')
    access_token_secret = input('Access Token Secret: ')
    media_path = input('Media Path: ')
    template_path = input('Template Path: ')
    secs = input('Check media path every N seconds: ')
    save_config(consumer_key, consumer_secret, access_token_key, access_token_secret, media_path, secs, template_path)

def save_config(consumer_key, consumer_secret, access_token_key, access_token_secret, media_path, secs, template_path):
    config = configparser.RawConfigParser()
    config.add_section('Main')
    config.set('Main', 'consumer_key', consumer_key)
    config.set('Main', 'consumer_secret', consumer_secret)
    config.set('Main', 'access_token_key', access_token_key)
    config.set('Main', 'access_token_secret', access_token_secret)
    config.set('Main', 'media_path', media_path)
    config.set('Main', 'secs', secs)
    config.set('Main', 'template_path', template_path)
    with open('twitter.cfg', 'w') as configfile:
        config.write(configfile)

def read_config():
    config_obj = ConfigFileObj()
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
        _media_path = config.get('Main', 'media_path')
        _secs = float(config.get('Main', 'secs'))
        _template_path = config.get('Main', 'template_path')

    config_obj.media_path = _media_path
    config_obj.template_path = _template_path
    config_obj.secs = _secs
    config_obj.api =  twitter.Api(consumer_key = _consumer_key,
                      consumer_secret = _consumer_secret,
                      access_token_key = _access_token_key,
                      access_token_secret = _access_token_secret)

    return config_obj

if __name__ == '__main__':
    _main(sys.argv)