import shutil
import audio_metadata
from os import path
import json
import time
import sys
import os
import getopt



# ajdkfdk


def walk_music(mediaLocation):
    f_count=0
    data = set()
    for r,d,f_list in os.walk(mediaLocation):
        print(r)
        # f_count = f_count+ len(f_list)
        for aFile in f_list:
            _,ext = os.path.splitext(aFile)

            if ext == "":
                continue
            f_count = f_count +1
            data.add(r + "/"+ aFile)

    print(f_count)

    return data


def correctName(unicode_text):
    reducingChars=[
        ":",
        "/",
        "®",
        "[",
        "]",
        "www.123musiq.com",
        "MassTamilan.io",
        "\"",
        ".com",
        ".in",
        "MassTamilan",
        "www.isaitamil",
        "www.mobitamilan.net",
        "Riya collections",
        "www.FreshlyServedHipHop",
        "www.TamilMp3Data Full Mp3 Songs",
        "www.primemusic.ru",
        "www.MobiTamilan.Net",
        "www.alphalink.au~mohans",
        "www.tamilboss",
        "www.SongsLover",
        "www.TamilWire",
        "www.BigMusic.In",
        "www.sensongs",
        "www.SouthMp3.Org)",
        "www.MobiTamilan.Net Mobile World",
        "www.TKada.Com",
        "www.Tamilanda.cc",
        "www.tamilwap",
        "www.tamilmp3data",
        "www.iHipHopMusic",
        "Masstamilan.In",
        "-",
        "©",
        "o5wap.ru"
    ]

    # unicode_text=x[:-1]
    # unicode_text=unicode_text.encode("utf8")

    for charToRemove in reducingChars:
        unicode_text=unicode_text.replace(charToRemove,"")

    unicode_text=unicode_text.strip()

    if len(unicode_text) == 0:
        unicode_text="Exception"

    if(unicode_text=="\u0000;\u0001ÿ\u0000þA\u0000s\u0000s\u0000a\u0000s\u0000s\u0000i\u0000n\u0000'\u0000s\u0000 \u0000C\u0000r\u0000e\u0000e\u0000d\u0000 \u0000B\u0000r\u0000o\u0000t\u0000h\u0000e\u0000r\u0000h\u0000o\u0000o\u0000d"):
        unicode_text="Exception"
        print("nullbytes fixed")
    return unicode_text

def getPath(fileName,destinationPath):

    #fileName ="./Kalakapovathu Yaaru.mp3"
    src = path.realpath(fileName)
    head,tail=path.split(src)
    # destinationPath = "/Users/vijaykiran225/Vijay_Music_Library/"
    try:
        metadata = audio_metadata.load(fileName)
        albumName=metadata.tags.album[0]
        fixedName=correctName(albumName)
        if(len(fixedName) ==0):
            print("something up")
        destinationPath = destinationPath + fixedName
        destinationPath = destinationPath +"/"+ tail
        #print(destinationPath)
        return (destinationPath,True,fixedName)

    except Exception as e:
        print(e)
        destinationPath = destinationPath + "Exception"
        destinationPath = destinationPath +"/"+ tail
        return (destinationPath,False,"Exception")

def readPlayListData(playListPath):
    filePtr = 0;
    filePtr =  open(playListPath,'r')

    plData=filePtr.read().split('\n')
    filePtr.close()
    return plData

def persistList(name,content):
    if(len(content)==0):
        print(f"nothing to write for {name}")
        return

    logFileName=f"logs/{name}_{int(time.time())}"
    passedFile=open(logFileName,'w')
    count =0
    for aVal in content:
        passedFile.write(aVal)
        passedFile.write("\n")
        count=count+1
    passedFile.close()
    print(f"wrote {count} records for {logFileName}")

