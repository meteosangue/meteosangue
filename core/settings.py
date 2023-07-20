import os, sys

# App settings
VERSION = '1.3.0'
DEBUG = False if os.getenv('PRODUCTION', '0') == '1' else True
FETCH_SITE_WAIT = int(os.getenv('FETCH_SITE_WAIT', 20))

# Twitter credentials
TW_ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', 'D3V')
TW_ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET', 'D3V')
TW_CONSUMER_KEY = os.getenv('CONSUMER_KEY', 'D3V')
TW_CONSUMER_SECRET = os.getenv('CONSUMER_SECRET', 'D3V')

# Telegram credentials
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'D3V')
TELEGRAM_CHANNEL = os.getenv('TELEGRAM_CHANNEL', 'D3V')

# Facebook credentials
FACEBOOK_TOKEN = os.getenv('FACEBOOK_TOKEN', 'D3V')

# Blood associations data
BLOOD_ASSOCIATIONS = [
    {
        'name': 'Avis Nazionale',
        'twitter_id': '@avisnazionale',
        'facebook_id': '154932917976132'
    },
    {
        'name': 'Avis Giovani',
        'twitter_id': '@giovaniavis',
    },
    {
        'name': 'Fidas Nazionale',
        'twitter_id': '@FIDASnazionale',
        'facebook_id': '49816054736'
    },
    {
        'name': 'Frates Nazionale',
        'twitter_id': '@FratresNaz',
    },
    {
        'name': 'Centro Naz. Sangue',
        'twitter_id': '@CentroSangue',
        'facebook_id': '477808612320970'
    }
]

API_FILE = os.path.join('api', 'meteo.json')

if 'test' in sys.argv:
    try:
        from .test_settings import *
    except ImportError:
        pass

