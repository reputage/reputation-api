# ================================================== #
#                   COMMAND LINE                     #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2018                                #
# Last Edited: 02/15/2018                            #
# Last Edited By: Brady Hammond                      #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

import click

# ================================================== #
#                        MAIN                        #
# ================================================== #

@click.command()
@click.argument('names', nargs=-1)
def main(names):
    """
    Runs the command line app. See
    http://click.pocoo.org/5/setuptools/#setuptools-integration
    for more details.
    """
    click.echo(repr(names))

# ================================================== #
#                        EOF                         #
# ================================================== #