import base64
import json
import requests
import textwrap

SITE_URL = 'https://frinkiac.com'
API_URL = '{0}/api/search'.format(SITE_URL)
CAPTION_URL = '{0}/api/caption'.format(SITE_URL)

class Screencap(object):
    def __init__(self, values):
        self.episode = values['Episode']
        self.timestamp = values['Timestamp']
        self.id = values['Id']

        # These get filled out when you hit _get_details
        self.caption = None
        self.ep_title = None
        self.season = None
        self.ep_number = None
        self.director = None
        self.writer = None
        self.org_air_date = None
        self.wiki_link = None

    def __repr__(self):
        try:
            ep = self.episode
            time = self.timestamp
            title = self.ep_title
        except AttributeError:
            self._get_details()
        finally:
            return 'Episode: {0} "{1}"'.format(self.episode, self.ep_title)

    def image_url(self):
        if self.director is None:
            self._get_details()
        return '{0}/img/{1}/{2}.jpg'.format(SITE_URL, self.episode, self.timestamp)

    def meme_url(self, caption = None):
        if self.caption is None:
            self._get_details()

        if caption is None:
            caption = self.caption

        return '{0}/meme/{1}/{2}.jpg?b64lines={3}'.format(
            SITE_URL, 
            self.episode, 
            self.timestamp, 
            base64.b64encode(bytes(caption, 'utf-8')).decode('ascii'))

    def _get_details(self):
        cap_search = requests.get('{0}?e={1}&t={2}'.format(CAPTION_URL, self.episode, self.timestamp))
        data = cap_search.json()
        caption = " ".join([subtitle['Content'] for subtitle in data['Subtitles']])
        chopped_captions = textwrap.fill(caption, 25)
        self.caption = chopped_captions
        self.ep_title = data['Episode']['Title']
        self.season = data['Episode']['Season']
        self.ep_number = data['Episode']['EpisodeNumber']
        self.director = data['Episode']['Director']
        self.writer = data['Episode']['Writer']
        self.org_air_date = data['Episode']['OriginalAirDate']
        self.wiki_link = data['Episode']['WikiLink']

def search(query):
    """Returns a list of Screencap objects based on the string provided.
    
    Example:
        from Frinkiac import search
        screenshot = search('them fing')
        screenshot.image_url()
        screenshot.meme_url()

    Once image_url() or meme_url() is hit then the Screencap object fills with:
    self.ep_title, .season, .ep_number, .director, .writer, .org_air_date, .wiki_link
    """

    try:
        gen_search = requests.get('https://frinkiac.com/api/search?q={0}'.format(query))
    except requests.exceptions.ConnectionError:
        return []

    info = gen_search.json()
    search_results = []
    for result in info:
        search_results.append(Screencap(result))

    return search_results