from unicodedata import name
from unittest import result
from statistics import mean
from flask import Flask, render_template
import googlemaps
import pprint
import requests

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('getapi2.html')

@app.route('/search_index', methods=['POST','GET'])
def search_index(word):
    word = request.form.get('word')
    key = 'AIzaSyCqmC20D0M_x4rrJyAMgdvJaY7-4cXYNBM'
    geo_request_ur1 = 'https://get.geojs.io/v1/ip/geo.json'
    data = requests.get(geo_request_ur1).json()
    client = googlemaps.Client(key)
    loc = {'lat': data['latitude'], 'lng': data['longitude']}
    place_results = client.places_nearby(location=loc, radius=100000, keyword='word',language='ja')
    
    results = []
    photos = []
    for place_result in place_results['results']:
        results.append(place_result)
        if not 'photos' in place_result.keys():
            photo = 'https://hamaotoko.com/wp-content/uploads/2020/09/img_0961-scaled-e1599991033270.jpg'
            photos.append(photo)
        else:
            
            p_value = place_result['photos'][0]['photo_reference']
            photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(p_value,'AIzaSyCqmC20D0M_x4rrJyAMgdvJaY7-4cXYNBM')
            photos.append(photo)
    return render_template('getapi2.html',results=results,photos=photos)


@app.route('/detail/<string:id>')
def detail(id):

    key = 'AIzaSyCqmC20D0M_x4rrJyAMgdvJaY7-4cXYNBM'
    url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+id+"&fields=name%2Crating%2Cformatted_phone_number%2Cformatted_address&key="+key
    #url = "https://maps.googleapis.com/maps/api/place/detailes/xml?key="+key+"&"+id
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return render_template('detail.html',detail=response)

if __name__=='__main__':
    app.run(debug=True)