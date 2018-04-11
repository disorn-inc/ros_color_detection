__author__ ='Jacques Saraydaryan'
# from https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python/25070200

import webcolors
from ColorRange import ColorRange

class ColorRGBToName():
    colorSimpleWebColorMap={}

    def __init__(self):
        self.configureColor()
        pass

    def getColorInformationName(self,r_original_color,r_modified_color):
        pass
        
        

    def closest_color(self,requested_color):
        min_colors = {}
        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_color[0]) ** 2
            gd = (g_c - requested_color[1]) ** 2
            bd = (b_c - requested_color[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        return min_colors[min(min_colors.keys())]

    def get_color_name(self, requested_colour):
        try:
            closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
        except ValueError:
            closest_name = self.closest_color(requested_colour)
            actual_name = None
        return actual_name, closest_name


    def black_white_gray_detector(self,H,S,V):
        if V <= 18:
            return "BLACK"
        elif S <= 20  and (V > 26 and V <= 70):
             return "GRAY"

        if S<=20 and V >= 70:
            return "WHITE"

        if S <= 20 and (V > 18 and V <= 48):
            return "DARK"

        return None
    
    def configureColor(self):
        self.colorSimpleWebColorMap["PINK"]=['PINK','LIGHTPINK','HOTPINK','DEEPPINK','PALEVIOLETRED','MEDIUMVIOLETRED']
        self.colorSimpleWebColorMap["RED"]=['LIGHTSALMON','SALMON','DARKSALMON','LIGHTCORAL','INDIANRED','CRIMSON','FIREBRICK','DARKRED','RED']
        self.colorSimpleWebColorMap["ORANGE"]=['ORANGERED','TOMATO','CORAL','DARKORANGE','ORANGE']
        self.colorSimpleWebColorMap["YELLOW"]=['YELLOW','LIGHTYELLOW','LEMONCHIFFON','LIGHTGOLDENRODYELLOW','PAPAYAWHIP','MOCCASIN','PEACHPUFF','PALEGOLDENROD','KHAKI','DARKKHAKI','GOLD']
        self.colorSimpleWebColorMap["BROWN"]=['CORNSILK','BLANCHEDALMOND','BISQUE','NAVAJOWHITE','WHEAT','BURLYWOOD','TAN','ROSYBROWN','SANDYBROWN','GOLDENROD','DARKGOLDENROD','PERU','CHOCOLATE','SADDLEBROWN','SIENNA','BROWN','MAROON']
        self.colorSimpleWebColorMap["GREEN"]=['DARKOLIVEGREEN','OLIVE','OLIVEDRAB','YELLOWGREEN','LIMEGREEN','LIME','LAWNGREEN','CHARTREUSE','GREENYELLOW','SPRINGGREEN','MEDIUMSPRINGGREEN' ,'LIGHTGREEN','PALEGREEN','DARKSEAGREEN','MEDIUMAQUAMARINE','MEDIUMSEAGREEN','SEAGREEN','FORESTGREEN','GREEN','DARKGREEN']
        self.colorSimpleWebColorMap["CYAN"]=['AQUA','CYAN','LIGHTCYAN','PALETURQUOISE','AQUAMARINE','TURQUOISE','MEDIUMTURQUOISE','DARKTURQUOISE','LIGHTSEAGREEN','CADETBLUE','DARKCYAN','TEAL']
        self.colorSimpleWebColorMap["BLUE"]=['LIGHTSTEELBLUE','POWDERBLUE','LIGHTBLUE','SKYBLUE','LIGHTSKYBLUE','DEEPSKYBLUE','DODGERBLUE','CORNFLOWERBLUE','STEELBLUE','ROYALBLUE','BLUE','MEDIUMBLUE','DARKBLUE','NAVY','MIDNIGHTBLUE']
        self.colorSimpleWebColorMap["PURPLE"]=['LAVENDER','THISTLE','PLUM','VIOLET','ORCHID','FUCHSIA','MAGENTA','MEDIUMORCHID','MEDIUMPURPLE','BLUEVIOLET','DARKVIOLET','DARKORCHID','DARKMAGENTA','PURPLE','INDIGO','DARKSLATEBLUE','SLATEBLUE','MEDIUMSLATEBLUE']
        self.colorSimpleWebColorMap["WHITE"]=['WHITE','SNOW','HONEYDEW','MINTCREAM','AZURE','ALICEBLUE','GHOSTWHITE','WHITESMOKE','SEASHELL','BEIGE''OLDLACE','FLORALWHITE','IVORY','ANTIQUEWHITE','LINEN','LAVENDERBLUSH','MISTYROSE']
        self.colorSimpleWebColorMap["GRAY"]=['GAINSBORO','LIGHTGRAY','SILVER','DARKGRAY','GRAY']
        self.colorSimpleWebColorMap["BLACK"]=['DIMGRAY','LIGHTSLATEGRAY','SLATEGRAY','DARKSLATEGRAY','BLACK']

    def simpleColor(self,web_color_name):
        for maincolor in self.colorSimpleWebColorMap.keys():
            if web_color_name in self.colorSimpleWebColorMap[maincolor]:
                return maincolor
        return None

#requested_colour = (119, 172, 152)
#actual_name, closest_name = get_color_name(requested_colour)