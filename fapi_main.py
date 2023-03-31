from fastapi import FastAPI
import json
import pandas as pd
import base64
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from io import BytesIO
import pandas as pd
import pickle, gzip
import numpy as np
import matplotlib.pyplot as plt

app = FastAPI()

# Returns a Python dictionary
@app.get("/dictionary")
async def get_dictionary():
    return {"message": "Hello, world!"}

# Returns a Pandas DataFrame
@app.get("/dataframe")
async def get_dataframe():
    data = {"Name": ["Alice", "Bob", "Charlie"], "Age": [25, 30, 35]}
    df = pd.DataFrame.from_dict(data, orient='columns')
    print(df)
    return JSONResponse(content=df.to_json(orient="records"))

# Returns a Pandas DataFrame
@app.get("/b64pickle")
async def get_dataframe():
    data = {"Name": ["Alice", "Bob", "Charlie"], "Age": [25, 30, 35]}
    df = pd.DataFrame.from_dict(data, orient='columns')
    imgbuf=get_image_buffer()
	
    raw_dict={'df':df, 'imgbuf':base64.b64encode(imgbuf.read()), 'mydict':{"a":1, 'b':2}}
    #raw_dict={'imgbuf':imgbuf.read(), 'mydict':{"a":1, 'b':2}}
    #raw_dict={'mydict':{"a":1, 'b':2}}
    tmpfile='xyzzzz'
    pickled_dict = pickle.dumps(raw_dict)
    print(pickled_dict)
    b64encoded_str = base64.b64encode(pickled_dict)
    print(raw_dict.keys(), b64encoded_str.decode('utf-8'))
    return JSONResponse(content=b64encoded_str.decode('ascii'))


def get_image_buffer():
    # Create a plot of a sine wave
    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    ax.plot(x, y)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Sine Wave")
    # Save the plot to a BytesIO object
    buffer = BytesIO()
    fig.savefig(buffer, format="jpg")
    # Return the image as a StreamingResponse
    buffer.seek(0)
    return buffer

# Returns a JPEG image
@app.get("/image")
async def get_image():
    buffer=get_image_buffer()
    return StreamingResponse(buffer, media_type="image/jpeg")


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
    json_str = json.dumps(mydict)
    print(json_str)
    return mydict


@app.get("/bigjson")
async def serve_bigjson():
    df=pd.read_csv('a.csv')
    mydict={}
    mydict['cmd']='vq_profile'
    mydict['message_txt']='my text'
    mydict['imgfname_list']=['img.jpg', 'tmp2.jpg']
    mydict['send_df']=df.head()
    print(mydict)
    enhanced_mydict=enhance_common_json(mydict)
    json_dict= json.dumps(mydict)
    print('type of dict:',type(json_dict))

    return JSONResponse(content=json_dict)



@app.post("/post_data")
async def post_data(data: dict):
    print('data received:',data)
    return {"data_received": data}

#dir(app)
