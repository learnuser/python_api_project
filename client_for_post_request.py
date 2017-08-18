import requests
import os

url = 'http://127.0.0.1:5000/upload'
api_url = 'https://herculesapi.herokuapp.com/upload'
api_url1='http://learnuser.pythonanywhere.com/upload'
# Pass single file to POST request.
#files = {'files':open("C:/Users/umurasa/Documents/2017/Q3 Release/dummy/MTCF_ID_8475.pdf",'rb')}

# Pass multiple files to POST request.
path = "C:/Users/umurasa/Documents/2017/Q3 Release/dummy/"

file_list=[]
for root, dirs, files in os.walk(path):
    for fileName in files:
        if len(files)>0:
            relDir = os.path.relpath(root, path)
            relFile = os.path.join(relDir, fileName)
            file_list.append(('srcfile',(fileName,open(path+relFile, 'rb'))))

data = {'collection_name':'CVLT3_QG','prefix':'MTCF_cvlt3_retest_','mongodb_id':'ID'}

#r = requests.post(url, data=data, files=files)
#print file_list[0], type(file_list[0])

r = requests.post(api_url1, data=data, files=file_list)
print r.text



