import base64
import json
import requests
import textwrap

SITE_URL = 'https://morbotron.com'
API_URL = '{0}/api/search'.format(SITE_URL)
CAPTION_URL = '{0}/api/caption'.format(SITE_URL)
RANDOM_URL = '{0}/api/random'.format(SITE_URL)

class Screencap(object):
    def __init__(self, values):
        self.episode = values['Episode']
        self.timestamp = values['Timestamp']
        self.id = values['Id']

    def __repr__(self):
        try:
            ep = self.episode
            time = self.timestamp
            title = self.ep_title
        except AttributeError:
            self._get_details()
        finally:
            return 'ID: {0} {1}/{2}'.format(self.id, self.episode, self.timestamp)

    def image_url(self, index):
        try:
            ep = self.episode
            ts = self.timestamp
        except AttributeError:
            self._get_details()
            ep = self.ep_number
            ts = self.timestamp
        finally:
            return '{0}/img/{1}/{2}.jpg'.format(SITE_URL, ep, ts)

    def meme_url(self, caption = None):
        if caption is None or not caption.strip():
            try:
                caption = self.caption
            except AttributeError:
                self._get_details()
                caption = self.caption
        else:
            if len(caption) > 300:
                caption = caption[:300]
            caption = self._chop_captions(caption)

        return '{0}/meme/{1}/{2}.jpg?b64lines={3}'.format(
            SITE_URL, 
            self.episode, 
            self.timestamp, 
            base64.urlsafe_b64encode(bytes(caption, 'utf-8')).decode('ascii'))

    def _get_details(self):
        cap_search = requests.get('{0}?e={1}&t={2}'.format(CAPTION_URL, self.episode, self.timestamp))
        data = cap_search.json()
        caption = " ".join([subtitle['Content'] for subtitle in data['Subtitles']])
        self.caption = self._chop_captions(caption)
        self.ep_title = data['Episode']['Title']
        self.season = data['Episode']['Season']
        self.ep_number = data['Episode']['EpisodeNumber']
        self.director = data['Episode']['Director']
        self.writer = data['Episode']['Writer']
        self.org_air_date = data['Episode']['OriginalAirDate']
        self.wiki_link = data['Episode']['WikiLink']

    def _chop_captions(self, caption):
        return textwrap.fill(caption, 25)

def search(query):
    """Returns a list of Screencap objects based on the string provided."""
    if len(query) > 200:
        query = query[:200]

    try:
        gen_search = requests.get('https://morbotron.com/api/search?q={0}'.format(query))
    except requests.exceptions.ConnectionError:
        return []

    info = gen_search.json()
    search_results = []
    for result in info:
        search_results.append(Screencap(result))

    return search_results

def random():
    """Returns a random screencap object"""

    try:
        random_search = requests.get(RANDOM_URL)
    except requests.exceptions.ConnectionError:
        return []

    info = random_search.json()
    random_screen = {'Episode': info['Frame']['Episode'], 'Timestamp' : info['Frame']['Timestamp'], 'Id': info['Frame']['Id']}
    random_Screencap = Screencap(random_screen)
    return random_Screencap