'''
ListTuner - Hendrik Scheeres
spotify.py

This file contains all the funtctions used in the main routes to make requests to the Spotify API.
The functions return the response data as formatted dictionaries.
 '''

import requests
import statistics
from math import floor

from models import *


''' Main functions '''

def get_user_info(headers):
    ''' requests the user information from the Spotify API and returns it as a formatted dictionary'''

    # request the user information from the Spotify API
    res = requests.get("https://api.spotify.com/v1/me", headers=headers)

    # check if the request was succesful
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    res = res.json()

    username = res["display_name"]

    # request the current users playlists
    params = {'limit': 50}
    res = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers, params=params)

    # check if the request was succesful
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    res = res.json()

    # create a list for all the playlist information
    playlists = []

    items = []
    items += res["items"]

    # if the user has more than 50 playlist make multiple requests to the Spotify API using the offset
    total = int(res["total"])
    if total > 50:

        chunks = int(floor(total/50))
        offset = 0

        for i in range(chunks):

            # request the remaining user playlists
            offset += 50
            params = {'limit': 50, 'offset': offset}
            res = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers, params=params)

            # check if the request was succesful
            if res.status_code != 200:
                raise Exception("ERROR: API request unsuccessful.")

            res = res.json()

            # append the playlist items to the items list
            items += res["items"]

    # extract all the relevant information from the response data and save it in a dict
    for item in items:

        playlist = {
        "name": item["name"],
        "id": item["id"],
        "tracks": item["tracks"]
        }

        # append the playlist to the list if it has 100 tracks or less
        if int(item["tracks"]["total"]) <= 100:
            playlists.append(playlist)

    # save the user info in a dict
    user_info = {
    "username": username,
    "playlists": playlists,
    "num_playlists": len(playlists)
    }

    return user_info



def get_playlist_info(id, headers):
    ''' requests the playlist information from the Spotify API using the playlist id and returns it as a formatted dictionary'''

    # request the playlist information from the Spotify API
    res = requests.get(f"https://api.spotify.com/v1/playlists/{id}", headers=headers)

    # check if the request was succesful
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    res = res.json()

    # extract all the relevant information from the response data
    tracks = []

    items = res["tracks"]["items"]
    for item in items:

        # check if the track has a valid Spotify ID
        if item["track"]["id"]:

            # list the track artists
            artist_names = []
            artists = item["track"]["artists"]
            for artist in artists:
                artist_names.append(artist["name"])

            # save the track info in a dict
            track = {
            "id": item["track"]["id"],
            "name": item["track"]["name"],
            "artist_names": artist_names,
            "preview_url": item["track"]["preview_url"]
            }

            # append that to the tracks list
            tracks.append(track)

    # save the playlist info in a dict
    playlist = {
    "name": res["name"],
    "id": res["id"],
    "num_tracks": len(tracks),
    "tracks": tracks,
    "external_urls": res["external_urls"]["spotify"]
    }

    return playlist



def get_seal_features(headers):
    ''' requests the track features from the Spotify API for the seal playlists in the database and returns it as a formatted dict '''

    # get seals playlist info from database
    seals = Seals.query.all()

    # create a list with the track features of each seal playlist
    seals_info = []

    for seal in seals:

        # get the track features
        try:
            seal_track_features = get_track_features(playlist_id=seal.playlist_id, headers=headers)
        except Exception as e:
            raise Exception(e)


        # save the seal information and track features in a dict
        seal_info = {
        "description": seal.description,
        "playlist_id": seal.playlist_id,
        "playlist_name": seal.playlist_name,
        "playlist_creator": seal.playlist_creator,
        "playlist_href": seal.playlist_href,
        "track_features": seal_track_features
        }

        seals_info.append(seal_info)

    return seals_info



