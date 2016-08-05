import locale
import requests

from datetime import datetime
from lxml import html

from .models import BloodGroup


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
def fetch_blood_groups():
    page = requests.get('https://web2.e.toscana.it/crs/meteo/')
    tree = html.fromstring(page.content)
    groups = tree.xpath('//input[@type="hidden"]')
    update_date = crs_to_date(tree.xpath('//div[@id="aggiornamento"]/text()')[0])
    dbgroups = []
    for group in groups:
        dbgroup, created = BloodGroup.objects.get_or_create(groupid=group.name)
        dbgroup.status = group.value
        dbgroups.append(dbgroup)
    return dbgroups, update_date