def process(playListData,debug,stopCount,destinationPath):
    opPathList=list()
    failuresList=list()
    count=0
    logAlbums=list()
    for aFile in playListData:
        opPath, statusCode,albumName =getPath(aFile,destinationPath)
        logAlbums.append(albumName)
        if opPath==aFile:
            print("already in right place")
            continue

        data=dict()
        data["origPath"] = aFile
        data["newPath"] = opPath
        if(statusCode == True):
            opPathList.append(data)
        else:
            failuresList.append(data)
        
        count= count+1
        if(debug==True and count == stopCount):
            break 
    
    processedData=dict()
    processedData["passed"]=opPathList
    processedData["failed"]=failuresList
    print(f"processed {count} records")

    persistList("albums",logAlbums)

    return processedData 

def persistFile(name,content):

    if(len(content)==0):
        print(f"nothing to write for {name}")
        return

    logFileName=f"logs/{name}_{int(time.time())}"
    passedFile=open(logFileName,'w')
    count =0
    for aVal in content:
        strData=f"mv {aVal['origPath']} {aVal['newPath']}\n"
        passedFile.write(strData)
        count=count+1
    passedFile.close()
    print(f"wrote {count} records for {logFileName}")

def moveFiles(contentList):
    count=0
    errs=list()


    for content in contentList:
        
        src = path.realpath(content['origPath'])
        head,tail=path.split(src)
        if not os.path.exists(head):
            print(f"file missing in origPath {content['origPath']}")
            errs.append(content['origPath'])
            continue

        print(f"oldPath<{content['origPath']}>")
        print(f"newPath<{content['newPath']}>")
        # errs.append(content['newPath'])
        # continue

        src = path.realpath(content['newPath'])
        head,tail=path.split(src)
        if not os.path.exists(head):
            os.makedirs(head)

        try:
            shutil.move(content['origPath'],content['newPath'])
        except Exception as e:
            print(e,"some Exception while coying")
            errs.append(content['origPath'])

        count=count+1
    print(f"moved {count} records ")
    print(f"erred {len(errs)} records")

def process_args(argv):
    persist = False
    move = False
    debug=False
    stopCount=10
    playListSrcPath="/Users/vj/Music/Copy"
    destinationPath = "/Users/vj/Music/Vijay_Music_Library/"

    try:
        opts, args = getopt.getopt(argv,"hd:c:p:m:s:o:",["debug=","stopcount=","persist=","move=","src=","output="])
    except getopt.GetoptError:
        print( 'autoOrganize.py -d <shouldDebug> -p <shouldPersistLogs> -c <count> -m <shouldMove> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print( 'autoOrganize.py -d <shouldDebug> -p <shouldPersistLogs> -c <count> -m <shouldMove> ')
            sys.exit()
        elif opt in ("-d", "--debug"):
            debug = bool(arg)
        elif opt in ("-c", "--stopcount"):
            stopCount = int(arg)
        elif opt in ("-p", "--persist"):
            persist = bool(arg)
        elif opt in ("-m", "--move"):
            move = bool(arg)
        elif opt in ("-s", "--src"):
            playListSrcPath = str(arg)
        elif opt in ("-o", "--output"):
            destinationPath = str(arg)
    print(persist ,move ,debug,stopCount)
    return (persist ,move ,debug,stopCount,playListSrcPath,destinationPath)


def fix_braces(a_file):
    ans = a_file.replace("[","%5B")
    ans = ans.replace("]","%5D")
    return ans


def generate_play_list(src):

    files = walk_music(src)

    file_name = f'pls/startup_{int(time.time())}.m3u'

    f_ptr=open(file_name,'w')

    for a_file in files:

        f_ptr.write(fix_braces(a_file))
        f_ptr.write("\n")

    f_ptr.close()


    return file_name



def main():

    (persist ,move ,debug,stopCount,playListSrcPath,destinationPath)=process_args(sys.argv[1:])

    fileData=walk_music(playListSrcPath)
    processedOutput=process(fileData,debug,stopCount,destinationPath)

    if move:
        moveFiles(processedOutput["passed"])
        moveFiles(processedOutput["failed"])
    if persist:
        persistFile("passed",processedOutput["passed"])
        persistFile("failed",processedOutput["failed"])

    opPath=generate_play_list("/Users/vj/Music")

    print("new playlist generated at ",opPath)

main()
print("done")