def get_track_features(playlist_id, headers):
    ''' requests track features of a playlist from the Spotify API using the playlist id and it returns as a formatted dict '''

    # get the playlist track info from the Spotify API
    res = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers)

    # check if the request was succesful
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    res = res.json()

    # extract all the relevant information from the response data
    track_names = []
    track_ids = []
    track_artist_names = []
    track_artist_ids = []
    items = res["items"]

    # loop through each track of the playlist
    for item in items:
        track = item["track"]

        # check if the track has a valid Spotify id
        if track["id"]:
            track_names.append(track["name"])
            track_ids.append(track["id"])

            # loop throught the artists of each track
            artists = track["artists"]
            for artist in artists:
                track_artist_names.append(artist["name"])
                track_artist_ids.append(artist["id"])

    # split the artist ids list into chunks to account for the request limit of 50
    track_artist_ids = make_chunks(list=track_artist_ids, n=50)

    # extract the genre info for all the tracks
    genres_list = []
    for chunk in track_artist_ids:

        try:
            genres = get_track_genres(track_artist_ids=chunk, headers=headers)
        except Exception as e:
            raise Exception(e)

        genres_list += genres

    # sort the genres intor a dictionary
    genres_dict = sort_track_genres(genres_list)

    # make a list of the track numbers
    track_nums = list(range(1, (len(items) + 1)))

    # get the track feature values and the average track feature values
    try:
        track_feature_values, analysis_urls = get_track_feature_values(track_ids=track_ids, headers=headers)
    except Exception as e:
            raise Exception(e)

    avg_track_feature_values = calc_avg_track_feature_values(track_feature_values)

    # save the track info in a dict
    track_features = {
    "track_names": track_names,
    "track_nums" : track_nums,
    "track_ids": track_ids,
    "track_artist_names": track_artist_names,
    "track_artist_ids": track_artist_ids,
    "track_feature_values": track_feature_values,
    "avg_track_feature_values": avg_track_feature_values,
    "genres_dict": genres_dict,
    "analysis_urls": analysis_urls
    }

    return track_features


''' Helper functions'''

def get_track_genres(track_artist_ids, headers):
    ''' requests the genres from the Spotify API using the artist ids and returns it as a list genre names '''

    # join the artis_ids in a comma seperated string
    artist_ids_list = ",".join(track_artist_ids)

    # request the artists info of all the tracks
    params = {"ids": artist_ids_list}
    res = requests.get("https://api.spotify.com/v1/artists", headers=headers, params=params)

    # check if the request was succesful
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    res = res.json()

    # extract the genres names from the response data
    genres = []
    artists = res["artists"]

    for artist in artists:
        genres += artist["genres"]

    return genres



def sort_track_genres(genres_list):
    ''' sorts and counts the occurences of each genre in a list and returns it as a dict '''

    # sort the list
    genres_list = sorted(genres_list)

    # create a dictionary that saves the occurences of each genre as a value with the genre as the key
    genres_dict = {}
    for key in genres_list:
        genres_dict[key] = genres_list.count(key)

    return genres_dict



def get_track_feature_values(track_ids, headers):
    ''' requests the track feature values from the Spotify API for a bundle of tracks using the track ids and returns it as a formatted dict '''

    # join the track_ids in a comma seperated string
    track_ids_list = ",".join(track_ids)

    # request the audiofeatures of all the tracks
    params = {"ids": track_ids_list}
    res = requests.get("https://api.spotify.com/v1/audio-features", headers=headers, params=params)

    # check if the request was succesful
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    res = res.json()

    # extract the relevant information from the response data
    audio_features = res["audio_features"]

    danceability = []
    energy = []
    loudness = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    analysis_urls = []

    for feature in audio_features:

        danceability.append(float(feature["danceability"]))
        energy.append(float(feature["energy"]))
        loudness.append(float(feature["loudness"]))
        speechiness.append(float(feature["speechiness"]))
        acousticness.append(float(feature["acousticness"]))
        instrumentalness.append(float(feature["instrumentalness"]))
        liveness.append(float(feature["liveness"]))
        valence.append(float(feature["valence"]))
        tempo.append(float(feature["tempo"]))
        analysis_urls.append(feature["analysis_url"])

    # save the features of the track in a dict
    track_feature_values = {
    "danceability": danceability,
    "energy": energy,
    "loudness": loudness,
    "speechiness": speechiness,
    "acousticness": acousticness,
    "instrumentalness": instrumentalness,
    "liveness": liveness,
    "valence": valence,
    "tempo": tempo,
    }

    return track_feature_values, analysis_urls



def calc_avg_track_feature_values(track_feature_values):
    ''' calculates the average track features from the track features and returns it as a dict '''

    avg_track_feature_values = {}

    # calculate the avarege value for each feature
    for key, value in track_feature_values.items():

        # select only the features needed for the chart
        if key != "loudness" and key != "tempo":
            avg_track_feature_values[key] = round(statistics.mean(value), 2)

    return avg_track_feature_values



def make_chunks(list, n):
    ''' seperates a list into n-sized chunks and returns a list containing the chunks '''

    # index the chunks and save them in a list
    lists = []
    for i in range(0, len(list), n):
        lists.append(list[i:i+n])

    return lists
