""""""
import base64
import csv
import datetime
import http.client
import json
import urllib.error
import urllib.parse
import urllib.request
from random import randint

import IPython
import requests
from flask import (Flask, jsonify, redirect, render_template, request,
                   send_file, send_from_directory, url_for)

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')
app.config.from_pyfile('config.py')

@app.route("/")
def mainpage():
    return render_template("index.html")

'''@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)'''

@app.route("/results/<search>")
def results():
    return render_template("results.html")

'''
@app.route("/api/get_concerts_by_location/<location>")
def getConcerts(location):

    search_term_url = "http://api.songkick.com/api/3.0/search/locations.json?query=" + location + "&apikey=Rt1x5W2pv3pJ1TSS"

    try:
        uResponse = requests.get(search_term_url)
    except requests.ConnectionError:
        print("ConnectionError\n" * 50)

        return "Connection Error"

    Jresponse = uResponse.text
    search_term = json.loads(Jresponse)

    metroarea_id = search_term['resultsPage']['results']['location'][0]['metroArea']['id']

    metroarea_search_url = "http://api.songkick.com/api/3.0/metro_areas/" + str(metroarea_id) + "/calendar.json?apikey=Rt1x5W2pv3pJ1TSS"

    try:
        uResponse = requests.get(metroarea_search_url)
    except requests.ConnectionError:
        return "Connection Error"

    Jresponse = uResponse.text
    upcoming_events_json = json.loads(Jresponse)

    print(upcoming_events_json)

    return jsonify(upcoming_events_json)
'''

@app.route("/api/search_by_artist", methods=['GET', 'POST'])
def search():
    artist = request.form['artist']
    artist_url = "http://api.songkick.com/api/3.0/search/artists.json?apikey=Rt1x5W2pv3pJ1TSS&query=" + artist

    try:
        uResponse = requests.get(artist_url)
    except requests.ConnectionError:
        return "Connection Error"

    Jresponse = uResponse.text

    search_term = json.loads(Jresponse)

    artist_id = search_term['resultsPage']['results']['artist'][0]['id']

    print(artist + ": " + str(artist_id))

    artist_results_url = "http://api.songkick.com/api/3.0/artists/" + str(artist_id) + "/calendar.json?apikey=Rt1x5W2pv3pJ1TSS"

    try:
        uResponse = requests.get(artist_results_url)
    except requests.ConnectionError:
        return "Connection Error"

    Jresponse = uResponse.text
    upcoming_events_json = get_venue_thumbnails(json.loads(Jresponse))
    # upcoming_events_json = json.loads(Jresponse)

    months = ["January", "February", "March","April", "May", "June", "July","August", "September", "October","November", "December"]


    for i in range(len(upcoming_events_json['resultsPage']['results']['event'])):
        event = upcoming_events_json['resultsPage']['results']['event'][i]
        event['start']['date'] = datetime.datetime.strptime(event['start']['date'], "%Y-%M-%d")
        date = event['start']['date']
        event['start']['date_pretty'] = str(date.day) + " " + months[date.month]
        # print(event['start']['date_pretty'])
        event['price_guess'] = "$" + str(randint(78, 367))
        # print(event['price_guess'])

    #return jsonify(upcoming_events_json)
    return render_template("results.html", artistName = artist, events = upcoming_events_json['resultsPage']['results']['event'])


@app.route("/api/get_flights/<start>/<end>")
def get_flights(start, end, depart, land):
    return render_template("flights_dummy.json")

@app.route("/api/get_hotels/<metroArea>")
def get_hotels(metroArea):
    return render_template("hotel_dummy.json")

@app.route("/api/get_metro_area/<lat>/<long>")
def get_metro_area(lat, long):
    return jsonify({
        "name" : "pittsburgh",
        "songkickid" : 22443
    })

def get_venue_thumbnails(upcoming_events):

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '4d867aa0000d4357a33b12ed475959d5',
    }

    for event in upcoming_events['resultsPage']['results']['event']:

        # print(event['venue']['displayName'])
        if event['venue']['displayName'] == 'Unknown venue':
            event['venue']['displayName'] = 'To Be Determined'

        location = event['venue']['displayName'] + " -seating -band -setlist -map"

        params = urllib.parse.urlencode({
            # Request parameters
            'q': location,
            'count': '1',
            'offset': '0',
            'mkt': 'en-us',
            'safeSearch': 'Moderate',
        })

        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v7.0/images/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        URL_dict = json.loads(data.decode('utf-8'))

        if 'value' in URL_dict and len(URL_dict['value']) > 0 and event['venue']['displayName'] != 'To Be Determined':
            event['thumbnailURL'] = URL_dict['value'][0]['thumbnailUrl']
        else:
            event['thumbnailURL'] = '../static/img/ae.jpg'

        # print(event['thumbnailURL'])

    # print(upcoming_events['resultsPage'])
    return upcoming_events

if __name__ == "__main__":
    app.run(host='0.0.0.0')
