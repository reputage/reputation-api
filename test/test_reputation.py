# ================================================== #
#                  TEST REPUTATION                   #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from click.testing import CliRunner
from reputation.cli import main

# ================================================== #
#                        MAIN                        #
# ================================================== #

def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output == '()\n'
    assert result.exit_code == 0

# ================================================== #
#                        EOF                         #
# ================================================== #