# TorRecon

CLI for searching multiple engines for releated .onion sites and checks they are live and saves to a file

### Supported Engines
ahmia
torch
not_evil - dehind --evil flag due to session token which makes parsing slow


# Install

This tool requires tor to be running on port 9050

```
python3 -m venv venv && source ./venv/bin/activate
pip install -r requirements.txt
python search.py -h
```

```
usage: search.py [-h] --search SEARCH --file FILE [--threads THREADS] [--title] [--evil]

ReconTor

optional arguments:
  -h, --help         show this help message and exit
  --search SEARCH    query to search for
  --file FILE        output file name
  --threads THREADS  increase threads default 5
  --title            save title with url ':' delimited
  --evil             search on not_evil much slower
  ```
