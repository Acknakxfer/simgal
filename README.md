# simgal
Simple Gallery: A generator (in Python) for static HTML5 slide files with geolocation (but no Java, no PHP)

- Generate (responsive) HTML5 files that require NO Java, PHP or other stuff. Just static HTML
- Keep HTML code in templates: don't make the generator spit out HTML
- Support for more than one (human) language (but re-use the image files) and make machine translation easy
- Support for geolocation (if the image has GPS coordinates)
- Optimize image size for the viewers screen
- Generate an index file (that is called index.html) and have everything neatly in one directory (with sub-dirs)

I have used a few 'slide shows' to be included on my website and had problems with changing PHP or HTML versions, changing Apache configs, poorly maintained code, code that mixes languages (PHP and HTML), etc. I just want to show (some) pictures with a (multi-lingual) caption, minimal navigation and an URL to show a geolocation. I'm OK with having a separate HTML file for each picture, but the directories need to be separate.
