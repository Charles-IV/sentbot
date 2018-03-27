# SentBot 1
### Chat bot created by @SatanicBanana

 > see the discord bot in action at https://discord.gg/UCftebN! - remember - be sensible with it.
 
 > add mine to your server! - https://discordapp.com/oauth2/authorize?&client_id=421772471713267713&scope=bot&permissions=0


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

The bot currently has different personalities (word sets) in each channel. To change this, run `.SERVER_MODE`. To change it back again, run `.CHANNEL_MODE`.


About staff and admins:

Admins are across all personalities and servers that bot is in, however two different people with their own `discord-details.txt` file do not share admins. They can only be assigned by those with access to the file and can run all commands.

Staff can run some administrative commands on the personality (either channel or server) they are added to. They are assigned by an admin, and cannot run commands such as adding or removing staff or shutting down the bot. Only admins can run these. They can run more commands than normal users (which can only run simple commands such as `!LIST_WORDS`.

## Commands

### Command line

Currently, there are no commands for the command line version, although when I get round to being able to save the dictionary, that and restoring will probably be the only ones.

### Discord bot

There are loads. When I understand them, I'll begin documenting them. (or you could make a pr?!)

There are currently 4 tiers of commands - standard, staff, debug and admin.

An admin can run any command, staff can run any but admin commands, and nermal users can only run standard commands.

The prefixes (yes I've got some now!) are as follows:

| Command type: | Standard | Staff | Debug | Admin |
| ------------- |:--------:|:-----:|:-----:|:-----:|
| **Prefix:**   | `!`      | `.`   | `d.`  | `$`   |

Standard text for SentBot to read and make sentences from has no prefix.


### Discord commands

| Prefix:   | Command               | Usage                             | Action    |
|:---------:| --------------------- | --------------------------------- | --------- |
| `$`       | **Admin commands**    |                                   |           |
| `$`       | `SHUTDOWN`            | `$SHUTDOWN`                       | Brings the bot offline. The bot owner will have to bring it back online |
| `$`       | `STAFF_ADD`           | `$STAFF_ADD <StaffName#0000>`     | Adds a staff member to the list of staff for that personality |
| `$`       | `STAFF_REMOVE`        | `$STAFF_REMOVE <StaffName#0000>`  | Removes a staff member to the list of staff for that personality |
| `.`   | **Staff commands**    |                       |       |
| `.`   | `CLEAR_DICTIONARY`    | `.CLEAR_DICTIONARY`   | Delete all words in the dictionary for that personality
| `.`   | `CHANNEL_MODE`        | `.CHANNEL_MODE`       | Switches the personalities in that server to channel mode - each channel has a different set of words and staff. This is default. |
| `.`   | `SERVER_MODE`         | `.SERVER_MODE`        | Switches to one personality shared across the whole server - words and staff are the same for all channels. |
