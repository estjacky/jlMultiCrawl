from fastapi import FastAPI
import os
import json
import requests
import pandas as pd
import base64
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from io import BytesIO
import pandas as pd

class jsonAPIHelper:

    @staticmethod
    def enhance_common_json(mydict):
        '''
        mydict can have the following keys:message_txt, imgfname_list,  b64_img_list, df_json_str
        '''
        key_list=['message_txt', 'imgfname_list', 'b64_img_dict', 'cmd', 'send_df']
        extra_keys=[k for k in mydict if k not in key_list]
        if 'imgfname_list' in mydict:
            if not 'b64_img_list' in mydict:
                mydict['b64_img_dict']={}
            for imgfname in mydict['imgfname_list']:
                with open(imgfname, 'rb') as f:
                    data=f.read()
                    b64data=base64.b64encode(data).decode('ascii')
                    print('b64data type:',type(b64data))
                    mydict['b64_img_dict'][imgfname]=b64data
        if 'send_df' in mydict:
            df=mydict['send_df']
            mydict['send_df']=json.dumps(df.to_json())
#        json_str = json.dumps(mydict)
#        print(json_str)
        return mydict

    @staticmethod
    def serve_bigjson():
        df=pd.read_csv('a.csv')
        mydict={}
        mydict['cmd']='vq_profile'
        mydict['message_txt']='my text'
        mydict['imgfname_list']=['img.jpg', 'tmp2.jpg']
        mydict['send_df']=df.head()
        print(mydict)
        enhanced_mydict=jsonAPIHelper.enhance_common_json(mydict)
        json_dict= json.dumps(mydict)
        print('type of dict:',type(json_dict))

        return JSONResponse(content=json_dict)
    
    @staticmethod    
    def unmarshall_json(json_dict, save_image=True, tmpdir='tmp'):
        
        if 'JSONResponse' in '%s' % type(json_dict):
            json_dict=json_dict.body
        if not type(json_dict)==type({}):
            json_dict=json.loads(json_dict)
            print("type is ",type(json_dict))
        if not type(json_dict)==type({}):
            json_dict=json.loads(json_dict)
            print("type is ",type(json_dict))

        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)
        ret_dict={}
        if 'send_df' in json_dict:
            y=json.loads(json_dict['send_df'])
        #   print('\n\n\n\ndf:%s' % y, type(y))
            nj=json.loads(y)
            print(type(nj), nj.keys())
            xdf=pd.read_json(y)
            xdf.to_csv(f'{tmpdir}/tmp.csv')
            ret_dict['send_df']=xdf

        olist=("cmd", "message_txt")


        if 'b64_img_dict' in json_dict:
            ret_dict['imgfname_list']=json_dict['imgfname_list']
            ret_dict['b64_img_dict']=json_dict['b64_img_dict']
            i=0
            for k in json_dict['b64_img_dict']:                
                ofname=f'{tmpdir}/{k}'                
                print(ofname)
                if save_image:
                    with open(ofname, 'wb') as f:
                        f.write(base64.b64decode(json_dict['b64_img_dict'][k]))
                        ret_dict['imgfname_list'][i]=ofname
                        ret_dict['b64_img_dict'][k]=""                        
                i=i+1

        for k in olist:
            if k in json_dict:
                ret_dict[k]=json_dict[k]
        return ret_dict

    
def test_pos_json(ret_json):
    # Define the URL of the FastAPI endpoint
    url = "http://localhost:8000/post_data"

    # Define the data to be sent in the request body
    data = {"name": "John", "age": 30}

    # Send the request and store the response
    #response = requests.post(url, json=data)
    ret_json2=fastAPIHelper.enhance_common_json(ret_json)
    response = requests.post(url, json=ret_json2)

    # Print the response from the server
    print(response.json())    
    
    
def test_run():
    _x=jsonAPIHelper.serve_bigjson()
    #_2=json.loads(_x.body)
    #_2=_x
    #save_image=False
    save_image=True
    ret_json=jsonAPIHelper.unmarshall_json(_x, save_image)
    #test_pos_json(ret_json)
    
if __name__=="__main__":
    test_run()
