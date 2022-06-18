import streamlit as st
from zipfile import ZipFile
import glob
import json
import datetime
from datetime import datetime
import numpy as np
import pandas as pd
import re
from functools import partial
import os
import sys
import shutil
st.header("This project is to read the json file of facebook messenger")
#this functionn extract zip file which user uploaded

def extractZip(file):
 if file is not None:
  with ZipFile(file, "r") as archive:
    
    st.sidebar.write("Extracting all the file ")
    print("Extracting all file now")
    archive.extractall()
    print("Done")
    st.sidebar.write("Done")


messenger_file = st.sidebar.file_uploader("Choose the messenger json dowmloaded file ")
if st.sidebar.button("extract zip"):
 if messenger_file is not None:
  extractZip(messenger_file) #this extract the zip file and store in file directory
 else:
  st.sidebar.write("Please upload file")



#facebook is decode in like this \\u00c9\\u0089 this cannot be decoded by json,, so this function is to fix this problem:   
fix_mojibake_escapes = partial(
     re.compile(rb'\\u00([\da-f]{2})').sub,
     lambda m: bytes.fromhex(m.group(1).decode()))


dicdata = {
  "date" :[],
  "sender" :[],
  "content" :[]
}

totalMessageCount = {
  "name" :[],
  "count" :[]
}
userName = ""
Mail = ""

datecount = 0
sendercount = 0 
contentcount = 0
startDate = ""
endDate =""
sideShow = []
  
userInfo = "messages/autofill_information.json" # this is the directory of user info stored 

  
try:  #I used this function to encode the user data json file because the user name may be Myanmar language
 with open(userInfo,"rb") as Info:
    repair = fix_mojibake_escapes(Info.read())
    userInfo = json.loads(repair.decode('utf-8'))
 userName = userInfo["autofill_information_v2"]["FULL_NAME"][0]
 Mail = userInfo["autofill_information_v2"]["EMAIL"][0]
except:
  st.sidebar.write("Upload and Extrect the file first")

st.sidebar.write( userName)
st.sidebar.write(Mail)

files = glob.glob("messages/inbox/**/*" , recursive = True) #find all the fileunder inbox

for file in files:
      if '.json' in file:# I only used json file to read and so i add json file directory to sideShow
	      sideShow.append(file)

names = []
fixmessage = []
# i fix all json file and sotredd as dictionary in 
for byonefix in sideShow:
    with open(byonefix,"rb") as chfile:
      repair = fix_mojibake_escapes(chfile.read())
      fixmessage.append(json.loads(repair.decode('utf8')))

for i in range(len(fixmessage)):
    for j in fixmessage[i]["participants"]:
      if j["name"] != userName:
        names.append(j["name"])

chosen_name = st.sidebar.selectbox("Choose name",names)
nameIndex = 0
for i in range(len(names)):
    if names[i] == chosen_name:
      nameIndex = i
for i in range(len(names)):
    totalMessageCount["name"].append(names[i])
    temp = 0
    for me in fixmessage[i]["messages"]:
      if "content" in me:
        temp += 1
      else:
        temp += 1
    totalMessageCount["count"].append(temp)




date = []
sender = []
content = []
i = 0
if nameIndex > 0 :
 for message in fixmessage[nameIndex]["messages"]:
    try:
      i += 1
      
      date.append(datetime.fromtimestamp(message["timestamp_ms"] / 1000).strftime("%Y-%m-%d %H:%M:%S"))
      sender.append(message["sender_name"])
      if "content" in message:
        temp = message["content"]
        
        content.append(temp)
      else:
        content.append("This message is removed")
        
     
      

    except KeyError:
      pass

if len(date)> 0 :
 startDate = date[-1]
 endDate = date[0]
date.reverse()
sender.reverse()
content.reverse()

 
for i in date:
    dicdata["date"].append(i)
    datecount += 1
for i in sender:
    dicdata["sender"].append(i)
    sendercount +=1
for i in content:
    dicdata["content"].append(i)
    contentcount += 1

dcount = pd.DataFrame(totalMessageCount)
df = pd.DataFrame(dicdata)
st.sidebar.write("After Using This Please click remove file to Remove Extracted file in the background")
if st.sidebar.button("Remove file"):
  shutil.rmtree("messages")
st.write("You start conversation with ",chosen_name ,"from",startDate,"to",endDate )
st.dataframe(df)
st.write(dcount)


st.write("Total message " , datecount)
st.write("There need to make showing the graph of how many messages are send in a day and search function")
