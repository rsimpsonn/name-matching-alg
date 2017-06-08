from MockData import e_data, acorns_data
from rosette.api import API, NameSimilarityParameters, RosetteException


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
    """Intended to match employers' data to Acorns accounts using first and last
        name, last four digits of social and optional email"""
    name, social, *email = info
    match = [key for key in acorns_data if social in key]  # Social should be only certain constant between data
    certainty_scores = []
    for x in match:
        acorns_name, social, *email = x
        certainty_scores.append(name_comparison("5457c89da0536d48221ae2659e479568", acorns_name, name))
    maximum_score = max(certainty_scores) # Get the maximum score
    return acorns_data[match[certainty_scores.index(maximum_score)]]


def directory_to_id(data):
    """Go through a company's employee directory and return dictionary of employee's info and Acorns ID's."""
    info_to_id = dict()
    for info in data:
        info_to_id[info] = acorns_alg(info)
    return info_to_id

if __name__ == "__main__":
    print(directory_to_id(e_data))
