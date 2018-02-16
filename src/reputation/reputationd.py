# ================================================== #
#                    REPUTATIOND                     #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2018                                #
# Last Edited: 02/15/2018                            #
# Last Edited By: Brady Hammond                      #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

import ioflo.app.run

# ================================================== #
#                        MAIN                        #
# ================================================== #


def main():
    """
    Reputation server daemon CLI. Runs ioflo plan from
    command line shell.

        Example Usage:
        reputationd -v verbose -r -p 0.0625 -n reputation -f src/reputation/flo/main.flo -b reputation.core

    """
    from reputation import __version__
    args = ioflo.app.run.parseArgs(version=__version__)

    ioflo.app.run.run(name=args.name,
                      period=float(args.period),
                      real=args.realtime,
                      retro=args.retrograde,
                      filepath=args.filename,
                      behaviors=args.behaviors,
                      mode=args.parsemode,
                      username=args.username,
                      password=args.password,
                      verbose=args.verbose,
                      consolepath=args.console,
                      statistics=args.statistics)

if __name__ == "__main__":
    main()

# ================================================== #
#                        EOF                         #
# ================================================== #
