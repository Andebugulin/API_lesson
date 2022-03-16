def sizes(response):
    json_response = response.json()
    degrees = json_response["response"]["GeoObjectCollection"]['featureMember'][0]["GeoObject"]["boundedBy"]["Envelope"]
    degre = (float(degrees["upperCorner"].split()[0]) - float(degrees["lowerCorner"].split()[0]),
             float(degrees["upperCorner"].split()[1]) - float(degrees["lowerCorner"].split()[1]))

    return list(map(str, degre))