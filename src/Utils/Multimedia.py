from src.APIs import FacebookAPI
from src.APIs import OpenWeatherMapAPI as WeatherAPI
from src.APIs import SpeechAPI
from src.NLP import NLP
from src.MsgBuilder import WeatherMB
from src.Models import Client

def process_message(user_id, message):  
    # Location message type
    if message['type'] == 'location':
        coordinates = message['data']
        __select_action(user_id, coordinates['lat'], coordinates['long'])

    # Image message type TODO
    elif message['type'] == 'image':
        image_url = message['data']
        FacebookAPI.send_picture(user_id,image_url)

    # Audio message type
    elif message['type'] == 'audio':
        audio_url = message['data']
        response = SpeechAPI.send_audio(audio_url)
        FacebookAPI.send_message(user_id,"I understood: " + response) # TODO remove this (just to see the results)
        NLP.process_message(user_id, response)        

    # Video message type TODO
    elif message['type'] == 'video':
        video_url = message['data']
        FacebookAPI.send_message(user_id, "I've received your video: %s"%(video_url))

    # File message type TODO
    elif message['type'] == 'file':
        file_url = message['data']
        FacebookAPI.send_message(user_id, "I've received your file: %s"%(file_url))

    # Unrecognizable incoming
    else:
        FacebookAPI.send_message(user_id, 'What?')


# select the action related to user context 
def __select_action(user_id, lat, long):
    client = Client.get_client(user_id)
    
    # handling a weather request with the localization 
    if client.context['node'] == 'WeatherRequest':
        response = WeatherAPI.getCurrentWeatherCoordinates(lat, long)
        icon, title, subtitle = WeatherMB.generateCurrentWeatherInfo(response)
        FacebookAPI.send_picture(user_id, icon, title, subtitle)
    
    else:
        FacebookAPI.send_message(user_id, 'I know where you are :)')