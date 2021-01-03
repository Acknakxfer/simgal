#!/usr/bin/python3
#
# name        : $RCSfile: simgal.py,v $ $Revision: 1.11 $
# issued      : $Date: 2021/01/03 13:36:19 $
# description : Simple Gallery generator
#
# id          : $Id: simgal.py,v 1.11 2021/01/03 13:36:19 adriaan Exp $
#
# NOTE that this works with Python version 3.5 and up.
# TODO sanitize Google Maps URL? (see below)

# IMPORTS
import os, argparse, shutil, subprocess, sys
# to read ini files:
from configparser import RawConfigParser, ExtendedInterpolation
# to fill out templates:
from string import Template

# Define and set slide defaults in a dictionary
configdict = { 'Language': 'en',
    'GalleryTitle': 'Simple Gallery',
    'IndexTemplate': 'simgal_index_template.html',
    'SlideTemplate': 'simgal_slide_template.html',
    'CSSTemplate' : 'simgal.css',
    'ThumbResolution': '200x200' }
# The HTML templates use more values: 'SmallResolution': '850x850',
# 'MediumResolution': '1280x1280', 'LargeResolution': '1920x1920'. Their values
# can be specified in the ini file. If they are not specified, one could remove
# the corresponding reference in the template.

# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("configfile", help="The name of an .ini file containing the settings and filenames of the slideshow")
parser.add_argument("-f", "--force", action="store_true", default=False, help="Force overwriting all HTML, CSS and SVG files")
parser.add_argument("-c", "--convert", action="store_true", default=False, help="Force (re)conversion of all JPG files")
parser.add_argument("-n", "--numbers", action="store_true", default=False, help="Add a \"slide #/count #\" to slides without caption")
parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase progress output (repeat for more)")
parser.add_argument("-d", "--debug", action="store_true", default=False, help="Add the resolution (in text) to the pictures (for HTML debugging purposes)")
args = parser.parse_args()

# Copy the ini file into a dict-like structure:
iniconfig = RawConfigParser(allow_no_value=True,interpolation=ExtendedInterpolation())
iniconfig.optionxform = str # this makes the ini file vars case-sensitive
# Read the config file (passed as an argument)
iniconfig.read(args.configfile)
# Copy the options (from the 'Slide Info' section) into our dictionary:
for option in iniconfig.options('Slide Config'):
    configdict[option] = iniconfig.get('Slide Config', option)

# Make the output directory
htmldir='simgal_'+str(configdict['Language'])
if not os.path.exists(htmldir):
    os.makedirs(htmldir)
    os.chmod(htmldir, 0o755)
# Make the directories for the scaled images
for resolution in iniconfig.options('Resolutions'):
    configdict[resolution] = iniconfig.get('Resolutions', resolution)
    if not os.path.exists(iniconfig['Resolutions'][resolution]):
        os.makedirs(iniconfig['Resolutions'][resolution])
        os.chmod(iniconfig['Resolutions'][resolution], 0o755)

# Make sure path(s) form config file are OK; ABORT if one is missing
if not os.path.exists(configdict['OrgSlidePath']):
    sys.exit('Error: path to original slides (OrgSlidePath: '+configdict['OrgSlidePath']+') is invalid')
if not os.path.exists(configdict['IndexTemplate']):
    sys.exit('Error: index template file path (IndexTemplate: '+configdict['IndexTemplate']+') is invalid')
if not os.path.exists(configdict['SlideTemplate']):
    sys.exit('Error: slide template file path (SlideTemplate: '+configdict['SlideTemplate']+') is invalid')
if not os.path.exists(configdict['CSSTemplate']):
    sys.exit('Error: CSS template file path (CSSTemplate: '+configdict['CSSTemplate']+') is invalid')

# (re)copy the CSS file into the output dir; set to 644
cssdest=os.path.join(htmldir, os.path.basename(configdict['CSSTemplate']))
# remove existing CSS (if 'force' was requested)
if os.path.exists(cssdest) and args.force == True:
    os.remove(cssdest)
# put a new one in place
if not os.path.exists(cssdest):
    shutil.copy(configdict['CSSTemplate'], cssdest)
# set it to 644
os.chmod(cssdest, 0o644)

