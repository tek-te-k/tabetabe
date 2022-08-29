from unicodedata import name
from unittest import result
from statistics import mean
from flask import Flask, render_template, url_for, request
import googlemaps
import pprint, os, json, requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main.html',)

@app.route('/search_index', methods=['GET', 'POST'])
def search_index():
    if request.method == 'POST':
        word = request.form.get('word')
        key = 'AIzaSyCqmC20D0M_x4rrJyAMgdvJaY7-4cXYNBM' #APIキー
        print(word)

        client = googlemaps.Client(key) #インスタンス生成
        # geo_request_url = 'https://get.geojs.io/v1/ip/geo.json'
        # geo_data = requests.get(geo_request_url).json()
        # print(geo_data['latitude'])
        # print(geo_data['longitude'])
        loc = {'lat': 33.9564096, 'lng': 131.2706817} # 軽度・緯度を取り出す
        place_results = client.places_nearby(location=loc, radius=10000, keyword={word} ,language='ja') #半径1000m以内のカフェ情報を取得
        #pprint.pprint(place_results)
        results = []
        photos = []
        p_values = []
        print(place_results)
        for place_result in place_results['results']:
            # 配列にphotosが存在しないとき、NO IMAGE画像を表示。
            if not 'photos' in place_result.keys() or place_result['business_status'] == "CLOSED_TEMPORARILY" or 'opening_hours' not in place_result:
                pass
                # photo = '/static/img/NO_IMAGE.png'
                # photos.append(photo)
                # p_values.append(p_value)
            else:
                results.append(place_result)
                p_value = place_result['photos'][0]['photo_reference']
                p_values.append(p_value)
                photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(p_value,key)
                photos.append(photo)
        return render_template('main.html',results=results,photos=photos,p_values=p_values)
    else:
        return render_template('main.html')

@app.route('/detail/<string:id>/<p_ref>')
def detail(id,p_ref):
    key = 'AIzaSyD_j3p1GZ9FWKt5Do_yRBdi_FvIFgNgqyQ' #APIキー
    url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&language=ja&key={}".format(id,key)
    photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(p_ref,key)

    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    return render_template('detail.html',details=response,photo=photo)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__=='__main__':
    app.run(debug=True)
    #app.run("0.0.0.0")