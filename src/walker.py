import os
import json
import time

# # "/Users/vj/Music/Copy"
# print(os.getcwd())

def walk_music(mediaLocation):
    
    data = set()
    for r,d,f_list in os.walk(mediaLocation):
        # f_count = f_count+ len(f_list)
        for aFile in f_list:
            _,ext = os.path.splitext(aFile)

            if ext == "" or ext == ".xspf" or ext == ".m3u" or ext == ".m3u-e":
                continue
            
            data.add(r + "/"+ aFile)

    print(len(data))

    return data

def fix_braces(a_file):
    ans = a_file.replace("[","%5B")
    ans = ans.replace("]","%5D")
    return ans



def generate_play_list():

    files = walk_music("/Users/vj/Music")

    file_name = f'pls/startup_{int(time.time())}.m3u'

    f_ptr=open(file_name,'w')

    for a_file in files:

        f_ptr.write(fix_braces(a_file))
        f_ptr.write("\n")

    f_ptr.close()


    return file_name


# walk_music("/Users/vj/Music/Copy")
print( generate_play_list() )



print("done")