import facebook
import json
import random
import telepot
import tweepy

from django.conf import settings
from .exceptions import MeteoSangueException


"""
Method to post with image on Twitter
"""
def tweet_status(status, image_path=None):
    try:
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        if image_path:
            new_tweet = api.update_with_media(image_path, status=status)
        else:
            new_tweet = api.update_status(status)
    except tweepy.TweepError as ex:
        raise MeteoSangueException(ex)

    try:
        mention = '{0} {1}'.format(
            ' '.join([ass['twitter_id'] for ass in settings.BLOOD_ASSOCIATIONS if 'twitter_id' in ass]),
            '⬆ Nuovo bollettino meteo ⬆',
        )
        api.update_status(mention, in_reply_to_status_id=new_tweet.id)
    except tweepy.TweepError as ex:
        pass #Mention is allowed to fail silently

"""
Method to post with image on Telegram
"""
def telegram_status(status, image_path=None):
    try:
        bot = telepot.Bot(settings.TELEGRAM_TOKEN)
        if image_path:
            bot.sendPhoto(settings.TELEGRAM_CHANNEL, open(image_path, "rb"))
        bot.sendMessage(settings.TELEGRAM_CHANNEL, status)
    except telepot.exception.TelepotException as ex:
        raise MeteoSangueException(ex)


"""
Method to generate mention tags in Facebook
"""
def _generate_tag(user_id):
    return {
        'tag_uid': user_id
    }


"""
Method to post with image on Facebook
"""
def facebook_status(status, image_path=None):

    tags = [_generate_tag(ass['facebook_id']) for ass in settings.BLOOD_ASSOCIATIONS if 'facebook_id' in ass]
    try:
        graph = facebook.GraphAPI(settings.FACEBOOK_TOKEN)
        if image_path:
            graph.put_photo(image=open(image_path, 'rb'), message=status, tags=json.dumps(tags))
        else:
            graph.put_wall_post(status)
    except Exception as ex:
        raise MeteoSangueException(ex)
