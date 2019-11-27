import os
import time
from io import BytesIO

import requests        #导入requests包
from PIL import Image
from bs4 import BeautifulSoup
import warnings
import datetime
warnings.filterwarnings('ignore')
#van gogh cezanne ukiyo-e
imgurl=[]
filenames=[]
dirstr="./vangoghL/"
def save_img():  ##保存图片
    l=len(imgurl)
    requests.adapters.DEFAULT_RETRIES = 5
    #User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
    tempimage=[]
    tempimagesize = []
    batchsize=160
    failedimagename = []
    if not os.path.exists(dirstr):
        os.mkdir(dirstr)
    for i in range(0,int(l/batchsize)):
        if i+1%103==0:
            print(datetime.datetime.now())
        print("-------%d------" % i)
        filename=filenames[i]
        filepath=dirstr+filename
        if os.path.exists(filepath):
            continue
        tempimage = []
        tempimagesize=[]

        for j in range(0,batchsize):
           # time.sleep(0.1)
            #print("***%d***" % j)
            url=imgurl[i*batchsize+j]
            img = requests.get(url, verify=False, headers=headers)
            #print(url)
            #print("code ",img.status_code)
            if img.status_code!=200:#没获取到
                continue
            if len(img.content) < 3072: #长度太小
                continue
            try:
                tmpIm = BytesIO(img.content)
                im = Image.open(tmpIm)
                w,h=im.size
                if not (w > 20 and h > 20):#尺寸不对
                    continue
                #print('开始保存图片')
                #print("filename ", filename, len(img.content))
                f = open(filepath, 'ab')
                f.write(img.content)
                #print(filepath, '图片保存成功！')
                f.close()
                break
            except OSError:
                pass
            continue
        #
        
    print(failedimagename)




def geturl():
    url = 'https://www.wikiart.org/en/vincent-van-gogh/all-works/text-list'
    #url = 'https://www.wikiart.org/en/claude-monet/all-works/text-list'
    strhtml = requests.get(url)        #Get方式获取网页数据
    #print(strhtml.text)
    soup=BeautifulSoup(strhtml.text,'lxml')
    lis=soup.find_all("li",class_="painting-list-text-row")
    suffixlists=["!PinterestSmall.jpg","!Portrait.jpg","!PinterestLarge.jpg","!Blog.jpg","!Large.jpg","!HalfHD.jpg","!HD.jpg"]
    for li in lis:
        #print(li)
        a_bf = BeautifulSoup(str(li))
        a = a_bf.find_all('a')
        for each in a:
            #print("------")
            #print(each.get('href'))
            substr=each.get('href')
            substrs=substr.split("/")
            filenames.append(substrs[-1] + ".jpg")
            for i in range(0,10):
                strurl="https://uploads"+str(i)+".wikiart.org/images/"+substrs[-2]+"/"+substrs[-1]+".jpg"


                for j in range(0,len(suffixlists)):
                    temp=strurl+suffixlists[j]
                    imgurl.append(temp)
                    #print(temp)
                imgurl.append(strurl)
                #print(strurl)

                strurl = "https://uploads" + str(i) + ".wikiart.org/images/" + substrs[-2] + "/" + substrs[-1] + "(1).jpg"


                for j in range(0,len(suffixlists)):
                    temp=strurl+suffixlists[j]
                    imgurl.append(temp)
                    #print(temp)
                imgurl.append(strurl)
                #print(strurl)
geturl()
save_img()
