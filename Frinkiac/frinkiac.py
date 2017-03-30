import base64
import json
import requests
import textwrap

FRINK_URL = 'https://frinkiac.com'
FRINK_API_URL = '{0}/api/search'.format(FRINK_URL)
FRINK_CAPTION_URL = '{0}/api/caption'.format(FRINK_URL)
FRINK_RANDOM_URL = '{0}/api/random'.format(FRINK_URL)

MORB_URL = 'https://morbotron.com'
MORB_API_URL = '{0}/api/search'.format(MORB_URL)
MORB_CAPTION_URL = '{0}/api/caption'.format(MORB_URL)
MORB_RANDOM_URL = '{0}/api/random'.format(MORB_URL)

class Screencap(object):
    def __init__(self, values, frink):
        self.episode = values['Episode']
        self.timestamp = values['Timestamp']
        self.id = values['Id']
        self.frink = frink
        if frink:
            self.rich_url = '{0}/caption/{1}/{2}'.format(FRINK_URL, self.episode, self.timestamp)
        else:
            self.rich_url = '{0}/caption/{1}/{2}'.format(MORB_URL, self.episode, self.timestamp)

    def __repr__(self):
        return '{1}/{2}'.format(self.id, self.episode, self.timestamp)

    def image_url(self, caption = False):
        """Provides the image for a given episode/timestamp. Pass 'True' for caption"""
        SITE_URL = FRINK_URL if self.frink else MORB_URL
        try:
            ep = self.episode
            ts = self.timestamp
        except AttributeError:
            self._get_details()
            ep = self.ep_number
            ts = self.timestamp
        finally:
            if caption:
                return self.meme_url(caption = caption)
            else:
                return '{0}/img/{1}/{2}.jpg'.format(SITE_URL, ep, ts)

    def meme_url(self, caption = None):
        SITE_URL = FRINK_URL if self.frink else MORB_URL
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
        CAPTION_URL = FRINK_CAPTION_URL if self.frink else MORB_CAPTION_URL
        cap_search = requests.get('{0}?e={1}&t={2}'.format(CAPTION_URL, self.episode, self.timestamp))
        data = cap_search.json()

        # This controls how many captions you get.
        caption = " ".join([subtitle['Content'] for subtitle in data['Subtitles']])
        self.caption = self._chop_captions(caption[:300])
        self.ep_title = data['Episode']['Title']
        self.season = data['Episode']['Season']
        self.ep_number = data['Episode']['EpisodeNumber']
        self.director = data['Episode']['Director']
        self.writer = data['Episode']['Writer']
        self.org_air_date = data['Episode']['OriginalAirDate']
        self.wiki_link = data['Episode']['WikiLink']

    def _chop_captions(self, caption):
        return textwrap.fill(caption, 25)

def search(query, frink = True):
    """Returns a list of Screencap objects based on the string provided."""
    SITE_URL = FRINK_URL if frink else MORB_URL
    if len(query) > 200:
        query = query[:200]

    try:
        gen_search = requests.get('{0}/api/search?q={1}'.format(SITE_URL, query))
    except requests.exceptions.ConnectionError:
        return []

    info = gen_search.json()
    search_results = []
    for result in info:
        search_results.append(Screencap(result, frink))

    return search_results

def random(frink = True):
    """Returns a random screencap object"""
    RANDOM_URL = FRINK_RANDOM_URL if frink else MORB_RANDOM_URL

    try:
        random_search = requests.get(RANDOM_URL)
    except requests.exceptions.ConnectionError:
        return []

    info = random_search.json()
    random_screen = {'Episode': info['Frame']['Episode'], 'Timestamp' : info['Frame']['Timestamp'], 'Id': info['Frame']['Id']}
    random_Screencap = Screencap(random_screen, frink)
    return random_Screencap