import sys
from nltk.corpus import wordnet as wn
import requests
import json

similarityCap = .25
prevWords = {}
EMOTIONS = ["adore", "funny", "anger", "anxiety", "awe", "awkward", "boring", "calm", "confusion", "disgust", "hate", "excitement", "fear", "curious", "joy", "nostalgia", "love", "sad", "satisfaction"]
common_nonconnotation = {"the", "as", "a", "an", "in", "of", "but", "and", "is"}

def find_difference(word, emotion):
    try:
        wor = wn.synsets(word)[0]
    except:
        return -9999
    allscore = []
    for meanin in wn.synsets(emotion):
        allscore.append(wor.path_similarity(meanin))
    allscore.sort(reverse=True)
    return allscore[0]

def get_word_emotion(word):
    if word in prevWords.keys():
        if prevWords[word] is None:
            return None
        return prevWords[word]
    if word not in common_nonconnotation:
        similarities = []
        for emotion in EMOTIONS:
            distance = find_difference(word, emotion)
            similarities.append((distance, emotion))
        similarities.sort(reverse=True)
        if similarities[0][0] > similarityCap:
            prevWords[word] = similarities[0][1]
            return similarities[0][1]
        prevWords[word] = None
    return None

def create_emotion_list(frequency_dict, total_emotions):
    list_of_percents = []
    for emotion in frequency_dict.keys():
        list_of_percents.append( ( frequency_dict[emotion] / total_emotions, emotion ) )
    list_of_percents.sort(reverse=True)
    final_list = []
    if list_of_percents[0][0] > 0.75:
        final_list.append((list_of_percents[0][1], list_of_percents[0][0]))
        return final_list
    min_range = list_of_percents[0][0] / 2
    for iteration in list_of_percents:
        if iteration[0] > min_range:
            final_list.append((iteration[1], iteration[0]))
    return final_list

def remove_punct(string):
    punct = ".,:;!?<>[]()\/+-='"
    new = ""
    for thing in string:
        if thing not in punct:
            new += thing
    return new

def read_txt(input):
    """with open("data.txt") as f:
        input_list = [input.strip() for input in f]
    input = "".join(input_list)"""
    input = remove_punct(input)
    input_list = input.split()
    frequencies = {}
    total_appearances = 0
    for word in input_list:
        word_emotion = get_word_emotion(word)
        if word_emotion is not None:
            total_appearances += 1
            if word_emotion not in frequencies.keys():
                frequencies[word_emotion] = 1
            else:
                frequencies[word_emotion] = frequencies[word_emotion]+1
    if len(frequencies.keys()) == 0:
        return []
    return create_emotion_list(frequencies, total_appearances)

endpoint_url = "https://api.spotify.com/v1/recommendations?"
token = "BQBYjH8GrNFlMv6kBVFPtRFH3zi_fuVe9jn7_loidRxgYi3D31iT-Wt2LnrNvX9tKSeG2DaQQa_CoTgsYdTmtlZ55ojv9S2qVOMp_XKXeie2NJ6qQ4-m5dsZ6jc28MoLPmgHpTT4JsNujdK7U19rxp4nfaH6HEnKdGMRoFK1-gB7nSCsRTDgBCDmlRG0smEDS6TJsaDZJgdnFw"
user_id = "31thsycepxrqhomn75aterzyttmq"

emotion_responses = []
seed_tracks={"adore":'7tyckyaQOzlsTjnujLinRt', "funny":'6YQ7aPJhk0MGpwoKfFAEbS', "anger":'56sk7jBpZV0CD31G9hEU3b', "anxiety":'0G21yYKMZoHa30cYVi1iA8', "awe":'0UOg3se2cLYlz9HmQZsSjE', "awkward":'15TQGEl1D0C5ztvvvnFCw7', "boring":'6yXPg2VYvluTxbd4No5vPQ', "calm":'3Uh7rAb7F0XGVpEEDwfH1k', "confusion":'0YPuRrM2NwzdtuShUKkts6', "disgust":'0ZUo4YjG4saFnEJhdWp9Bt', "hate":'0y0v0SDevDcGW5rsDElup3', "excitement":'2McQQA5nCLVL0XvzcxWhFC', "fear":'1g10rYqM3jJQsWRnXCFcx7', "curious":'0nF5aQoLs2YtbWwClXvumL', "joy":'4y5bvROuBDPr5fuwXbIBZR', "nostalgia" :'3zBhihYUHBmGd2bcQIobrF', "love":'0tgVpDi06FyKpA1z0VMD4v', "sad":'1ONoPkp5XIuw3tZ1GzrNKZ', "satisfaction":'60IGhnH20N82dNxKnc8jDd'}
uris = []

list_of_emotions = read_txt(sys.argv[1])

for emotion in list_of_emotions:
    # OUR FILTERS

    limit=int(emotion[1]*10)
    market="US"
    
    # PERFORM THE QUERY
    query = f'{endpoint_url}limit={limit}&market={market}'
    query += f'&seed_tracks={seed_tracks[emotion[0]]}'

    response = requests.get(query, 
                headers={"Content-Type":"application/json", 
                            "Authorization":f"Bearer {token}"})
    emotion_responses.append(response.json())

print('Recommended Songs:')
for json_response in emotion_responses:
    for i,j in enumerate(json_response['tracks']):
                uris.append(j['uri'])
                print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")

#Create the playlist

endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

request_body = json.dumps({
          "name": "MusingTheMusic",
          "description": "MusingTheMusic",
          "public": True
        })
response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                        "Authorization":f"Bearer {token}"})

url = response.json()['external_urls']['spotify']
print(response.status_code)

#Fill the playlist

playlist_id = response.json()['id']

endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

request_body = json.dumps({
          "uris" : uris
        })
response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                        "Authorization":f"Bearer {token}"})

print(response.status_code)

print(f'Your playlist is ready at {url}')