#! /usr/bin/env python2

__author__ = 'ki113d'

import re
import urllib2
import argparse
import platform
from sys import exit
from time import sleep


class _ConsoleColourer(object):
    """Basic class to handle the coloring of console output. Only
    supports ANSI escape sequences.

    @note: Currently no windows support.
    @todo: Add Windows support
    """

    __slots__ = ['__colours']

    def __init__(self):
        """Initialises colour codes for formatting use."""
        self.__colours = {
            'w': 0,   # White
            'r': 31,  # Red
            'g': 32,  # Green
            'o': 33,  # Orange
            'b': 34,  # Blue
            'p': 35,  # Purple
            'c': 36,  # Cyan
            'G': 37,  # Grey
        }

    def print_(self, string):
        """Formats and outputs a given string.

        @type string:  string
        @param string: String to be formatted and printed.
        """
        base = '\033[{0}m'

        for char in self.__colours:
            if platform.system() is 'Windows':
                string = string.replace('%' + char, '')
            else:
                string = string.replace('%' + char,
                                        base.format(self.__colours[char]))

        print string, '\033[0m'


cc = _ConsoleColourer()


class HashChecker(object):
    """Handles checking of hashes against online database and file
    manipulation.
    """

    __slots__ = ['__in_file', '__out_file', '__delay', '__single', '__total',
                 '__servers']

    def __init__(self, cli_args):
        """Initialises all variables and starts the main application
        method.
        """
        self.__in_file = cli_args.in_file
        self.__out_file = cli_args.out_file
        self.__delay = cli_args.delay
        self.__single = cli_args.single
        self.__total = 0
        self.__servers = [
            {
                'name': 'md5.noisette.ch',
                'url': 'http://md5.noisette.ch/md5.php?hash={0}',
                'pat': '<string><\!\[CDATA\[(.*)]]',
            }
        ]
        self.start()

    def start(self):
        """Applications main method.

        Systematically goes through all given strings performs checks,
        on them and outputs any results found before writing said
        results to file.
        """
        for string in self.read_file(self.__in_file):
            if not self.__single:
                string = string.split(':')
            result = self.check_hash(string)

            if result is not None:
                if not self.__single:
                    string = ':'.join([string[0], result])
                else:
                    string = ' = '.join([string, result])

                self.write_file(self.__out_file, string)
                self.__total += 1
                cc.print_('%g[%Gi%g] %bHash found%G:            %o' + string)

            sleep(self.__delay)

        cc.print_('%g[%Gi%g] %bTotal hashes found%G:    %o' +
                  str(self.__total))
        cc.print_('%g[%Gi%g] %bAll hashes written to%G: %o' + self.__out_file)

    def check_hash(self, string):
        """Checks a given hash against an online database.

        @type  string: string
        @param string: The hash to be checked.

        @rtype:        string or None
        @return:       The hash's plaintext if successful, else None
        """
        ret = None

        if not self.__single:
            string = string[1]

        for server in self.__servers:
            contents = urllib2.urlopen(server['url'].format(string)).read()
            result = re.search(server['pat'], contents)

            if result:
                ret = result.groups()[0]
                break

        return ret

    def read_file(self, fd):
        """Reads a list of hashes from the specified input file.

        @type fd:  string
        @param fd: Fully qualified path to the file to the file to be
                   read.

        @rtype:    list
        @return:   The contents of the file in list form.
        """
        ret = list()

        try:
            with open(fd, 'r') as fd:
                ret = [line.strip() for line in fd.readlines()]
        except IOError:
            self.stop('File can not be opened for reading!')

        return ret

    def write_file(self, fd, line):
        """Writes data to a specified output file.

        @type fd:    string
        @param fd:   Fully qualified path to the file to the file to be
                     written to.
        @type line:  string
        @param line: The line to be written to the file.
        """
        try:
            with open(fd, 'a') as fd:
                fd.write(line + '\n')
        except IOError:
            self.stop('File can not be opened for writing!')

    @staticmethod
    def stop(error_string):
        """Outputs an error and exits the application.

        @type error_string:  string
        @param error_string: The error string to be printed.
        """
        cc.print_('%g[%r!%g] %oError%g: %o{0}'.format(error_string))
        cc.print_('%g[%r!%g] %oClosing!')
        exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''A simple application that checks md5 hashes against''' +
                    '''online databases.''')
    parser.add_argument('in_file', type=str,
                        help='File from which the hashes should be read.')
    parser.add_argument('out_file', type=str,
                        help='File to which the discovered hashes should be' +
                             'written.')
    parser.add_argument('-d', '--delay', type=int, default=4,
                        help='Delay in seconds, between each hash check.')
    parser.add_argument('-s', '--single', action='store_true',
                        help='With this parameter each line should consist' +
                             ' of a lone md5 hash!')

    args = parser.parse_args()
    HashChecker(args)
