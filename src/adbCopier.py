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
#        print(r)
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
    move = True
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

    # json.load("/Users/vj/Music/mem_1661362457.json")
    files = walk_music(src+"/Vijay_Music_Library")

    file_name = f'{src}/android_{int(time.time())}.sh'

    f_ptr=open(file_name,'w')

    mem = {}

    for a_file in files:

        a,b,c=getPath(a_file,src+"/Vijay_Music_Library/")
        if c not in mem:
            mem[c] = []
        mem[c].append(a)

        content = f'./adb shell mkdir \"/storage/sdcard0/Music/{c}\"'
        f_ptr.write(content)
        f_ptr.write("\n")
        content = f'./adb push \"{a}\" \"/storage/sdcard0/Music/{c}\"'
        f_ptr.write(content)
        f_ptr.write("\n")

    f_ptr.close()

    file_name = f'{src}/mem_{int(time.time())}.json'
    f_ptr=open(file_name,'w')
    f_ptr.write(json.dumps(mem))
    f_ptr.close()

    return file_name


def generate_play_listV2(src):

    
    # files = walk_music(src+"/Vijay_Music_Library")

    file_name = f'{src}/android_{int(time.time())}.sh'

    f_ptr=open(file_name,'w')

    mem =  json.load(open("/Users/vj/Music/mem_1661363078.json"))

    for album in mem:

        songsInpath = mem[album]
        
        content = f'./adb shell mkdir \"/storage/sdcard0/Music/{album}\"'
        f_ptr.write(content)
        f_ptr.write("\n")
        for song in songsInpath:
            content = f'./adb push \"{song}\" \"/storage/sdcard0/Music/{album}\"'
            f_ptr.write(content)
            f_ptr.write("\n")

    f_ptr.close()

    return file_name

def generate_play_listV3(src):

    
    # files = walk_music(src+"/Vijay_Music_Library")

    file_name = f'{src}/android_{int(time.time())}.sh'

    f_ptr=open(file_name,'w')

    counter = 0 
    i=-1
    album=""
    r_ptr= open("/Users/vj/Music/process.m3u",'r').read().splitlines()

    for mem in r_ptr:
        
        if(counter % 75 ==0):
            i=i+1
            album = f'folder_{i}';
            content = f'./adb shell mkdir \"/storage/sdcard0/Music/{album}\"'
            f_ptr.write(content)
            f_ptr.write("\n")
            
      
        content = f'./adb push \"{mem}\" \"/storage/sdcard0/Music/{album}\"'
        f_ptr.write(content)
        f_ptr.write("\n")
        counter = counter+1

    f_ptr.close()

    return file_name


def splitFile(src,breakingPoint):

    file_names = []

    fptr= open(src,'r').read().splitlines()

    fname='part_0.sh'
    wptr = open(fname,'w')
    file_names.append(fname)
    i=0
    for line in fptr:
        if i!=0 and i%breakingPoint == 0:
            fname = f'part_{i}.sh'  
            wptr.close()
            wptr = open(fname,'w')
            file_names.append(fname)

        wptr.write(line)
        wptr.write("\n")
        i = i+1



    return file_names



def main():

    # (persist ,move ,debug,stopCount,playListSrcPath,destinationPath)=process_args(sys.argv[1:])

    # fileData=walk_music(playListSrcPath)
    # processedOutput=process(fileData,debug,stopCount,destinationPath)

    # if move:
    #     moveFiles(processedOutput["passed"])
    #     moveFiles(processedOutput["failed"])
    # if persist:
    #     persistFile("passed",processedOutput["passed"])
    #     persistFile("failed",processedOutput["failed"])

    opPath=splitFile("/Users/vj/Music/android_1661365483.sh",100)

    print("new playlist generated at ",opPath)

main()
print("done")
