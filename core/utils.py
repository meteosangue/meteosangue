import locale
import os
import requests

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
            update_time.strftime("%Y-%m-%d_%H:%M:%S"),
            File(f)
        )
        f.close()
        os.unlink(f.name)
        for group in groups:
            dbgroup, created = BloodGroup.objects.get_or_create(groupid=group.name)
            dbgroup.status = group.value
            dbgroup.save()
    return BloodGroup.objects.all(), log


"""
Method to post blood weather on social
"""
def post_blood_weather(blood_groups, log):
    pass
