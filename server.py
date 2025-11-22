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


@app.route("/proxy")
def proxy():
    # الرابط الذي يريد العميل الوصول إليه
    external_url = request.args.get("url")
    
    if not external_url:
        return "Please provide ?url=", 400

    # إرسال الطلب إلى السيرفر الخارجي
    external_response = requests.get(external_url)

    # إعادة الردّ للعميل
    return Response(
        external_response.content,                     # نفس البيانات
        status=external_response.status_code,          # نفس الحالة
        headers={"Content-Type": "image/x-dwdawdwa+png"}          # تغيير الـ Content-Type حسب رغبتك
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
