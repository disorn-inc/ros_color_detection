__author__ ='Jacques Saraydaryan'


class ColorRange():
    min_H=0
    max_H=0
    label=''

    def getColor(self,minH,maxH,label):
        self.min_H=minH
        self.max_H=maxH
        self.label=label
