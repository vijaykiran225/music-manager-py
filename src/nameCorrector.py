from collections import Counter
import json


# import re
# s = "Example String"
# replaced = re.sub('[ES]', 'a', s)
# print replaced 

albumfilePtr= open("albums_1620583128",'r',encoding='utf8')

reducingChars=[
	":",
	"/",
	"®",
	"[",
	"]",
	"www.123musiq.com",
	"MassTamilan",
	"\"",
	".com",
	".in",
	".io",
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

albums=list()
for x in albumfilePtr:
	unicode_text=x[:-1]
	# unicode_text=unicode_text.encode("utf8")

	for charToRemove in reducingChars:
		unicode_text=unicode_text.replace(charToRemove,"")
		if len(unicode_text) == 0 or unicode_text[0]==" ":
			unicode_text="Exception"
		unicode_text=unicode_text.strip()

	albums.append(unicode_text)
albumfilePtr.close()

print(len(albums))
ans = Counter(albums)

albumfilePtr= open("alb.json",'w',encoding='utf8')
unicode_text=json.dumps(ans,indent=4,ensure_ascii=False)
# unicode_text=unicode_text.encode("utf8")
albumfilePtr.write(unicode_text)
albumfilePtr.close()

