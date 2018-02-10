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
    params = ""
    return render_template("templates/index.html")

@app.route("/api/get_concerts_by_location/<location>")
def getConcerts(location):

    return render_template("concerts_dummy_pittsburgh.json")

    # search_term_url = "http://api.songkick.com/api/3.0/search/locations.json?query=" + search_term + "&apikey=Rt1x5W2pv3pJ1TSS"
    #
    # try:
    #     uResponse = requests.get(search_term_url)
    # except requests.ConnectionError:
    #     print("ConnectionError\n" * 50)
    #
    #     return "Connection Error"
    #
    # Jresponse = uResponse.text
    # search_term_json = json.loads(Jresponse)
    #
    # print(search_term_json)
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


@app.route()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
