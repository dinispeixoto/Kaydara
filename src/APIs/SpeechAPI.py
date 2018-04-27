from pydub import AudioSegment

import os, json, requests, urllib

# Environment variables on heroku
USERNAME = os.environ['SPEECH_USERNAME']
PASSWORD = os.environ['SPEECH_PASSWORD']

# send audio file and return the transcript 
def send_audio(audio_url):
    headers = {'Content-Type': 'audio/flac',}  
    params = {'model': 'en-US_NarrowbandModel',}  

    audio_file = __download(audio_url)
    __convert(audio_file)
    data = open(audio_file + '.flac', 'rb').read()

    response = requests.post('https://stream.watsonplatform.net/speech-to-text/api/v1/recognize', 
                headers=headers, data=data, params=params, auth=(USERNAME, PASSWORD))
    
    response_decoded = response.content.decode("utf-8")
    dict_response = json.loads(response_decoded)
    print(dict_response)

    os.remove(audio_file)
    os.remove(audio_file + '.flac')

    if dict_response['results']:
        return dict_response['results'][0]['alternatives'][0]['transcript']
    else:
        return 'Nothing'

def __download(audio_url):
    webFile = urllib.request.urlopen(audio_url)                                                     
    fileName = audio_url.split('/')[-1]
    localFile = open(fileName, 'wb')
    localFile.write(webFile.read())
    
    webFile.close()
    localFile.close()
    return fileName

def __convert(audio):
    AudioSegment.from_file(audio).export(audio + '.flac', format='flac')