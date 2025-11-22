from flask import Flask, request, redirect

app = Flask(__name__)

# SSRF test logging
@app.route("/", defaults={"path": ""}, methods=["GET","POST"])
@app.route("/<path:path>", methods=["GET","POST"])
def catch_all(path):
    print("---- Incoming Request ----")
    print("Path:", path)
    print("Method:", request.method)
    print("Headers:", dict(request.headers))
    print("Query:", dict(request.args))
    print("Body:", request.get_data())
    print("--------------------------")
    return "OK", 200
    
@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    """
    جلب محتوى رابط مُعطى في محددات الاستعلام (Query Parameters).
    مثال للاستخدام: http://127.0.0.1:5000/fetch_data?url=https://example.com
    """
    
    # 1. الحصول على قيمة مفتاح 'url' من محددات الاستعلام (request.args)
    url_to_fetch = request.args.get('url')

    # التحقق مما إذا تم تمرير الرابط
    if not url_to_fetch:
        return jsonify({
            "error": "الرجاء توفير رابط (URL) في مسار الطلب باستخدام المفتاح 'url'.",
            "example": "/fetch_data?url=https://www.google.com"
        }), 400

    try:
        # 2. إرسال طلب HTTP GET لجلب المحتوى
        # يُنصح دائماً باستخدام مهلة (timeout)
        response = requests.get(url_to_fetch, timeout=10)

        # 3. التحقق من حالة الاستجابة وإثارة خطأ إذا كانت سيئة
        response.raise_for_status()

        # 4. إرجاع المحتوى النصي للرابط
        return jsonify({
            "status": "success",
            "url": url_to_fetch,
            # محتوى الصفحة
            "content": response.text,
            "encoding": response.encoding
        })

    except requests.exceptions.HTTPError as e:
        # التعامل مع أخطاء HTTP (مثل 404 Not Found)
        return jsonify({
            "status": "error",
            "message": f"فشل جلب الرابط: خطأ HTTP {response.status_code}",
            "details": str(e)
        }), 500
    except requests.exceptions.RequestException as e:
        # التعامل مع أخطاء الاتصال أو المهلة
        return jsonify({
            "status": "error",
            "message": f"حدث خطأ أثناء محاولة الاتصال بالرابط: {type(e).__name__}",
            "details": str(e)
        }), 500

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
