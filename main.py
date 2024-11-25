from flask import Flask, request, render_template
# import markdown

import whatsapp
from chat import chat

app = Flask(__name__)


# receives a notification from whatsapp containing the user message,
# runs it through the conversation chain and sends back a response via whatsapp
@app.route("/webhook", methods=["POST"])
def webhook():
    if whatsapp.webhook(request.json):
        return "", 200
    else:
        # Return a '404 Not Found' if event is not from a WhatsApp API
        return "", 404


# Accepts GET requests at the /webhook endpoint. You need this URL to setup webhook initially.
@app.route("/webhook", methods=["GET"])
def verify():
    if whatsapp.verify(
        request.args.get("hub.verify_token"), request.args.get("hub.mode")
    ):
        # Respond with 200 OK and challenge token from the request
        return request.args.get("hub.challenge"), 200
    else:
        # Responds with '403 Forbidden' if verify tokens do not match
        return "", 403


@app.route("/ask", methods=["GET", "POST"])
def ask():
    # query = request.args.get("query")
    query = request.form["query"]
    if query:
        res = chat(query)
        return res, 200
    else:
        return "", 404


@app.route("/")
def home():
    return render_template("index.html")
    # with open("README.md", "r") as markdown_file:
    #     content = markdown.markdown(markdown_file.read())
    #     return render_template("markdown.html", content=content)


# boots up the server when main.py is run
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
