import youtube_dl
import requests
import time
from bs4 import BeautifulSoup
import sys
import getopt



def search_yt(fileName):
	url = 'https://www.youtube.com/results?search_query=' + fileName
	time.sleep(2)
	html = requests.get(url)
	soup = BeautifulSoup(html.content, "html.parser")

	text_url = ""
	text_link = []
	
	for a in soup.find_all('a', href=True, text=True):
		text_url = a['href']

		if text_url.find('/watch?v=') == 0 :
			#print (text_url)
			text_link.append(text_url)
			#print (link_text)
	#url_list.append(text_link[0])
	#print ("ssssss : ", text_link[0])
	return text_link[0]

def find_ytUrl(file_ext='mp4', name=None, 
	search_list=None):
	'''
		file_ext : file extension
		name : search name
		search_list : search name list
	'''
	url_list = []
	#TODO file ext
	#if file_ext == '':
	
	if name != None :
		url_list.append(search_yt(name))
	
	elif search_list != None :
		f = open(search_list,'r')
		
		while True:  
			fileName = f.readline()	
			if fileName == '':
				break
			url_list.append(search_yt(fileName))
		f.close()
	yt_download(url_list)
	
#download yotube file
def yt_download(urlList):
	
	count = 0
	for url in urlList :
		url = 'https://www.youtube.com' +  url
		#with youtube_dl.YoutubeDL({'format':'137'}) as ydl:
		with youtube_dl.YoutubeDL({'format':'137'}) as ydl:
			ydl.download([url])
			count +=1
	
	print (str(count) +' file download')

# help alert
def help():
	print ("print help usage")
	print ("[-e] is file extension")
	print ("[-f] is file name")
	print ("[-i][--input] is url list")
	print ("[-h][--help] is help option")
	return 
 
def noOption():
	print ('print help usage')
	print ('[-h][--help] command input')

# start menue
def main():
	try:
	# 여기서 입력을 인자를 받는 파라미터는 단일문자일 경우 ':' 긴문자일경우 '='을끝에 붙여주면됨
		opts, args = getopt.getopt(sys.argv[1:],"f:e:i:",["input=","help"])
	
	except getopt.GetoptError as err:
		print (str(err))
		help()
		sys.exit(1)

	file_ext = None
	name = None
	search_list = None
	
	if opts == [] :
		noOption()
		sys.exit(1)

	for opt,arg in opts:
		#print ("arg is : " +str(arg))

		if (opt == '-e'):
			file_ext = arg
		elif (opt == '-f'):
			name = arg
		elif (opt == '-i' or opt =='--input'):
			search_list = arg
		elif ( opt == "-h") or ( opt == "--help"):
			help()
			sys.exit(1)
 	
	find_ytUrl(file_ext, name, search_list)
	
if __name__ == '__main__':
	main()
