import locale
import pytz
import tweepy

from django.conf import settings
from datetime import datetime


"""
Method to get date from CRS output
"""
def crs_to_date(date):
    my_tz = pytz.timezone('Europe/Rome')
    locale.setlocale(locale.LC_TIME, "it_IT")
    clean1 = date.replace('Aggiornato a\xa0', '').replace('\xa0alle\xa0', ' ').split(' ')
    clean2 = ' '.join(clean1[1:])
    return my_tz.localize(datetime.strptime(clean2, "%d %B %Y %H:%M"))


"""
Method to post with image on Twitter
"""
def tweet_status(status, image_path=None):
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    if image_path:
        api.update_with_media(image_path, status=status)
    else:
        api.update_status(status)
