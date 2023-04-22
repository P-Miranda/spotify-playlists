# Spotify playlists
Get Spotify playlist information from [Web
API](https://developer.spotify.com/documentation/web-api)

# Setup
1. Create Spotify Application:
    1. Go to [Developper dashboard](https://developer.spotify.com/dashboard)
    2. Create app
    3. Add a redirect URI: (eg. `http://localhost:3000`) TODO: add this do config
2. Update configuration:
    1. Make a copy of `.config-template.toml`:
    ```bash
    cp .config-template.toml .config.toml
    ```
    2. Add `client_id` and `client_secret` to `.config.toml`
3. Get authorization code:
    1. Run application once
    2. Add authorization code to `.config.toml` file

# Usage
- Run `make all` target with the following optional variables:
    - USER: string with Spotify user name
    - TOKEN: path to file with Github access token (`.token` by default)

## Example
```Bash
make all TOKEN=.my_token USER=John-Smith
```

## Other Usefull Resources:
- [Youtube Video](https://youtube.com/watch?v=-FsFT6OwE1A)
- [Medium
  Article](https://python.plainenglish.io/bored-of-libraries-heres-how-to-connect-to-the-spotify-api-using-pure-python-bd31e9e3d88a)
