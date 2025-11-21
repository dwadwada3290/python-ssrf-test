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

# Redirect ديناميكي
@app.route("/redirect")
def red():
    url = request.args.get("to")
    if url:
        return redirect(url, code=302)
    else:
        return "No 'to' parameter provided", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
