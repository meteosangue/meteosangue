import locale
import pytz

from datetime import datetime


"""
Method to get date from CRS output
"""
def crs_to_date(date):
    my_tz = pytz.timezone('Europe/Rome')
    try:
        locale.setlocale(locale.LC_TIME, "it_IT.utf8")
    except:
        locale.setlocale(locale.LC_TIME, "it_IT")
    clean1 = date.replace('Aggiornato a\xa0', '').replace('\xa0alle\xa0', ' ').split(' ')
    clean2 = ' '.join(clean1[1:])
    return my_tz.localize(datetime.strptime(clean2, "%d %B %Y %H:%M"))

