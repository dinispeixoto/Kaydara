import os, json, requests

# Environment variables on heroku
USERNAME = os.environ['SPEECH_USERNAME']
PASSWORD = os.environ['SPEECH_PASSWORD']

# send audio file and return the transcript 
def send_audio(audio):
    headers = { 'Content-Type': 'audio/flac',}                                                              # audio type
    data = open(audio + 'audio-file.flac', 'rb').read()                                                     # data is binary 
    response = requests.post('https://stream.watsonplatform.net/speech-to-text/api/v1/recognize', 
                headers=headers, data=data, auth=(USERNAME, PASSWORD))
    
    response_decoded = response.content.decode("utf-8")
    dict_response = json.loads(response_decoded)

    return dict_response['results'][0]['alternatives'][0]['transcript']

"""
if __name__ == '__main__':
    transcript = send_audio('resources/')
    print(transcript)
"""