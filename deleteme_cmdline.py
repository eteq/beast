import inspect
import argparse

import deleteme_funcs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--global-setting', action='store_true',
                        help='some global thingie')

    subparsers = parser.add_subparsers(dest='subparser_name', required=True,
                                       help='sub-command help')

    # create the subparsers and populate them with the correct arguments
    funcs_to_subcommand = inspect.getmembers(deleteme_funcs, inspect.isfunction)
    for name, func in funcs_to_subcommand:
        subparser = subparsers.add_parser(name, help=func.__doc__)
        for parname, arg in inspect.signature(func).parameters.items():
            sanitized_name = parname.replace('_', '-')
            if arg.default == inspect.Signature.empty:
                subparser.add_argument(sanitized_name)
            else:
                subparser.add_argument('--' + sanitized_name,
                                       default=arg.default)

    # now actually parse the arguments
    args = parser.parse_args()

    # set the global
    deleteme_funcs.GLOBAL_SETTING = args.global_setting

    # and call the function
    for name, func in funcs_to_subcommand:
        if args.subparser_name == name:
            # make a dictionary containing the correct inputs to the function,
            # extracted from the parsed arguments
            funcargs = {}
            for parname in inspect.signature(func).parameters:
                funcargs[parname] = getattr(args, parname.replace('-', '_'))
            func(**funcargs)
            break  # drop out immediately, which skips the "else" below
    else:
        assert False, 'Invalid subparser! This should be impossible...'
