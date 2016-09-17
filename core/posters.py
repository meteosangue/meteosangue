import facebook
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
            api.update_with_media(image_path, status=status)
        else:
            api.update_status(status)
    except tweepy.TweepError as ex:
        raise MeteoSangueException(ex)


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
Method to post with image on Facebook
"""
def facebook_status(status, image_path=None):
    try:
        graph = facebook.GraphAPI(settings.FACEBOOK_TOKEN)
        if image_path:
            graph.put_photo(image=open(image_path, 'rb'), message=status)
        else:
            graph.put_wall_post(status)
    except Exception as ex:
        raise MeteoSangueException(ex)
