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
- Developed on Linux (while travelling through South-America), used on Ubuntu 18.04 and 20.04. Should work on all distro's (with changes to this install procedure).
- Download the ZIP file and unpack it *or* use `git clone`

         git clone https://github.com/Acknakxfer/simgal.git # using git; OR:
         unzip simgal-main.zip                              # if using ZIP
         cd simgal*                                         # simgal-main for ZIP file, simgal for git clone

- Move the contents of the Templates folder to a hidden folder in your $HOME directory

        [ -e ~/.simgal_templates ] && mv -i ~/.simgal_templates ~/.simgal_templates.org
        mv -i Templates ~/.simgal_templates

- Make the script excutable and put it in `/usr/bin`

         chmod 755 simgal.py
         sudo mv -i simgal.py /usr/bin/simgal

- Put a selection of your original (full-res) pictures in a separate directory anywhere on your filesystem (symlinks can be used to combine slides from different folders). The script will not change anything in this directory with your originals. See (OrgSlidePath) in the provided America_en.ini for an example.

- Change directories to the place where you keep your website (directory tree) and create a `slideshow` folder and at least one `.ini` file

        mkdir slideshow
        cd slideshow
        vi America_en.ini   # use the distributed one as example

- Edit the `.ini` to suit your needs: Language, GalleryTitle, TemplatePath, source path to images (OrgSlidePath), resolutions. *And* one line for each slide (with optional captions)
- Make sure you have `python3`, `exiftool` (from `libimage-exiftool-perl`) and `convert` (from `imagemagick`) installed

## Usage:
- Generate a first (test) batch:

        simgal --numbers --verbose --verbose America_en.ini

- Open the index page straight from the filesystem: `firefox simgal_en/index.html`
- Or, if you have a local HTTP server (that opens `index.html` when passed a directory): `http://localhost/<website path>/slideshow/simgal_en/`

The script accepts these options:

- **--force** will (re)generate all HTML files and (re)copy the CSS and SVGs. This will mostly result in generating files that are identical to the existing ones but with a later timestamp, causing a new transfer to the web server (annoying when you're using slow internet while travelling). By default (without *--force*), only the first and last HTML will be regenerated, allowing for extensions (at the end) to existing, published slideshows (which will occur if you publish while you travel). Should you find a (published) typo in a caption: manually remove *only* the corresponding HTML file - the script will automatically regenerate 'missing' HTMLs.
- **--convert** will similarly re-convert all JPGs. This is costly, in (local) CPU time and it *will* cause a major transfer to the web server.
- **--numbers** will substitute *slidenumber / slidecount* for all slides that do not have a caption.
- **--verbose** Increases output (repeat for more output).
- **--debug** Adds the resolution in text to the JPGs (so one can see what resolution is served on small(er) screens). Probably best with *--convert*.
- **--help** will print a help message

## Warning:
This the first Python (and HTML5) code I ever wrote. I'd appreciate if you'd let me know if you find issues or when you have suggestions.

<!-- 
# name		: $RCSfile: README.md,v $ $Revision: 1.7 $
# issued	: $Date: 2021/01/04 10:15:10 $
# id		: $Id: README.md,v 1.7 2021/01/04 10:15:10 adriaan Exp $

# vim:set textwidth=0 ft=markdown:
-->
