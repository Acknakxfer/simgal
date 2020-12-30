# simgal
Simple Gallery: A generator (in Python) for static HTML5 slide files with geolocation (but no Java, no PHP)

## Design goals:
- Generate (responsive) HTML5 files that require NO Java, PHP or other stuff. Just static HTML
- Keep HTML code in templates: don't make the generator spit out HTML
- Support for more than one (human) language (but re-use the image files) and make machine translation easy
- Support for geolocation (if the image has GPS coordinates)
- Optimize served image size for the viewer's screen
- Generate an index file (that is called index.html) and have everything neatly in one directory (with sub-dirs)

## Reasoning:
I have used a few 'slide shows' to be included on my website and had problems with changing PHP or HTML versions, changing Apache configs, poorly maintained code, code that mixes languages (PHP and HTML), etc. I just want to show (some) pictures with a (multi-lingual) caption, minimal navigation and an URL to show a geolocation and never worry about it again. (The oldest part of my website is 20+ years old and I've gotten tired of going back in and maintaining stuff because something broke my slideshow.) I'm OK with having a separate HTML file for each picture. I do like to keep file types and languages in separate sub-directories.

## Example:
A slideshow of our trip through [South America in 2018](https://www.choam.com/2018_uy-co/slideshow/simgal_en). The same in Dutch: [Zuid-Amerika in 2018](https://www.choam.com/2018_uy-co/slideshow/simgal_nl)

## How to use:
- Developed on Linux (while travelling), used on Ubuntu 18.04 and 20.04
- Make sure you have `exiftool` (from `libimage-exiftool-perl`), `convert` (from `imagemagick`) and `python3` installed
- Put your selection of your original (full-res) pictures in a separate directory anywhere on your filesystem (symlinks OK). This directory will be read but not altered in any way. 
- Create a directory for your templates

        mkdir ~/.simgal_templates
- Copy `simgal_index_template.html`, `simgal_slide_template.html`, `simgal.css` and `map-pin.svg` into it
- Change directories to the place where you keep your website (directory tree) and create `slideshow`

        mkdir slideshow
        cd slideshow
- Copy `simgal.py` and `America_en.ini` into it and edit to suit your needs: language, title, source dir with images, resolutions. AND one line for each slide (with optional captions)
- Start generating:

        ./simgal.py --verbose --verbose America_en.ini
- Open the index page straight from the filesystem: `firefox file://<website path>/slideshow/simgal_en/index.html` (Note that `<website path>` starts with a `/`, giving a total of 3 of them)
- Or, if you have a local HTTP server (that opens `index.*` when passed a directory): `http://localhost/<website path>/slideshow/simgal_en/`

## Warning:
This the first Python (and HTML5) code I ever wrote.


<!-- 
# name		: $RCSfile: README.md,v $ $Revision: 1.2 $
# issued	: $Date: 2020/12/30 09:05:24 $
# id		: $Id: README.md,v 1.2 2020/12/30 09:05:24 adriaan Exp $

# vim:set textwidth=0 ft=markdown:
-->
