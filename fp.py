from PIL import Image
import numpy as np
import pytesseract
import re
import matplotlib.pyplot as plt
import time
import math
def img_to_array(filename):
    image = Image.open(filename)
    image = image.convert('L')
    array = np.array(image)
    n = len(array)
    m = len(array[0])
    for i in range(n):
        for j in range(m):
            if array[i][j]<200:
                array[i][j] = 0
            else:
                array[i][j] = 255
    return array
def array_to_img(array):
       return Image.fromarray((array))
def word_analysis(array,raw_up,raw_down):
    result = ['0' for i in range(len(array[0]))]
    for j in range(len(array[0])):
        n = 0
        for k in range(raw_up,raw_down):
            if array[k][j]==0:
                n=1
                break
        if n==0:
            result[j]='1'
    list_target = []
    list_distance = []
    s = ''.join(result)
    target = re.finditer('01+0',s)
    start = list(re.finditer('10+1',s))
    for each in target:
        list_target.append((each.start(),each.end()))
        list_distance.append(each.end()-each.start())
    maxn= max(list_distance)
    minn= min(list_distance)
    list_slice = [start[0].start()]
    for i in range(len(list_distance)):
        if (maxn-list_distance[i])<=(list_distance[i]-minn):
            list_slice.append(int((list_target[i][1]+list_target[i][0])/2))
    list_slice.append(start[-1].end())
    return list_slice
def raw_analysis(array):
    l = []
    for sublist in array:
        n = 0
        for each in sublist:
            if each==0:
                n+=1
        l.append(n)
    state = [1 for i in range(len(l))]
    k = 10
    m = max(l)
    l = [m-l[i] for i in range(len(l))]
    for i in range(k):
        change = [0 for i in range(len(l))]
        for j in range(len(l)-1):
            change[j] += (l[j+1]-l[j])/m
            change[j+1] += (l[j]-l[j+1])/m
        state = [state[i]+change[i] for i in range(len(state))]
    state = [round(state[i],2) for i in range(len(state))]
    z = zip(l,state)
    for each in z:
        print(each)
       
def pointing_word(filename,*args):
    imarray = img_to_array(filename)
    raw = args[0]
    column = args[1]
    raw_up = raw
    raw_down = raw+1
    while True:
        n = 0
        for each in imarray[raw_up]:
            if each==0:
                n+=1
        if n<=3:
            break
        else:
            raw_up-=1   
    while True:
        n = 0
        for each in imarray[raw_down]:
            if each==0:
                n+=1
        if n<=3:
            break
        else:
            raw_down+=1
    list_ref = word_analysis(imarray,raw_up,raw_down)
    column_left = args[1]
    column_right = args[1]+1
    for i in range(len(list_ref)-1):
        if list_ref[i]<=args[1]<=list_ref[i+1]:
            column_right = list_ref[i+1]
            column_left = list_ref[i]
            break
    img2 = array_to_img(imarray)
    img3 = img2.crop((column_left,raw_up,column_right,raw_down))
    return img3
class onclick:
    def __init__(self,fig,filename):
        self.x = 0
        self.y = 0
        self.cid = fig.canvas.mpl_connect('button_press_event',self)
        self.filename = filename
    def __call__(self,event):
        self.x = event.x
        self.y = event.y
        im = pointing_word(self.filename,event.y,event.x)
        print(self.y,self.x,event.y,event.x)
        text = pytesseract.image_to_string(im, lang='eng')
        print(text)
def search_word(filename):
    img = Image.open(filename)
    fig = plt.figure('Image')
    plt.imshow(img)
    plt.title(filename)
    click = onclick(fig,filename)
    plt.show()
    
#search_word('img1.jpg')
#raw_analysis(img_to_array('img1.jpg'))
t1 = time.perf_counter()
im = pointing_word('img1.jpg',500,361)
t2 = time.perf_counter()
print(t2-t1)
im.show()
text = pytesseract.image_to_string(im, lang='eng')
print(text)
