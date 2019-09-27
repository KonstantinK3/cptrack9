from flask import Flask, request, jsonify
import os
from database import get_codes_from_base

app = Flask(__name__)


@app.route('/')
def index():
    return 'use /codes to get list of codes 30 days befoe and after'

@app.route('/codes', methods=['GET'])
def get_codes():
    if request.method == 'GET':
        ans = get_codes_from_base(30)
        return jsonify(ans)



# @app.route("/weather", methods=['GET'])
# def get_weather():
#     if request.method == 'GET':
#         city = request.args.get('city')
#         return weather(city)


# def weather(city):
#     if city_in_da_base(city):
#         ans = get_city_from_base(city)
#     else:
#         api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={APPID}'
#         resp = requests.get(api_url)
#         resp_text = json.loads(resp.text)
#         ans = {}
#         try:
#             ans["city"] = resp_text["name"]
#             ans["temp"] = resp_text["main"]["temp"]
#             ans["pressure"] = round(resp_text["main"]["pressure"]/1.3332239, 2)
#             ans["wind"] = resp_text["wind"]["speed"]
#             write_city_to_base(ans)
#         except:
#             ans = resp_text
#     return jsonify(ans)


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
