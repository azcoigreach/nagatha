from core.cli import pass_environment
import click
import pickle

@click.command('read_pickle', short_help='Read pickle')
@click.argument('filename', type=click.Path(resolve_path=True), required=True)
@pass_environment
def cli(ctx, filename):
    '''Show contents of a pickle.'''
    file = open(filename, 'rb')
    ctx.vlog(click.format_filename(filename))
    data = pickle.load(file)
    ctx.vlog(data)
