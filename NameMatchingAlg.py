from MockData import e_data, acorns_data
from rosette.api import API, NameSimilarityParameters, RosetteException

api_key = "5457c89da0536d48221ae2659e479568"


def name_comparison(key, acorns_name, name):
    """Return similarity score between two names using Rosette API."""
    api = API(key)  # Create instance of API
    params = NameSimilarityParameters() # All documented on GitHub.
    params["name1"] = {"text": acorns_name, "language": "eng", "entityType": "PERSON"}
    params["name2"] = {"text": name, "entityType": "PERSON"}
    try:
        return api.name_similarity(params)
    except RosetteException as e:
        print(e)


def acorns_alg(info):  # Using tuples seems pretty helpful for data storage
    """Matches employers' data to Acorns accounts using first and last
        name, last four digits of social and optional email. 
        Returns matched ID and a score between 0 and 1 representing the confidence
        level of the match."""
    name, social, *email = info
    match = [key for key in acorns_data if social in key]  # Social should be only certain constant between data
    certainty_scores = []
    for acorns_info in match:
        acorns_name, acorns_social, *acorns_email = acorns_info
        if email == acorns_email and len(acorns_email) > 0:
            return {"id": acorns_data[acorns_info], "score": 1.0} # Same social and same verified email should be accurate enough to return certain match
        certainty_scores.append(name_comparison(api_key, acorns_name, name)["score"])
    maximum_score = max(certainty_scores) # Get the maximum score
    return {"id": acorns_data[match[certainty_scores.index(maximum_score)]], "score": maximum_score} # Return the ID and accuracy of the search as a dictionary


def directory_to_id(data):
    """Go through a company's employee directory and return dictionary of employee's info to Acorns IDs."""
    info_to_id = dict()
    for info in data:
        info_to_id[info] = acorns_alg(info)["id"]
    return info_to_id

if __name__ == "__main__":
    print(directory_to_id(e_data))
