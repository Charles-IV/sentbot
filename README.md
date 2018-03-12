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

Copy `discord-details-template.txt` to `discord-details.txt`. Or rename it, but that may make git pulling hard in future.

Edit `discord-details.txt` appropietly. If you only want one admin, remove `OtherName#0000` and the comma. If you add admin (you can technically have infinite), just add `,OtherAdminName#0000` to the end of line 3. _Make sure there are no spaces!_ This may seem obvious, but I knew this, but made the mistake and spent ages trying to fix it.

Remember if an admin changes their discord name, you will need to edit the file.

You can edit and save this file while the bot is still running - no nead to restart it! (this will be a lifesaver until I figure out save/restore)

Then run it (linux - `python3 sentbot1-discord.py`) and your bot should go online. Be sure to credit me and @SatanicBanana - remember that he gave me the code and let me upload it, and I'm making the code public.

The bot currently has different personalities (word sets) in each channel. To change this, run `SERVER_MODE`. To change it back again, run `CHANNEL_MODE`.

## Commands

### Command line

Currently, there are no commands for the command line version, although when I get round to being able to save the dictionary, that and restoring will probably be the only ones.

### Discord bot

There are loads. When I understand them, I'm begin documenting them. (or you could make a pr?!)
