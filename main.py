# -*- coding: utf-8 -*-

import os
import json

from core import settings
from lxml import html
from tempfile import NamedTemporaryFile
from selenium import webdriver

from core.posters import tweet_status, telegram_status
from core.posters_register import posters_register
from core.utils import crs_to_date


"""
Register posters
"""
posters_register.register_poster(tweet_status, 'twitter_done')
posters_register.register_poster(telegram_status, 'telegram_done')
# posters_register.register_poster(facebook_status, 'facebook_done')


"""
Method to format blood groups status
"""
def get_blood_group_list(blood_groups, icon, group_status, group_desc):
    blood_groups_for_status = [k for k,v in blood_groups.items() if v == group_status]
    if len(blood_groups_for_status):
        return '{0} {1}: {2}\n'.format(icon, group_desc, ' , '.join(blood_groups_for_status))
    else:
        return ''
    

"""
Method to generate API json file
"""
def generate_api(update_time, xml_groups):
    api = {}
    api['date'] = update_time.isoformat()
    api['status'] = {}
    for group in xml_groups:
        group_id = group.name.replace('N', '-').replace('P', '+')
        api['status'][group_id] = group.value
    with open(settings.API_FILE, "w") as outfile:
        outfile.write(json.dumps(api, indent=4))


"""
Method to post blood weather on social
"""
def post_blood_weather():
    with open(settings.API_FILE, "r") as outfile:
        blood_groups = json.loads(outfile.read())['status']
        status = ''
        status += get_blood_group_list(blood_groups, '🚨', 'Z', 'Emergenza')
        status += get_blood_group_list(blood_groups, '🆘', 'U', 'Urgente')
        status += get_blood_group_list(blood_groups, '💜', 'F', 'Fragile')
        status += get_blood_group_list(blood_groups, '💚', 'S', 'Stabile')
        status += get_blood_group_list(blood_groups, '💛', 'E', 'Eccedenza')

        print (status)

        # posters_register.run(status)


"""
Method to fetch blood groups
"""
def update_blood_groups():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://web2.e.toscana.it/crs/meteo/")
    # time.sleep(settings.FETCH_SITE_WAIT)

    f = NamedTemporaryFile(delete=False)
    driver.set_window_size(450, 650)
    # time.sleep(settings.FETCH_SITE_WAIT)
    driver.save_screenshot(f.name)
    tree = html.fromstring(driver.page_source)
    driver.quit()

    groups = tree.xpath('//input[@type="hidden"]')
    update_time = crs_to_date(tree.xpath('//div[@id="aggiornamento"]/text()')[0])
    if os.path.getsize(f.name) > 3000: # check if image is valid
        os.unlink(f.name)
        generate_api(update_time, groups)
    f.close()
    return True


needs_update = update_blood_groups()
if needs_update:
    post_blood_weather()