# copy all SVG files to the HTML destination directory.
svgfiles = [ 'map-pin.svg', 'arrow-up.svg', 'arrow-down.svg', 'arrow-left.svg', 'arrow-right.svg' ]
for svg in svgfiles:
    # complain if SVG doesn't exist, but go on (generated HTML will be valid)
    svgsource=os.path.join(configdict['TemplatePath'], svg)
    if not os.path.exists(svgsource):
        print('Error: SVG file ('+svgsource+') is missing; continuing')
        continue
    # (re)copy SVG (from 'svgsource', above)
    svgdest=os.path.join(htmldir, svg)
    # remove existing SVG for destination (if 'force' was requested)
    if os.path.exists(svgdest) and args.force == True:
        os.remove(svgdest)
    if not os.path.exists(svgdest):
        shutil.copy(svgsource, svgdest)
    # set it to 644
    os.chmod(svgdest, 0o644)

# Define a list of tuples: each tuple holds the trunk of the slidename[0], the
# extension of the slidename [1], the caption for that slide [2] and the
# gpsposition [3] in the array slidelist[]
slidelist = []
if args.verbose >= 1:
    if args.convert:
        print('Converting ALL slides')
    else:
        print('Converting NEW slides')
# Iterate all slides in the 'Slides' section, make tuples in the slidelist and scale the images
for slide in iniconfig['Slides']:
    if args.verbose >= 2:
        print('Checking/converting: ', slide)
    jpgsource = os.path.join(configdict['OrgSlidePath'], slide)
    if not os.path.exists(jpgsource):
        print("File ",jpgsource," does NOT exist and will be skipped.")
        continue

    # Extract GPS location from the file (if any)
    cmd='exiftool -gpsposition -c \"%+.6f\" \"'+jpgsource+'\"'
    gpsposition=(subprocess.check_output(cmd, shell=True)).decode("UTF-8")
    # clean up string, remove whitespace and leading "GPS Position                    : " string
    gpsposition=gpsposition.strip()
    gpsposition=gpsposition.replace('GPS Position                    : ', '')
    gpsposition=gpsposition.replace(' ', '')
    if args.verbose >= 2:
        print('GPS Location found: ', gpsposition)

    # append a tuple with the (truncated) slide name and the caption to the list
    slidelist.append((os.path.splitext(slide)[0],os.path.splitext(slide)[1],iniconfig['Slides'][slide],gpsposition))
    # start scaling to the 4 resolutions
    for resolution in iniconfig['Resolutions']:
        target=os.path.join(iniconfig['Resolutions'][resolution],slide)
        if os.path.exists(target) and args.convert == False:
            continue # when the file is already there AND no new conversion was requested
        if args.debug == False:
            # convert the file
            cmd='convert \"'+jpgsource+'\" -geometry '+iniconfig['Resolutions'][resolution]+' \"'+target+'\"'
        else:
            # convert the file, but put the resolution in the file (for HTML5 debugging)
            cmd='convert \"'+jpgsource+'\" -geometry '+iniconfig['Resolutions'][resolution]+' -font Arial -pointsize 50 -draw \"gravity north fill black text 0,12 res_'+iniconfig['Resolutions'][resolution]+' fill white text 1,11 res_'+iniconfig['Resolutions'][resolution]+'\" \"'+target+'\"'
        if args.verbose >= 2:
            print('Now running: ', cmd)
        subprocess.run(cmd, shell=True)
        # make sure Apache can read it
        os.chmod(target, 0o644)
    # make a blurred version (in the thumbnail resolution)
    blur=os.path.join(iniconfig['Resolutions']['ThumbResolution'],os.path.splitext(slide)[0]+'_blur'+os.path.splitext(slide)[1])
    if os.path.exists(blur):
        continue # when the file is already there
    cmd='convert \"'+jpgsource+'\" -geometry '+iniconfig['Resolutions']['ThumbResolution']+' -blur 0x5 \"'+blur+'\"'
    if args.verbose >= 2:
        print('Now running: ', cmd)
    subprocess.run(cmd, shell=True)
    # make sure Apache can read it
    os.chmod(blur, 0o644)

# Set up the (first part of the) index file
indexfile=open(os.path.join(htmldir,'index.html'), 'w')
if args.verbose >= 1:
    print('Prepare (first part) of the index HTML file')
indexlist=[]
matched=False
# Dirty: make the very first slide available as $CurrentSlide
configdict['CurrentSlide']=slidelist[0][0]
with open(configdict['IndexTemplate'], 'r') as indextempl:
    for line in indextempl:
        if 'simgal: end of slide' in line:
            break
        if matched:
            indexlist.append(line)
        else: 
            if 'simgal: start of slide' in line:
		# notice that the line containing <!-- simgal: start of slide --> is removed
		# make sure there is NO other HTML on these lines!
                matched=True
            else:
                # print(Template(line).safe_substitute(configdict), end="")
                indexfile.write(Template(line).safe_substitute(configdict))

