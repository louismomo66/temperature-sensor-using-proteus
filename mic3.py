import pyaudio
import audioop
import dropbox
import math
import os

import wave
from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import schedule
from datetime import datetime
chunk = 1024 * 2 
format1 = pyaudio.paInt16
channels1 = 1
rate1 = 44100
record_secs = 10
#dev_index = 1
wav_output_filename = 'wave2.wav'

Broker = "192.168.43.141"
sub_topic = "mic/spldb"
topic = "mic/recording"

p = pyaudio.PyAudio()

def record():
    stream= p.open(format=format1,
                channels= channels1,
                rate = rate1,
                input = True,
                frames_per_buffer=chunk)
    print("Startin....")
    frames = []
    for i in range(0,int(rate1/chunk*record_secs)):
        data = stream.read(chunk,exception_on_overflow=False)
        #print('Appending')
        frames.append(data)
    print('Stop..')    
    #stream.stop_stream()
    #stream.close()
    #p.terminate()
    wavefile=wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(channels1)
    wavefile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wavefile.setframerate(rate1)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    f = open("wave2.wav","rb")
    audio = f.read()
    f.close()
    byteArray=bytearray(audio)
    mqttc = mqtt.Client("node-red")
    mqttc.connect(Broker,1883,60)
    mqttc.publish(sub_topic,byteArray)
    dbx = dropbox.Dropbox('sl.BO7zMD2orIPT5CkU7cuksFjiPzRLfaSLotHR3-9pzs6gng-XTy_89oZQq0fwQDvewj8ZbLJ0STxJivFybsNPeiAPOe215u89k70jyTnRu9W-b3fKrpBNJPC-ZYTlNAVQIK5ETog') #enter your dropbox app API key between the quotation marks
    dbx.users_get_current_account()

    for root, dirs, files in os.walk("/home/pi"): #Searching in this folder
        for file in files:
            if file.endswith(".wav"): #looks for all files that end in .mp3
                f = open(os.path.join(root,file),'rb')
                dbx.files_upload(bytes(f.read()),'/Audio/recordin3.wav') 
    
    
    
    

schedule.every(0.5).minutes.do(record)

def stream():
    stream= p.open(format=format1,
                channels= channels1,
                rate = rate1,
                input = True,
                frames_per_buffer=chunk)
    print("Startin....")
    frames = []
    #for i in range(0,int(rate1/chunk)):
    while True:
        data = stream.read(chunk,exception_on_overflow=False)
        #print('Appending')
        frames.append(data)
        rms = audioop.rms(data,2)
        db = 20*math.log10(rms/20)
        db = round(db,2)
        SPLdb = -46+db+94-40
        SPLdb = round(SPLdb,2)
        #print(rms)
        #print(SPLdb)
        schedule.run_pending()
        mqttc = mqtt.Client("node-red")
        mqttc.connect(Broker,1883,60)
        mqttc.publish(sub_topic,SPLdb)








stream()
