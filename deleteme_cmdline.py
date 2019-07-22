import argparse

import deleteme_funcs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--global-setting', action='store_true',
                        help='some global thingie')

    subparsers = parser.add_subparsers(dest='subparser_name', required=True,
                                       help='sub-command help')

    parser_myfunc = subparsers.add_parser('myfunc', help='myfunc help')
    parser_myfunc.add_argument('a')
    parser_myfunc.add_argument('--b', default=2)


    parser_myfunc2 = subparsers.add_parser('myfunc2', help='myfunc2 help')
    parser_myfunc2.add_argument('a')
    parser_myfunc2.add_argument('--c', default=3)

    args = parser.parse_args()

    # set the global
    deleteme_funcs.GLOBAL_SETTING = args.global_setting

    if args.subparser_name == 'myfunc':
        deleteme_funcs.myfunc(args.a, args.b)
    elif args.subparser_name == 'myfunc2':
        deleteme_funcs.myfunc2(args.a, args.c)
    else:
        assert False, 'Invalid subparser! This should be impossible...'
