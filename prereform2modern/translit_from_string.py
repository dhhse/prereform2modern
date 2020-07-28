#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 18.01.2017 12:50:03 MSK

import re
import sys

from process import Processor

def main(args):
    print_log = False
    print args
    if args[1] == '-t':
        text = ' '.join(args[2:])
        show_json = True
    else:
        text = ' '.join(args[1:])
        show_json = False
    try:
        new_txt = Processor.process_text(
            text,
            [u'@', u'{', u'}'],
            [u'', u'{', u'}'],
            1,
            print_log
            )
    except:
        try:
            text = text.decode('utf-8')
            new_txt = Processor.process_text(
                text,
                [u'@', u'{', u'}'],
                [u'', u'{', u'}'],
                1,
                print_log
                )
        except:
            return 0
    if show_json:
        print new_txt[-1]
    else:
        print new_txt[0]

    return 0

if __name__ == '__main__':
    main(sys.argv)
