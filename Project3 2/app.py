# dictionary-api-python-flask/app.py
from flask import Flask, request, jsonify, render_template
from model.dbHandler import match_exact, match_like

app = Flask(__name__)


@app.get("/")
def index():
    """
    DEFAULT ROUTE
    This method will
    1. Provide usage instructions formatted as JSON
    """
    return render_template("index.html")


@app.get("/dict")
def dictionary():
    """
    DEFAULT ROUTE
    This method will
    1. Accept a word from the request
    2. Try to find an exact match, and return it if found
    3. If not found, find all approximate matches and return
    """

    words = request.args.getlist("word")

    if not words:
        response = {"status":"error","word" : "words", "data" : "word not faund"}

        return jsonify(response)

    response = {"words": []}



    for word in words:
        definitions = match_exact(word)

        if definitions:
             response["words"].append({"status":"success","data":definitions,"word":word})
        else:
            definitions = match_like(word)
            if definitions:
                response["words"].append({"status": "partial", "data":definitions, "word":word})
            else:
                response["words"].append({"status":"error","data": "word not found", "word":word})
                
    return render_template("results.html", response=jsonify(response))


if __name__ == "__main__":
    app.run()
