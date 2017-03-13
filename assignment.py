from flask import Flask, render_template, redirect, url_for, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import os
import googlemaps
import requests

google_key = "AIzaSyATJAVx9fPMrYIwvOTkHj2Q0pP7r6WgtKM"
app = Flask(__name__, template_folder="templates")
app.config['GOOGLEMAPS_KEY'] = "AIzaSyATJAVx9fPMrYIwvOTkHj2Q0pP7r6WgtKM"
GoogleMaps(app)

gmaps = googlemaps.Client(key=google_key)

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

# /<my_location>
@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form

        geocode_result = gmaps.geocode(request.form['LocationCity'])
        geo = geocode_result[0]
        geometry = geo['geometry']

        location = geometry['location']
        latitude = location['lat']
        longitude = location['lng']
        print "Lat, Lng: ", latitude, longitude

        north = latitude + 0.5
        south = latitude - 0.5
        west = longitude - 0.5
        east = longitude + 0.5
        print "North, South, West, East: ", north, south, west, east

        earthquakes = requests.get("http://api.geonames.org/earthquakesJSON?north=" + str(north) + "&south=" + str(south) + "&east=" + str(east) + "&west=" + str(west) + "&username=davethefinder")
        earthquakesJSON = earthquakes.json()

        markers = earthquakesJSON['earthquakes']
        marks = []

        for x in markers:
            mark = {
            'icon': '//maps.google.com/mapfiles/ms/icons/red-dot.png',
            'lat': x['lat'],
            'lng': x['lng'],
            'infobox': (
                        "Datetime: %s" % x['datetime'] + ""
                        "<br>Latitude: " + str(x['lat']) + ""
                        "<br>Longitude: " + str(x['lng']) + ""
                        "<br>Depth: " + str(x['depth']) + ""
                        "<br>EQID: %s" % x['eqid'] + ""
                        "<br>Magnitude: " + str(x['magnitude']) + ""
                        "<br>Source: %s" % x['src'] + ""
                        )
            }
            marks.append(mark)

        eqmap = Map(
            identifier="eqmap", varname="eqmap",
            style=(
                "height:75%;"
                "width:75%;"
                "top:1;"
                "left:1;"
                "right:1;"
                "position:absolute;"
            ),
            lat = latitude, lng = longitude, markers = marks, zoom = 9
        )

        return render_template('result.html', eqmap=eqmap)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug = True, use_reloader = True, host='0.0.0.0', port=port)
