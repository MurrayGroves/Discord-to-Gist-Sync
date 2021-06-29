import discord
import asyncio
import requests
import configparser
import json


# Load config from path
def load_config(path):
    conf = configparser.ConfigParser()
    conf.read(path)

    # Dict of required values and prompts if missing
    required = {"gist": {"id": "Enter gist ID: ", "filename": "Enter gist filename: ", "token": "Enter GitHub token (needs gist scope): ", "username": "Enter GitHub username: "},
                "discord": {"token": "Enter Discord token: ", "channel": "Enter Discord channel ID"}}

    # Ask user for missing values
    updated = False
    for category in required:
        if category not in conf:
            conf[category] = {}

        for key in required[category]:
            if key not in conf[category]:
                conf[category][key] = input(required[category][key])
                updated = True

    if updated:
        conf.write(open(path, "w+"))

    return conf


config = load_config("settings.ini")


# Upload content to the gist
async def upload_gist(content):
    token = config["gist"]["token"]
    gist_id = config["gist"]["id"]
    filename = config["gist"]["filename"]
    username = config["gist"]["username"]

    url = f"https://api.github.com/gists/{gist_id}"
    headers = {"Authorization": f"token {token}", "accept": "application/vnd.github.v3+json"}
    payload = {"files": {filename: {"content": content}}}
    params = {"scope": "gist"}

    req = requests.patch(url, auth=requests.auth.HTTPBasicAuth(username, token), params=params, data=json.dumps(payload))
    

client = discord.Client()


@client.event
async def on_ready():
    print(f"Logged in to Discord as {client.user}")

    channel = await client.fetch_channel(config["discord"]["channel"])
    async for message in channel.history(limit=1):
        new_message = message.content

    print(f"Uploading latest message:\n{new_message}")

    await upload_gist(new_message)


@client.event
async def on_message(message):
    if message.author.bot:  # Ignore message if sent by a bot
        return

    if message.content == "GIST BOT PING":
        await message.channel.send("pong")

    if str(message.channel.id) == config["discord"]["channel"]:
        new_message = message.content
        print(f"New message received:\n{new_message}")
        await upload_gist(new_message)


client.run(config["discord"]["token"])
