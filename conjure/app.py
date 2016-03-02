""" Application entrypoint
"""

from ubuntui.ev import EventLoop
from ubuntui.palette import STYLES
from conjure.controllers.welcome import WelcomeController
from conjure.ui import ConjureUI
from conjure import async
import json
import sys
import argparse
import os.path as path


class ApplicationException(Exception):
    """ Error in application
    """
    pass


class Application:
    def __init__(self, opts):
        """ init

        Arguments:
        opts: Options passed in from cli
        """
        with open(opts.build_conf) as json_f:
            config = json.load(json_f)

        with open(opts.build_metadata) as json_f:
            config['metadata_filename'] = path.abspath(opts.build_metadata)
            config['metadata'] = json.load(json_f)

        self.common = {
            'opts': opts,
            'ui': ConjureUI(),
            'config': config
        }

    def unhandled_input(self, key):
        if key in ['q', 'Q']:
            async.shutdown()
            EventLoop.exit(0)

    def _start(self, *args, **kwargs):
        """ Initially load the welcome screen
        """
        WelcomeController(self.common).render()

    def start(self):
        EventLoop.build_loop(self.common['ui'], STYLES,
                             unhandled_input=self.unhandled_input)
        EventLoop.set_alarm_in(0.05, self._start)
        EventLoop.run()


def parse_options(argv):
    parser = argparse.ArgumentParser(description="Conjure setup",
                                     prog="conjure-setup")
    parser.add_argument('-c', '--config', dest='build_conf', metavar='CONFIG',
                        help='Path to Conjure config')
    parser.add_argument('-m', '--metadata', dest='build_metadata',
                        metavar='METADATA',
                        help='Path to bundle services metadata')

    return parser.parse_args(argv)


def main():
    opts = parse_options(sys.argv[1:])

    if not opts.build_conf:
        raise ApplicationException(
            "A conjure config is required, see conjure-setup -h.")

    if not path.exists(opts.build_conf):
        raise ApplicationException("Unable to find {}".format(opts.build_conf))

    if not path.exists(opts.build_metadata):
        raise ApplicationException("Unable to find {} metadata".format(
            opts.build_metadata
        ))

    app = Application(opts)
    app.start()