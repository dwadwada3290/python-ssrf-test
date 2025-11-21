from flask import Flask, request

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
