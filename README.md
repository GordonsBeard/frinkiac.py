# Frinkiac.py
A Python wrapper for the [Frinkiac](http://frinkiac.com) and [Morbotron](http://morbotron.com) search engines.

   
####Example:

    from Frinkiac import search
    screenshot = search('them fing')
    screenshot.image_url()
    screenshot.meme_url()

`Screencap.image_url()` 
Returns a URL string of the image sans caption.

`Screencap.meme_url(caption)` Returns a URL string with the caption provided. If no caption is provided it will return the approprate subtitle for the scene.

Once `image_url()` or `meme_url()` is hit then the Screencap object fills with the details of the scene itself:

    .ep_title, .season, .ep_number, .director, 
    .writer, .org_air_date, .wiki_link

You can also get a random Screencap object by hitting `frinkiac.random()`

####Morbotron:
Just pass "False" along to the initial `.search()` or `.random()`

    from Frinkiac import random
	screenshot = random(False).meme_url()

####Thanks:
* [chanko](https://github.com/chanko/) for his [Frinkiac Ruby wrapper](https://github.com/chanko/frinkiac) I basically backward engineered.