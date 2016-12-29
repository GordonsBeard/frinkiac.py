import unittest
import frinkiac

# 'them fing', first value
valid_init_dict = {'Episode': 'S13E16', 'Timestamp': 918584, 'Id': 1796916}
valid_image_url = 'https://frinkiac.com/img/S13E16/918584.jpg'
valid_meme_url = 'https://frinkiac.com/meme/S13E16/918584.jpg?b64lines=VGhleSBjYWxsIHRoZW0gZmluZ2VycywKYnV0IEkgbmV2ZXIgc2VlICdlbSBmaW5nLgpPaCwgdGhlcmUgdGhleSBnby4='
valid_caption = 'They call them fingers,\nbut I never see \'em fing.\nOh, there they go.'
hello_world_caption_url = 'https://frinkiac.com/meme/S13E16/918584.jpg?b64lines=SGVsbG8gV29ybGQh'
absurd_length_caption = 'It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way – in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only.'
absurd_length_caption_url = 'https://frinkiac.com/meme/S13E16/918584.jpg?b64lines=SXQgd2FzIHRoZSBiZXN0IG9mIHRpbWVzLAppdCB3YXMgdGhlIHdvcnN0IG9mCnRpbWVzLCBpdCB3YXMgdGhlIGFnZSBvZgp3aXNkb20sIGl0IHdhcyB0aGUgYWdlIG9mCmZvb2xpc2huZXNzLCBpdCB3YXMgdGhlCmVwb2NoIG9mIGJlbGllZiwgaXQgd2FzCnRoZSBlcG9jaCBvZiBpbmNyZWR1bGl0eSwKaXQgd2FzIHRoZSBzZWFzb24gb2YKTGlnaHQsIGl0IHdhcyB0aGUgc2Vhc29uCm9mIERhcmtuZXNzLCBpdCB3YXMgdGhlCnNwcmluZyBvZiBob3BlLCBpdCB3YXMKdGhlIHdpbnRlciBvZiBkZXNwYWlyLCB3ZQpoYWQgZXZlcnl0'

class Test_Frinkiac(unittest.TestCase):
    def test_Screencap_good_init(self):
        # Test the Screencap with known good init values
        testCap = frinkiac.Screencap(valid_init_dict)
        self.assertEqual(valid_image_url, testCap.image_url())

    def test_Search_image_url(self):
        # Test the Search for a single image url
        testSearch = frinkiac.search('them fing')[0]
        self.assertEqual(valid_image_url, testSearch.image_url())

    def test_Search_multiple(self):
        # Test the Search in case of multiple results
        testSearch = frinkiac.search('lazy saturday')
        self.assertEqual(len(testSearch), 36)
        for result in testSearch:
            if isinstance(result, frinkiac.Screencap):
                success = True
            else:
                self.fail("Was returned a non-Screencap object!")
        self.assertTrue(success)

    def test_Seach_no_results(self):
        # Test the Search in case of no results
        testSearch = frinkiac.search('asdf')
        self.assertEqual(len(testSearch), 0)

    def test_Search_meme_url(self):
        # Test the Search to see if it can bring back a captioned image
        testSearch = frinkiac.search('them fing')[0]
        self.assertEqual(valid_meme_url, testSearch.meme_url())

    def test_Meme_url_custom_caption_short(self):
        # Tests the Meme URL's support of a custom caption
        testSearch = frinkiac.search('them fing')[0]
        caption_url = testSearch.meme_url('Hello World!')
        self.assertEqual(hello_world_caption_url, caption_url)

    def test_Meme_url_custom_caption_long(self):
        # Tests the Meme URL's support of a custom caption
        testSearch = frinkiac.search('them fing')[0]
        caption_url = testSearch.meme_url(absurd_length_caption)
        self.assertEqual(absurd_length_caption_url, caption_url)

    def test_Caption_slicing(self):
        # Make sure the captions are split on 25 characters
        testSearch = frinkiac.search('them fing')[0]
        testSearch.image_url()
        self.assertEqual(valid_caption, testSearch.caption)

if __name__ == '__main__':
    unittest.main()