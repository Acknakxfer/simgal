# simgal
Simple Gallery: A generator (in Python) for static HTML5 slide files with geolocation (but no Java, no PHP)

## Design goals:
- Generate (responsive) HTML5 files that require NO Java, PHP or other stuff. Just static HTML
- Keep HTML code in templates: don't make the generator spit out HTML
- Support for more than one (human) language (but re-use the image files) and make machine translation easy
- Support for geolocation (if the image has GPS coordinates)
- Optimize image size for the viewers screen
- Generate an index file (that is called index.html) and have everything neatly in one directory (with sub-dirs)

## Reasoning:
I have used a few 'slide shows' to be included on my website and had problems with changing PHP or HTML versions, changing Apache configs, poorly maintained code, code that mixes languages (PHP and HTML), etc. I just want to show (some) pictures with a (multi-lingual) caption, minimal navigation and an URL to show a geolocation. I'm OK with having a separate HTML file for each picture, but the directories need to be separate.

## Example:
A slideshow of our trip through [South America in 2018](https://www.choam.com/2018_uy-co/slideshow/simgal_en). The same in Dutch: [Zuid-Amerika in 2018](https://www.choam.com/2018_uy-co/slideshow/simgal_nl)

## How to use:
- Create a directory for your templates

        mkdir ~/.simgal_templates
- Copy `simgal_index_template.html`, `simgal_slide_template.html`, `simgal.css` and `map-pin.svg` into it
- Change directories to the place where you keep your website (directory tree) and create `slideshow`

        mkdir slideshow
        cd slideshow
- Copy `simgal.py` and `America_en.ini` into it and edit to suit your needs
- Start generating:

        ./simgal.py --verbose --verbose America_en.ini
- Start browsing at `http://<website directory tree>/slideshow/simgal_en` (assuming your language is `en`)
