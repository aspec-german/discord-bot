# discord-bot

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

### Creation of requirements.txt

Create a virtualenv as explained above.  
Then use the following commands to install the packages in this `.venv`:

```bash
pip3 install discord.py python-dotenv
pip3 freeze >requirements.txt
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
docker run -it -v $(pwd):/opt bot # bash/zsh
docker run -it -v (pwd):/opt bot
```

[virtualenv]: https://docs.python.org/3/library/venv.html
