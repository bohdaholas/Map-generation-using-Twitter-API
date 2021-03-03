import folium
from geopy.geocoders import Nominatim
from flask import Flask, request, render_template
import twitter2

app = Flask(__name__)


@app.route('/')
def get_username():
    """
    Displays html-form that has:
    1) Username field
    2) Button to submit the form
    """
    # Display form
    return render_template("index.html")


@app.route('/map', methods=['POST'])
def display_map():
    """
    Get the entered username in the form and display the html-map
    """
    if request.method == 'POST':
        username = request.form.get('username')
        folium_map = build_map(get_followers_names_and_locations(username))
        return folium_map


def get_followers_names_and_locations(username):
    """
    Get followers names and locations from a json object that was retrieved
    from a function "get_followers_data" in twitter2.py module.
    """
    followers_json = twitter2.get_followers_data(username)
    followers = []
    nom = Nominatim(user_agent="map-generation")
    for follower in followers_json['users']:
        name, location = follower['screen_name'], follower['location']
        location = nom.geocode(location)
        if location:
            followers.append((name, (location.latitude, location.longitude)))
    return followers


def build_map(followers: list):
    """
    Build a folium map and save it as an HTML file
    """
    folium_map = folium.Map()
    for follower in followers:
        folium.Marker(location=[*follower[1]], popup=follower[0]).add_to(folium_map)
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)