# Piaz
Simple tool for setting up Anti-GFW tools.

## Prerequisites
- Python 3.6+

## Install
Currently, pip is not supported, so you need to clone this repo to use it.
```bash
git clone https://github.com/itsamirhn/piaz.git && cd piaz
```
then install dependencies
```bash
pip install -r requirements.txt
```

## Usage
You only need to run these commands on your local machine.
```bash
python -m piaz root@1.1.1.1
```
Replace `1.1.1.1` with your server's IP address.


Run `python -m piaz --help` to see all available options.

## TODO
- [ ] Support pip
- [ ] Support for stop/edit/delete remote configs
- [ ] Error handling and logging
- [ ] Support more protocols (e.g. HTTP, SOCKS, etc.)
- [ ] Support more tools (e.g. Shadowsocks, ShadowsocksR, etc.)
- [ ] Add customizable options for pro users.
- [ ] Support bridge configuration
- [ ] Write tests & docs