""""""
import json

import IPython
import requests
from flask import (Flask, jsonify, redirect, render_template, request,
                   send_file, url_for, request, send_from_directory)


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
    upcoming_events_json = json.loads(Jresponse)

    #return jsonify(upcoming_events_json)
    return render_template("results.html", artistName = artist, events = upcoming_events_json['resultsPage']['results']['events'])


@app.route("/api/get_flights/<start>/<end>")
def get_flights(start, end, depart, land):
    return render_template("flights_dummy.json")

@app.route("/api/get_hotels/<metroArea>")
def get_hotels(metroArea):
    return render_template("hotel_dunny.json")

@app.route("/api/get_metro_area/<lat>/<long>")
def get_metro_area(lat, long):
    return jsonify({
        "name" : "pittsburgh",
        "songkickid" : 22443
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0')
