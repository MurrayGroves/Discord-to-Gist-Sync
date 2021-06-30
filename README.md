# Discord to Gist Sync

Syncs the latest message from a Discord channel to a provided Gist.

## Configuration
The program will prompt you for all the required details when you first run it, here is an explanation of all the details:

- Gist ID: The ID of the gist you want to update (you must create it first).
- Gist filename: The filename of the file within the gist that you want to update.
- GitHub token: A github personal access token with the 'gist' scope.
- GitHub username: The GitHub username that owns/has access to the gist.
- Discord Token: The Discord bot token for a bot that has read access (and read history) to the provided channel.
- Discord channel: The Discord ID of the channel you want to read from.
