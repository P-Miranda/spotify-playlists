#!/usr/bin/env python3
# Python script to get playlists from Spotify user

import argparse
import json
import requests
import subprocess
import toml
from urllib.parse import urlencode
import webbrowser


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="spotify_playlists", description="Get Spotify playlists"
    )
    parser.add_argument(
        "config_file",
        type=str,
        help="Path to configuration file",
    )
    parser.add_argument("user", type=str, help="Spotify account user name")

    return parser.parse_args()


def read_config_file(config_file):
    return toml.load(config_file)


def get_all_repos_from_user(user, client_id):

    # try to get max number of pages
    # check: https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28
    # /user/repos endpoint
    user_repos_endpoint = f"https://api.github.com/user/repos"
    params = {"per_page": 100, "page": 1}

    repos = []
    get_next_page = True
    # get all other repo pages
    while get_next_page == True:
        get_next_page = get_repos_from_api(
            repos,
            requests.get(user_repos_endpoint, auth=(user, client_id), params=params),
        )
        # next iteration: get next page
        params["page"] = params["page"] + 1

    return repos


def request_user_authorization(client_id, scopes):
    endpoint = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:3000",
        "scope": scopes,
    }

    print("First time access instructions:")
    print("1. Login to Spotify and agree")
    print("2. Copy the code=<auth_code> from the redirect url into .toml file")
    print("3. Run the script again")

    webbrowser.open(f"{endpoint}?{urlencode(params)}")


if __name__ == "__main__":
    print("Get Spotify playlists")

    args = parse_arguments()
    config = read_config_file(args.config_file)
    print(config)

    # scopes = "playlist-read-private playlist-read-collaborative"
    # request authorization code if not set
    if not config["auth_code"]:
        request_user_authorization(config["client_id"], config["scopes"])
