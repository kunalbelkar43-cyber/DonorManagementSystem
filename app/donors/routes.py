from app.donors import donors

@donors.route("/")
def index():
    return "Donors Module Working"