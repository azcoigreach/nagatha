from core.cli import pass_environment
import click
import requests
import pickle

@click.command('crypto', short_help='Cryptocurrency commands')
@click.option('-s','--symbol', default='BTCUSDT', help='Symbol for Crypto - eg. "BTCUSDT"')
@pass_environment
def cli(ctx, symbol):
    '''Crypto commands'''
    URL = str('https://api.binance.us/api/v3/ticker/24hr?symbol='+symbol)
    r = requests.get(url=URL)
    data = r.json()
    ctx.vlog(data)
    file = open('crypto.pickle', 'wb')
    pickle.dump(data, file)
    file.close()
    ctx.vlog('pickled')


