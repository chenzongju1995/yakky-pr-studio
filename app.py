import hashlib
import base64
import urllib.request
import urllib.parse
import json
import os
from flask import Flask, send_file, request, jsonify

app = Flask(__name__)

KD_EBUSINESS_ID = '1922454'
KD_API_KEY = '1ff4963d-b427-4901-afb9-5788b998aba0'
KD_API_URL = 'https://api.kdniao.com/Ebusiness/EbusinessOrderHandle.aspx'


@app.route('/')
def index():
    return send_file('templates/index.html')


@app.route('/api/track', methods=['POST'])
def api_track():
    data = request.get_json()
    req_obj = {
        'OrderCode': '',
        'ShipperCode': data.get('ShipperCode', 'SF'),
        'LogisticCode': data.get('LogisticCode', '')
    }
    customer_name = data.get('CustomerName', '')
    if customer_name:
        req_obj['CustomerName'] = customer_name
    req_data = json.dumps(req_obj)
    md5_hex = hashlib.md5((req_data + KD_API_KEY).encode()).hexdigest()
    data_sign = base64.b64encode(md5_hex.encode()).decode()
    body = urllib.parse.urlencode({
        'RequestData': req_data,
        'EBusinessID': KD_EBUSINESS_ID,
        'RequestType': '1002',
        'DataSign': data_sign,
        'DataType': '2'
    }).encode()
    try:
        resp = urllib.request.urlopen(
            urllib.request.Request(KD_API_URL, data=body, headers={'Content-Type': 'application/x-www-form-urlencoded'}),
            timeout=10
        )
        return jsonify(json.loads(resp.read()))
    except Exception as e:
        return jsonify({'Success': False, 'Reason': str(e)})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
