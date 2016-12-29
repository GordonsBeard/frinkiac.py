import unittest
import frinkiac

# 'them fing', first value
valid_init_dict = {'Episode': 'S13E16', 'Timestamp': 918584, 'Id': 1796916}
valid_image_url = 'https://frinkiac.com/img/S13E16/918584.jpg'
valid_meme_url = 'https://frinkiac.com/meme/S13E16/918584.jpg?b64lines=VGhleSBjYWxsIHRoZW0gZmluZ2VycywKYnV0IEkgbmV2ZXIgc2VlICdlbSBmaW5nLgpPaCwgdGhlcmUgdGhleSBnby4='
valid_caption = 'They call them fingers,\nbut I never see \'em fing.\nOh, there they go.'

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

    def test_Caption_slicing(self):
        # Make sure the captions are split on 25 characters
        testSearch = frinkiac.search('them fing')[0]
        testSearch.image_url()
        self.assertEqual(valid_caption, testSearch.caption)

if __name__ == '__main__':
    unittest.main()