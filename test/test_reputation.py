# ================================================== #
#                  TEST REPUTATION                   #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2018                                #
# Last Edited: 02/18/2018                            #
# Last Edited By: Brady Hammond                      #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from click.testing import CliRunner
from reputation.cli import main

# ================================================== #
#                        MAIN                        #
# ================================================== #

def test_main():
    """
    Test reputation main.
    """
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output == '()\n'
    assert result.exit_code == 0

    print("test/test_reputation: test_main() \033[92mPASSED\033[0m")

# ================================================== #
#                        EOF                         #
# ================================================== #