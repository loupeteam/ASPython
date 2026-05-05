"""``aspython run-tests`` subcommand — query an on-PLC unit test server."""
import logging

from ..unittests import UnitTestServer


SUBCOMMAND = 'run-tests'
HELP = 'Run unit tests against a PLC test server.'


def add_subparser(subparsers):
    p = subparsers.add_parser(SUBCOMMAND, help=HELP, description=HELP)
    p.add_argument('host', type=str, help='IP address of the PLC running the tests')
    p.add_argument('-d', '--destination', type=str, required=True,
                   help='Destination directory for the test result XML files')
    p.add_argument('-a', '--all', action='store_true',
                   help='Run all available tests')
    p.set_defaults(func=run)
    return p


def run(args) -> int:
    logging.debug('args: %s', args)
    logging.info('Querying test server to retrieve list of available tests')

    testServer = UnitTestServer(args.host, args.destination)
    if not testServer.connected:
        logging.error('Could not connect to the test server')
        return 1

    for testSuite in testServer.testSuites:
        logging.info(f'Running test suite {testSuite["device"]}')
        testServer.runTest(testSuite['device'])
    return 0
