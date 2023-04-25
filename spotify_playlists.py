#!/usr/bin/env python3
# Python script to get playlists from Spotify user

import argparse
import base64
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


def write_config(config, filename):
    toml_string = toml.dumps(config)
    with open(filename, "w") as f:
        f.write(toml_string)


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


def encode_credentials(config):
    return base64.b64encode(
        config["client_id"].encode() + b":" + config["client_secret"].encode()
    ).decode("utf-8")


def request_access_token(config, config_file):
    endpoint = "https://accounts.spotify.com/api/token"
    header = {
        "Authorization": "Basic " + encode_credentials(config),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params = {
        "grant_type": "authorization_code",
        "code": config["auth_code"],
        "redirect_uri": "http://localhost:3000",
    }
    response = requests.post(endpoint, headers=header, data=params)
    response_json = response.json()

    # print(response_json)
    if response_json:
        config["access_token"] = response_json["access_token"]
        config["refresh_token"] = response_json["refresh_token"]
        write_config(config, config_file)


def refresh_access_token(config, config_file):
    endpoint = "https://accounts.spotify.com/api/token"
    header = {
        "Authorization": "Basic " + encode_credentials(config),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params = {
        "grant_type": "refresh_token",
        "refresh_token": config["refresh_token"],
    }
    response = requests.post(endpoint, headers=header, data=params)
    response_json = response.json()
    # print(response_json)
    if response_json:
        config["access_token"] = response_json["access_token"]
        write_config(config, config_file)


def get_playlist_info(config):
    endpoit = "https://api.spotify.com/v1/me/playlists"
    header = {
        "Authorization": "Bearer " + config["access_token"],
    }
    params = {
        "limit": 50,
        "offset": 0,
    }
    response = requests.get(endpoit, headers=header, params=params)
    response_json = response.json()
    # print(response_json)
    with open("playlists.json", "w") as f:
        json.dump(response_json, f, indent=4)

    playlist_info_from_json(response_json)


def playlist_info_from_json(json_data):
    for playlist in json_data["items"]:
        print(f'{playlist["name"]}: {playlist["tracks"]["total"]} tracks')


if __name__ == "__main__":
    print("Get Spotify playlists")

    args = parse_arguments()
    config = read_config_file(args.config_file)
    # print(config)

    # Initial setup: obtain access and refresh tokens
    if not config["refresh_token"]:
        # request authorization code if not set: 1st run
        if not config["auth_code"]:
            request_user_authorization(config["client_id"], config["scopes"])
        # request access and refresh tokens: 2nd run
        else:
            request_access_token(config, args.config_file)
    # Regular run: check for valid access token or refresh
    else:
        refresh_access_token(config, args.config_file)

    # Regular operation:
    get_playlist_info(config)
