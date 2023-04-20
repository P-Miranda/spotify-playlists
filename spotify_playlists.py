#!/usr/bin/env python3
# Python script to get playlists from Spotify user

import argparse
import json
import requests
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="spotify_playlists", description="Get Spotify playlists"
    )
    parser.add_argument(
        "token_file",
        type=str,
        help="Path to file containing github access token with repository permissions",
    )
    parser.add_argument("user", type=str, help="Spotify account user name")

    return parser.parse_args()


def get_token(token_file):
    with open(token_file, "r") as token_file:
        return token_file.readline().rstrip("\n")


def get_repos_from_api(repo_list, api_response):
    repos = api_response.json()
    if repos == []:
        return False

    for repo in repos:
        tmp_dict = {}
        tmp_dict["name"] = repo["name"]
        tmp_dict["html_url"] = repo["html_url"]
        tmp_dict["private"] = repo["private"]
        repo_list.append(tmp_dict)

    return True


def get_all_repos_from_user(user, token):

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
            repos, requests.get(user_repos_endpoint, auth=(user, token), params=params)
        )
        # next iteration: get next page
        params["page"] = params["page"] + 1

    return repos


if __name__ == "__main__":
    print("Get Spotify playlists")

    args = parse_arguments()

    token = get_token(args.token_file)
    print(f"Token: {token}\nUser: {args.user}")
