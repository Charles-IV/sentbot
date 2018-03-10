# SentBot 1
### Chat bot created by @SatanicBanana

 > see the discord bot in action at https://discord.gg/UCftebN! - remember - be sensible with it.

## Usage

Use `sudo pip install module-name` to install required modules for the version you want to run (e.g. `colorama` and `discord`)

Of course, if you're on Windows, it's slightly different. Go Google how to do it.

### Command line

To run in terminal, simply run sentbot1.py.
e.g. on linux - `python3 sentbot1.py` from the same directory.

### Discord bot

To run it as a discord bot, you need to create a bot app at https://discordapp.com/developers/applications/me

Replace the `token` in `client.run('token')` (on the last line) with your token. (Google it)

Then replace `BotName#0000` (on line 305 - at time of writing) with your bots username. Make sure you keep the `"` on either side.

Then replace all occurences of `OwnerName#0000` with the username of the user with admin rights of the bot.

Then run it (linux - `python3 sentbot1-discord.py`) and your bot should go online. Be sure to credit me and @SatanicBanana - remember that he gave me the code and let me upload it, and I'm making the code public.

Don't worry, I intend to make this simpler - soon you may be able to paste them into a .gitignore'd file, and maybe even have multiple admins.

## Commands

### Command line

Currently, there are no commands for the command line version, although when I get round to being able to save the dictionary, that and restoring will probably be the only ones.

## Discord bot

There are loads. When I understand them, I'm begin documenting them. (or you could make a pr?!)
