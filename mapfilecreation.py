#!/usr/bin/env python
import os, glob, re, datetime, sys

class Mapfile():
    def __init__(self, wms_title, directory, tiled):
        self.mappath = directory + wms_title + ".map"
        header =  self.header(wms_title)
        if tiled:
          self.filelist = glob.glob(directory + '*.shp')
          body = self.body_mapfile(tiled)
        else:
          self.filelist = glob.glob(directory + '*.tif')
          self.filelist += glob.glob(directory + '*.ecw')
          self.filelist.sort()
          body = self.body_mapfile(tiled)

    def header(self, wms_title):
            '''Function to create the header of the mapfile. Containing title, url and EPSG'''
            wmap = open(self.mappath, 'w')
            wmap.write('''
MAP
NAME "''' + str(wms_title) + '''"

WEB
  IMAGEPATH "/www/"
  IMAGEURL "/www/"
  METADATA
    "wms_title"     "''' + str(wms_title) + '''"  
    "wms_enable_request" "*"
    "wms_onlineresource" "http://babbage/cgi-bin/mapserv?map=''' + str(self.mappath) + '''&"
    "wms_srs"       "epsg:28992"
  END
END
FONTSET "/var/maps/fontset.txt"

PROJECTION
  "init=epsg:28992"   ##required
END
             ''')
            wmap.close()

    def body_mapfile(self, tiled):
        from osgeo import gdal
        filelist = self.filelist
        wmap = open(self.mappath, 'r+')
        wmap.readlines()
        for file in filelist:
            projection = str(28992)  #proj.pop()
            nodata = 0
            (filedir, filename) = os.path.split(file)
            layername = re.split('[.]', filename)[0]
            wmap.write("""
LAYER
  NAME '""" + layername + """'
      METADATA
      "wms_title"   '""" + layername + """'
      END
  TYPE RASTER
  STATUS ON""")

            if not tiled:
                wmap.write("""
  DATA  '""" + str(file) + """'""")
            elif tiled:
                wmap.write("""
  TILEINDEX  '""" + str(file) + """'
  TILEITEM 'LOCATION'""")
            wmap.write("""
  PROJECTION
  "init=epsg:""" + projection + """"   ##required
  END
  PROCESSING "NODATA=""" + str(int(nodata)) + """"
  PROCESSING "OVERSAMPLE_RATIO=1.0"
  PROCESSING "RESAMPLE=AVERAGE"
END

            """)
        wmap.write("""
# LAYER
#   NAME "copyright"                      # we should always have one layer "base"
#   METADATA
#     "wms_title"     "copyright"
#   END
#   STATUS DEFAULT
#   TYPE ANNOTATION

#   TRANSFORM ll #set the image origin to be lower left
#   FEATURE
#     POINTS
#       100 -100 #set the offset from lower left position in pixels
#     END
#     TEXT " (c) 2012 NEO" #this is the displaying text
#   END
#   CLASS
#     LABEL #defines the font, colors etc. of the text
#       TYPE truetype
#       FONT "PTSans"
#       SIZE 9
#       COLOR 0 0 0
#       FORCE TRUE

#     END
#   END
#   UNITS PIXELS #sets the units for the feature object
# END

END""")
        wmap.close()


def main(wms_title, directory, tiled):
    instantiate = Mapfile(wms_title, directory, tiled)

if __name__ == "__main__":
    wms_title, directory = str(sys.argv[1]), str(sys.argv[2])
    try:
        if sys.argv[3] == 'tiled':
            tiled = True
    except:
        tiled = False
    main(wms_title, directory, tiled)
