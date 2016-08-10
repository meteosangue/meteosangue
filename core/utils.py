import facebook
import locale
import os
import requests
import tweepy

from django.conf import settings
from django.core.files import File
from django.db.models import Q
from datetime import datetime
from lxml import html
from tempfile import NamedTemporaryFile
from selenium import webdriver

from .models import BloodGroup, Log


"""
Method to get date from CRS output
"""
def crs_to_date(date):
    locale.setlocale(locale.LC_TIME, "it_IT")
    clean1 = date.replace('Aggiornato a\xa0', '').replace('\xa0alle\xa0', ' ').split(' ')
    clean2 = ' '.join(clean1[1:])
    return datetime.strptime(clean2, "%d %B %Y %H:%M")


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


"""
Method to format blood groups status
"""
def get_blood_group_list(blood_groups, icon, group_status, group_desc):
    blood_groups_for_status = blood_groups.values_list('groupid', flat=True).filter(status=group_status)
    if len(blood_groups_for_status):
        return '{0} {1}: {2}\n'.format(icon, group_desc, ' | '.join(blood_groups_for_status))
    else:
        return ''


"""
Method to post blood weather on social
"""
def post_blood_weather(blood_groups, log):
    status = ''
    status += get_blood_group_list(blood_groups, '⚫️', 'Z', 'Emergenza')
    status += get_blood_group_list(blood_groups, '🔴', 'U', 'Urgente')
    status += get_blood_group_list(blood_groups, '⚠️', 'F', 'Fragile')
    status += get_blood_group_list(blood_groups, '💚', 'S', 'Stabile')
    status += get_blood_group_list(blood_groups, '💛', 'E', 'Eccedenza')
    if not log.twitter_done:
        try:
            tweet_status(status, os.path.join(settings.UPLOAD_METEO, log.image.name))
            log.twitter_done = True
            log.save()
        except tweepy.TweepError as ex:
            pass


"""
Method to fetch blood groups
"""
def update_blood_groups():
    driver = webdriver.PhantomJS()
    driver.set_window_size(450, 650)
    driver.get("https://web2.e.toscana.it/crs/meteo/")

    f = NamedTemporaryFile(delete=False)
    driver.save_screenshot(f.name)
    tree = html.fromstring(driver.page_source)
    driver.quit()

    groups = tree.xpath('//input[@type="hidden"]')
    update_time = crs_to_date(tree.xpath('//div[@id="aggiornamento"]/text()')[0])
    log, created = Log.objects.get_or_create(datetime=update_time)

    if created:
        Log.objects.filter(~Q(datetime=update_time)).delete()
        log.image.save(
            update_time.strftime("%Y-%m-%d_%H:%M:%S") + '.png',
            File(f)
        )
        f.close()
        os.unlink(f.name)
        for group in groups:
            group_id = group.name.replace('N', '-').replace('P', '+')
            dbgroup, created = BloodGroup.objects.get_or_create(groupid=group_id)
            dbgroup.status = group.value
            dbgroup.save()
    return BloodGroup.objects.all(), log
