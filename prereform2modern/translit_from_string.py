#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from prereform2modern.process import Processor


def main(args=sys.argv):
    if args[1] == '-t':
        text = ' '.join(args[2:])
        new_txt = Processor.process_text(
            text,
            show=True,
            delimiters=[u'', u'{', u'}'],
            check_brackets=False,
            # print_log=False
            )
    else:
        text = ' '.join(args[1:])
        new_txt = Processor.process_text(
            text,
            show=False,
            delimiters=False,
            check_brackets=False,
            # print_log=False
            )
    print(new_txt[0])

    return 0


if __name__ == '__main__':
    main()
