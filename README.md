# discord-bot

This is a small bot for [our discord server][server] :robot:

The main purpose for this bot is to replace the [Invite-Role
Bot][invitebot], since it was down more than it was up - but we also
wanted to use the same functionality: adding a role to a member
according to an invite (new user uses invite `xyz` and gets role `foo`,
another user joins with invite `abc` and gets role `bar`).  
Unfortunately this is not yet implemented in the [Discord API][api] and
a [bug report/feature request][issue] for this is already over 2 years
old.  
That's why there is (of course) [a catch][catch] ...

Nevertheless and since it's a good excuse to learn and use python, have
fun with this bot :tada:

## Installation

First create a [virtualenv][]:

```bash
python3 -m venv .venv
source .venv/bin/activate # bash/zsh
. .venv/bin/activate.fish # fish
```

Then install the requirements:

```bash
pip3 install -r requirements.txt
```

## Usage

Copy `env.tmpl` to `.env` and replace `xyz` with the proper values.  
Then run:

```bash
python3 bot.py
```

### Docker

```bash
docker build -t bot .
docker run --rm -it -v $(pwd):/opt bot # bash/zsh
docker run --rm -it -v (pwd):/opt bot
```

## Development / Contribution

Create a virtualenv as explained in [Installation][] above.  
Then use the following commands to install the packages in this `.venv`:

```bash
pip3 install discord.py python-dotenv
pip3 freeze >requirements.txt
```

Happy coding! :tada:  
If you're done, use `pip3 freeze` again to generate a new
`requirements.txt` and create a merge request :wink:

[server]: https://aktivista.net/2020/06/13/die-aspec-community-in-zeiten-von-corona-und-darueber-hinaus/
[invitebot]: https://top.gg/bot/480240313525600267
[api]: https://discord.com/developers/docs/intro
[issue]: https://support.discord.com/hc/de/community/posts/360030115172
[catch]: https://anidiots.guide/coding-guides/tracking-used-invites#theres-a-catch
[virtualenv]: https://docs.python.org/3/library/venv.html
[Installation]: #Installation
