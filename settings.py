import time

# window size
WIDTH = 650
HEIGHT = 650

# grid
GRIDCOOR = (150,150)
GRIDDIM = (450,450)
BLANK = [[0 for i in range(9)] for i in range(9)]
DEFAULTBOARD = [[7,0,0,0,0,9,2,1,0],
                [0,0,0,7,3,4,0,0,0],
                [0,3,0,1,0,8,0,4,6],
                [0,9,0,3,0,0,8,2,0],
                [2,0,0,0,1,0,0,0,4],
                [0,1,8,0,0,2,0,7,0],
                [9,4,0,6,0,1,0,5,0],
                [0,0,0,9,4,7,0,0,0],
                [0,7,6,2,0,0,0,0,8]]
FINISHED = [[0,3,4,6,7,8,9,1,2],
            [6,7,2,1,9,5,3,4,8],
            [1,9,8,3,4,2,5,6,7],
            [8,5,9,7,6,1,4,2,3],
            [4,2,6,8,5,3,7,9,1],
            [7,1,3,9,2,4,8,5,6],
            [9,6,1,5,3,7,2,8,4],
            [2,8,7,4,1,9,6,3,5],
            [3,4,5,2,8,6,1,7,9]]

# button
BUTTONDIM = (100, 50)

# border thickness
MAINBORDER = 3
INNERBORDER = 1

# cell size
CELLSIZE = GRIDDIM[0] // 9

# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (80,80,80)
LIGHTGREY = (180,180,180)
LIGHTPURPLE = (195,195,255)
PURPLE = (240,150,250)
LIGHTBLUE = (160,224,248)
LIGHTRED = (255,100,100)
LIGHTGREEN = (100,200,100)


# cell colors
SELECTEDCELLCOLOR = PURPLE
INCORRECTCELLCOLOR = LIGHTRED
BUTTONCOLOR = (80,80,80)

# other
TIMEDELAY = 2

# font
FONT = 'inkfree'
FONTSIZE = 25

# available fonts
# 'arial', 'arialblack', 'bahnschrift', 'calibri', 'cambriacambriamath',
# 'cambria', 'candara', 'comicsansms', 'consolas', 'constantia', 'corbel',
# 'couriernew', 'ebrima', 'franklingothicmedium', 'gabriola', 'gadugi',
# 'georgia', 'impact', 'inkfree', 'javanesetext', 'leelawadeeui',
# 'leelawadeeuisemilight', 'lucidaconsole', 'lucidasans', 'malgungothic',
# 'malgungothicsemilight', 'microsofthimalaya',
# 'microsoftjhengheimicrosoftjhengheiui',
# 'microsoftjhengheimicrosoftjhengheiuibold',
# 'microsoftjhengheimicrosoftjhengheiuilight',
# 'microsoftnewtailue', 'microsoftphagspa', 'microsoftsansserif',
# 'microsofttaile', 'microsoftyaheimicrosoftyaheiui',
# 'microsoftyaheimicrosoftyaheiuibold', 'microsoftyaheimicrosoftyaheiuilight',
# 'microsoftyibaiti', 'mingliuextbpmingliuextbmingliuhkscsextb',
# 'mongolianbaiti', 'msgothicmsuigothicmspgothic', 'mvboli',
# 'myanmartext', 'nirmalaui', 'nirmalauisemilight', 'palatinolinotype',
# 'segoemdl2assets', 'segoeprint', 'segoescript', 'segoeui', 'segoeuiblack',
# 'segoeuiemoji', 'segoeuihistoric', 'segoeuisemibold', 'segoeuisemilight',
# 'segoeuisymbol', 'simsunnsimsun', 'simsunextb',
# 'sitkasmallsitkatextsitkasubheadingsitkaheadingsitkadisplaysitkabanner',
# 'sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold',
# 'sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic',
# 'sitkasmallsitkatextitalicsitkasubheadingitalicsitkaheadingitalicsitkadisplayitalicsitkabanneritalic',
# 'sylfaen', 'symbol', 'tahoma', 'timesnewroman', 'trebuchetms', 'verdana',
# 'webdings', 'wingdings', 'yugothicyugothicuisemiboldyugothicuibold',
# 'yugothicyugothicuilight', 'yugothicmediumyugothicuiregular',
# 'yugothicregularyugothicuisemilight', 'holomdl2assets']