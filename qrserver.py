#!/usr/bin/python

from flask import Flask, request, render_template, send_file
from qrcode import QRCode, ERROR_CORRECT_L
import StringIO


app = Flask(__name__)


@app.route('/qr/<data>')
def qr_data(data):
    return generate_qr_and_send_file(data)


@app.route('/qr/', methods=['GET', 'POST'])
def qr():
    if len(request.values) > 0 and request.values['data']:
        data = request.values['data']

        if request.method == 'POST':
            print 'POST data is', data

        return generate_qr_and_send_file(data)

    return render_template('qr.html')


def generate_qr_and_send_file(data):
    image = generate_qr_as_pil_image(data)
    output = StringIO.StringIO()
    image.save(output, "PNG")
    output.seek(0)
    return send_file(output, attachment_filename="qr.png")


def generate_qr_as_pil_image(data):
    qr = QRCode(error_correction=ERROR_CORRECT_L, box_size=5, border=1)
    qr.add_data(data)
    qr.make()
    return qr.make_image()


if __name__ == '__main__':
    app.run()
