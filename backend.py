""""""
import json

import IPython
import requests
from flask import (Flask, jsonify, redirect, render_template, request,
                   send_file, url_for)

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')
app.config.from_pyfile('config.py')

@app.route("/")
def mainpage():
    return render_template("templates/index.html")

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

    # print(search_term['resultsPage']['results'][''])

    # print(search_term)
    return render_template("concerts_dummy_pittsburgh.json")


    #
    # IPython.embed()
    #
    # # metroarea_id = str(search_term_json[resultsPage]results.metroArea.id)
    #
    # return jsonify(search_term_json)

    #
    # metroarea_search_url = "http://api.songkick.com/api/3.0/metro_areas/" + metroarea_id + "/calendar.json?apikey=Rt1x5W2pv3pJ1TSS"
    #
    # try:
    #     uResponse = requests.get(metroarea_search_url)
    # except requests.ConnectionError:
    #     return "Connection Error"
    #
    # Jresponse = uResponse.text
    # upcoming_events_json = json.loads(Jresponse)
    #
    # return jsonify(upcoming_events_json.resultsPage.results.event)

@app.route("/api/search_by_artist/<search_term>")
def search(search_term):
    return render_template("concerts_dummy_pittsburgh.json")

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
