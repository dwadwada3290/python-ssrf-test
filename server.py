from flask import Flask, request, redirect, jsonify, Response
import requests

app = Flask(__name__)

@app.route('/fake.png')
def fake_image():
    # نرجع Redirect إلى ملف غير صورة
    return redirect('/not_image', code=302)

# الملف الذي يتم التحويل إليه
@app.route('/not_image')
def not_image():
    # محتوى نصي بدل صورة
    return Response("hello its me", mimetype='image/x-fklsflsd+png')
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
