# simgal
Simple Gallery: A generator (in Python) for static HTML5 slide files with geolocation (but no Java, no PHP)

## Design goals:
- Generate (responsive) HTML5 files that require NO Java, PHP or other stuff. Just static HTML
- Keep HTML code in templates: don't make the generator spit out HTML
- Support different JPG resolutions to be able to optimize the served image size for the viewer's screen
- Support for more than one (human) language (but re-use the image files) and make machine translation easy
- Support for geolocation (if the image has GPS coordinates)
- Generate an index file (that is called index.html) and have everything neatly in one directory (with sub-dirs)
- Avoid unnecessary uploads to the web server after extensions (do not re-generate HTML or re-convert JPGs unless instructed) 

## Reasoning:
I have used a few 'slide shows' to be included on my website and had problems with changing PHP or HTML versions, changing Apache configs, poorly maintained code, code that mixes languages (PHP and HTML), etc. I just want to show (some) pictures with a (multi-lingual) caption, minimal navigation and an URL to show a geolocation and **never worry about it again**. (The oldest part of my website is 20+ years old and I've gotten tired of going back in and maintaining stuff because something broke a slideshow.) I'm OK with having a separate HTML file for each picture. I do like to keep file types and languages in separate sub-directories.

## Example:
A slideshow of our trip through [South America in 2018](https://www.choam.com/2018_uy-co/slideshow/simgal_en). The same in Dutch: [Zuid-Amerika in 2018](https://www.choam.com/2018_uy-co/slideshow/simgal_nl)

## How to 'install':
- Developed on Linux (while travelling through South-America), used on Ubuntu 18.04 and 20.04
- Make sure you have `exiftool` (from `libimage-exiftool-perl`), `convert` (from `imagemagick`) and `python3` installed
- Put your selection of your original (full-res) pictures in a separate directory anywhere on your filesystem (symlinks OK). This directory will be read but not altered in any way. 
- Create a directory for your templates

        mkdir ~/.simgal_templates

- Copy `simgal_index_template.html`, `simgal_slide_template.html`, `simgal.css` and all `.svg`s into it
- Change directories to the place where you keep your website (directory tree) and create `slideshow`

        mkdir slideshow
        cd slideshow

- Copy `simgal.py` and `America_en.ini` into it and edit to suit your needs: language, title, source dir with images, resolutions. AND one line for each slide (with optional captions)
- Start generating:

        python3 simgal.py --verbose --verbose America_en.ini

- Open the index page straight from the filesystem: `firefox file://<website path>/slideshow/simgal_en/index.html` (Note that if `<website path>` starts with a `/`, there will be a total of 3 of slashes ('/'))
- Or, if you have a local HTTP server (that opens `index.html` when passed a directory): `http://localhost/<website path>/slideshow/simgal_en/`

## Usage:
The script accepts these options:

- **--force** will (re)generate all HTML files and (re)copy the CSS and SVGs. This will mostly result in generating files that are identical to the existing ones but with a later timestamp, causing a new transfer to the web server (annoying when you're using slow internet while travelling). By default (without *--force*), only the first and last HTML will be regenerated, allowing for extensions (at the end) to existing, published slideshows (which will occur if you publish while you travel). Should you find a (published) typo in a caption: manually remove *only* the corresponding HTML file - the script will automatically regenerate 'missing' HTMLs.
- **--convert** will similarly re-convert all JPGs. This is costly, in (local) CPU time and it *will* cause a major transfer to the web server.
- **--numbers** will substitute *slidenumber / slidecount* for all slides that do not have a caption.
- **--verbose** Increases output (repeat for more output).
- **--debug** Adds the resolution in text to the JPGs (so one can see what resolution is served on small(er) screens). Probably best with *--convert*.
- **--help** will print a help message

## Warning:
This the first Python (and HTML5) code I ever wrote.

<!-- 
# name		: $RCSfile: README.md,v $ $Revision: 1.5 $
# issued	: $Date: 2021/01/03 13:55:37 $
# id		: $Id: README.md,v 1.5 2021/01/03 13:55:37 adriaan Exp $

# vim:set textwidth=0 ft=markdown:
-->
