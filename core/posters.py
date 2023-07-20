#import facebook
import json
import telepot
import tweepy

from .settings import BLOOD_ASSOCIATIONS, TW_CONSUMER_KEY, TW_CONSUMER_SECRET, TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET, TELEGRAM_CHANNEL, TELEGRAM_TOKEN, FACEBOOK_TOKEN
from .exceptions import MeteoSangueException


"""
Method to post with image on Twitter
"""
def tweet_status(status, image_path=None):
    try: 
        auth = tweepy.OAuth1UserHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
        auth.set_access_token(
            TW_ACCESS_TOKEN,
            TW_ACCESS_TOKEN_SECRET,
        )
        old_api = tweepy.API(auth)

        media = old_api.media_upload(filename=image_path)
        media_id = media.media_id

        api = tweepy.Client(
            consumer_key=TW_CONSUMER_KEY,
            consumer_secret=TW_CONSUMER_SECRET,
            access_token=TW_ACCESS_TOKEN,
            access_token_secret=TW_ACCESS_TOKEN_SECRET
        )
        new_tweet = api.create_tweet(text=status, media_ids=[media_id])
    except tweepy.errors.TweepyException as ex:
        raise MeteoSangueException(ex)

    try:
        mention = '{0} {1}'.format(
            ' '.join([ass['twitter_id'] for ass in BLOOD_ASSOCIATIONS if 'twitter_id' in ass]),
            'Nuovo bollettino meteo ⬆',
        )
        api.create_tweet(text=mention, in_reply_to_tweet_id=new_tweet.data['id'])
    except tweepy.errors.TweepyException as ex:
        pass #Mention is allowed to fail silently


"""
Method to post with image on Telegram
"""
def telegram_status(status, image_path=None):
    try:
        bot = telepot.Bot(TELEGRAM_TOKEN)
        if image_path:
            bot.sendPhoto(TELEGRAM_CHANNEL, open(image_path, "rb"))
        bot.sendMessage(TELEGRAM_CHANNEL, status)
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

    tags = [_generate_tag(ass['facebook_id']) for ass in BLOOD_ASSOCIATIONS if 'facebook_id' in ass]
    try:
        graph = facebook.GraphAPI(FACEBOOK_TOKEN)
        if image_path:
            graph.put_photo(image=open(image_path, 'rb'), message=status, tags=json.dumps(tags))
        else:
            graph.put_wall_post(status)
    except Exception as ex:
        raise MeteoSangueException(ex)
