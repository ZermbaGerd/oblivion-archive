from flask import Flask
from flask import request, render_template, make_response, url_for, send_from_directory
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    response = make_response(render_template("index.html"), 200)
    return response

@app.route("/entry/<string:entry_name>")
def get_entry(entry_name):
    print("received a properly routed request to an entry")
    # get the data for the entry (based on how many times we've seen it)
    if not request.cookies.get(entry_name):
        entryData = getEntryData(entry_name, 0)
    else:
        entryData = getEntryData(entry_name, request.cookies.get(entry_name))
    
    # check to see if entry data is fucked up
    if entryData[0] == None or entryData[1] == None or entryData[2] == None:
        print(" there should be an error here") # TODO: make this actually throw an error, and make sure getEntryData does proper checking for whether the resources exists
    

    # make the HTTP Response
    response = make_response(render_template("entry.html", description=entryData[0], metadata=entryData[1], pictureURL=entryData[2]))

    # if they haven't visited yet, set their cookie
    if not request.cookies.get(entry_name) or request.cookies.get(entry_name) == "0":
        response.set_cookie(entry_name, "1")
    
    else: # otherwise increment it
        response.set_cookie(entry_name, str(int(request.cookies.get(entry_name))+1))
    
    return response


# resets all of the cookies back to 0. i think the check i edited in the "if they haven't visited yet" line should be ok with it
@app.route("/reset_entries")
def reset_entries():
    # TODO: make this not hardcoded in this function - so that you can use the same list of index.html and this
    entryList = ["Example",
        "Second_Example",
        "Instagram_Account_-_Cristiano_Ronaldo",
        "Notre-Dame_de_Paris"]
    
    response = make_response()
    for entry in entryList:
        if request.cookies.get(entry):
            response.set_cookie(entry, "0")
    
    return response, 200

def generateUsername():
    return "placeholder"


def getEntryData(entry, time):
    """
    Based on a properly structured entry time and the time this is being accessed, return the right resources
    """
    metadata = None
    description = None

    time = int(time)

    # clean time
    if time > 3:    # TODO: fix this to make sure we're working with the right number of iterations
        time = 3
    if time < 0:
        time = 0

    # open the json file with its data      # TODO this should be wrapped in a try/except or sumn
    # url_for('static', filename="descriptions/" + entry + ".json") - tried this for a while, didn't work
    # TODO: change this so it's not hardcoded
    with open("static/descriptions/"+ entry+".json") as infile:
        content = json.load(infile)
        metadata = content[str(time)]["metadata"]
        description = content[str(time)]["description"]

    # look in the assets folder for the picture associated with the given entry at the given number of accesses
    picURL = url_for('static', filename="assets/" + entry + "/" + str(time) + ".png")

    return description, metadata, picURL