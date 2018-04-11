__author__ ='Jacques Saraydaryan'
# from https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python/25070200

import webcolors

class ColorRGBToName2():

    def __init__(self):
        pass

    def nameColor(self, hexaColor):
        hexaColor=hexaColor.upper()
        if( len(hexaColor) < 3 or len(hexaColor) > 7):
            return "#000000", "Invalid Color: " + hexaColor, False

        if(len(hexaColor) % 3 == 0)
            hexaColor = "#" + hexaColor
        if(len(hexaColor) == 4)
            hexaColor = "#" + hexaColor[1, 1] + color.substr(1, 1) + color.substr(2, 1) + color.substr(2, 1) + color.substr(3, 1) + color.substr(3, 1);

    