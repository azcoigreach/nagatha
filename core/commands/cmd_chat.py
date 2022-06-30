from core.cli import pass_environment

import click
from .cmd_crypto import *
import pickle

@click.command('chat', short_help='Chat function')
@pass_environment
def cli(ctx):
    '''Nagatha's chat function'''
    # ctx.log(cmd_crypto.cli())
    ctx.vlog('bleep bloop, debug info')
