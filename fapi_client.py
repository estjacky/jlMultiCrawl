import requests
import json
import gzip,pickle
import os,sys
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Call the dictionary endpoint
response = requests.get("http://localhost:8000/dictionary")
data = response.json()
print(data)

response = requests.get("http://localhost:8000/b64pickle")
data = response
print('b64:',data.content)
import base64
barray=base64.b64decode(data.content)
new_dict=pickle.loads(barray)
print(new_dict)
new_file='tmp2.jpg'
with open(new_file, 'wb') as f:
	f.write(base64.b64decode(new_dict['imgbuf']))


# Call the image endpoint
response = requests.get("http://localhost:8000/image")
#image = Image.open(BytesIO(response.content))
#with open('a.jpg', 'wb') as f
#	image.show()
with open('img.jpg', 'wb') as f:
	f.write(response.content)

response = requests.get("http://localhost:8000/bigjson")
print('xxxxxxxxx##############:',response.json())
#x=json.loads(response.json())
json_dict=json.loads(response.json())

def unmarshall_json(json_dict):
    tmpdir='tmp'
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)
    ret_dict={}
    if 'send_df' in json_dict:
        y=json.loads(json_dict['send_df'])
	#	print('\n\n\n\ndf:%s' % y, type(y))
        nj=json.loads(y)
        print(type(nj), nj.keys())
        xdf=pd.read_json(y)
        xdf.to_csv(f'{tmpdir}/tmp.csv')
        ret_dict['send_df']=xdf

    olist=("cmd", "message_txt")
#olist=[]
    if 'b64_img_dict' in json_dict:
        for k in json_dict['b64_img_dict']:
            print(k)
            ofname=f'{tmpdir}/{k}'
            with open(ofname, 'wb') as f:
                f.write(base64.b64decode(json_dict['b64_img_dict'][k]))
                ret_dict['image_fname']=ofname

    for k in olist:
        if k in json_dict:
            ret_dict[k]=json_dict[k]
    return ret_dict


ret_dict=unmarshall_json(json_dict)
print(ret_dict)
exit()
print(type(response.json()))
print(type(x))
print(x.keys())
y1=(x['send_df'])
y=json.loads((x['send_df']))
print(y1, type(y1), type(y))
#print(y)
print(type(y))



exit()
# Call the dataframe endpoint
response = requests.get("http://localhost:8000/dataframe")
print('##############:',response.json())
x=response.json()
print('x is type ',type(x[0]))
json_obj=json.loads(x)
print(json_obj, type(json_obj[0]))
#data = pd.read_json(json_obj, orient="columns")
#data = pd.DataFrame.from_dict(dict(response.json()[0]), orient="columns")
#data = pd.DataFrame.from_dict(json_obj[0], orient="columns")

#data = pd.DataFrame.from_dict(json_obj[0], index=[1,2,3])
#data = pd.DataFrame(json_obj, index=[1,2,3])
data = pd.DataFrame(json_obj)
#data = pd.DataFrame.from_dict(json_obj[0], orient="columns", index=json_obj[0].keys())
print(type(data))


