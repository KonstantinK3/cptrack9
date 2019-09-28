from flask import Flask, request, jsonify, send_file, render_template
import os, json, hashlib, qrcode
from database import get_codes_from_base, get_code_by_date

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

#возвращаем список кодов на 30 до текущей даты и 30 дней после
@app.route('/codes', methods=['GET'])
def get_codes():
    if request.method == 'GET':
        ans = get_codes_from_base(30)
        return jsonify(ans)

def get_hash(request):
    if request.method == 'GET':
        name = request.args.get('name')
        surname = request.args.get('surname')
        passport = request.args.get('passport')
        issueDate = request.args.get('issueDate')
        dueDate = request.args.get('dueDate')
        areas = request.args.get('areas')

        #получение кода из базы
        code = get_code_by_date(issueDate)

        #формирование строки для кодирования
        credentials_w_code = f"{name} {surname} {passport} {issueDate} {dueDate} {areas} {code}"

        hash = hashlib.sha1(credentials_w_code.encode()).hexdigest()
        credentials_w_hash = f"{name} {surname} {passport} {issueDate} {dueDate} {areas} {hash}"

        return (credentials_w_hash)

@app.route('/tickets', methods=['GET'])
def get_credentials_hash():
    return get_hash(request)


@app.route('/qr', methods=['GET'])
def get_qr():
    if request.method == 'GET':

        #формирование картинки
        img = qrcode.make(get_hash(request))
        filename = "qr1.png"
        img.save(filename)

        return (send_file(filename, mimetype='image/png'))

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