# Now generate the individual HTML files for each slide
if args.verbose >= 1:
    print('Generate one HTML file for each slide')
maxx=len(slidelist)
configdict['SlideCount']=len(slidelist)
configdict['PreviousSlide']=slidelist[maxx-1][0]
for x in range(0, maxx):
    configdict['SlideNumber']=x+1
    configdict['CurrentSlide']=slidelist[x][0]
    configdict['CurrentSlideExt']=slidelist[x][1]

    # Take the caption from the ini file (if it was specified)
    if slidelist[x][2]:
        configdict['SlideCaption']=slidelist[x][2]
    else:
        if args.numbers == True:
            # display number and count of slides
            configdict['SlideCaption']=str(configdict['SlideNumber'])+' / '+str(configdict['SlideCount'])
        else:
            # display nothing
            configdict['SlideCaption']=""

    # Put the GPS Position in the configdict
    # TODO to worry about URL encoding, or not?
    if slidelist[x][3]:
        configdict['GPSPosition']=slidelist[x][3]
    else:
        configdict['GPSPosition']=""

    # on the last slide: point to the first slide, otherwise to the next slide
    if x == maxx-1:
        configdict['NextSlide']=slidelist[0][0]
    else:
        configdict['NextSlide']=slidelist[x+1][0]

    # Write from the in-core indexlist to the index file
    for line in indexlist:
        indexfile.write(Template(line).safe_substitute(configdict))

    # Determine the ACTUAL width of each image and store in our configdict as XXXXResolutionWidth
    for resolution in iniconfig['Resolutions']:
        target=os.path.join(iniconfig['Resolutions'][resolution],configdict['CurrentSlide']+configdict['CurrentSlideExt'])
        cmd='identify -format \'%w\' \"'+target+'\"'
        configdict[resolution+'Width']=int(subprocess.check_output(cmd, shell=True))

    # The first and last slides are always regenerated; if THIS slide AND the next slide exist, regeneration may be skipped.
    target=os.path.join(htmldir,configdict['CurrentSlide']+'.html')
    nexttarget=os.path.join(htmldir,configdict['NextSlide']+'.html')
    # write the file if it does not exist, if the NEXT file does not exist
    # (the current needs to point to that one), when it's the first or the last
    # (they point to each other too).
    if args.force == True or not os.path.exists(target) or not os.path.exists(nexttarget) or x == 0 or x == maxx-1:
        # Write the HTML file
        slidefile=open(target, 'w')
        if args.verbose >= 2:
            print('Writing: ', configdict['CurrentSlide']+'.html')
        with open(configdict['SlideTemplate'], 'r') as slidetempl:
            suppress=False # output every line from the template
            for line in slidetempl:
                # here, check for: "simgal: if geoloc" AND presence of geoposition from EXIF
                # if yes: insert next lines,
                # otherwise skip until "simgal: end of if geoloc" is found
                if not suppress and "simgal: if geoloc" in line and configdict['GPSPosition'] == "":
                    suppress=True
                # copy the line substituting vars from dictionary unless suppress is True
                if not suppress:
                    slidefile.write(Template(line).safe_substitute(configdict))
                if suppress and "simgal: end of if geoloc" in line:
                    suppress=False
        slidefile.close()
        # make sure Apache can read it
        os.chmod(target, 0o644)
        # end of if "force, this, next exists or first and last"
    # previous is the current for the next iteration
    configdict['PreviousSlide']=configdict['CurrentSlide']
    # end of for x from 0 to max slide number

# Wrapping up: finish the index.html file
# This is not efficient: we're re-reading the whole source index file. Fortunately it's small...
if args.verbose >= 1:
    print('Finishing index HTML file')
matched=False
with open(configdict['IndexTemplate'], 'r') as indextempl:
    for line in indextempl:
        if matched:
            # print(Template(line).safe_substitute(configdict), end="")
            indexfile.write(Template(line).safe_substitute(configdict))
        else:
            if 'simgal: end of slide' in line:
                matched=True
            continue
indexfile.close()
# make sure Apache can read it
os.chmod(os.path.join(htmldir,'index.html'), 0o644)

# vim:set textwidth=0 ft=python tabstop=8 softtabstop=0 expandtab shiftwidth=4 smarttab:
