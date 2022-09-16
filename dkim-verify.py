#!/usr/bin/python3

from __future__ import print_function

import argparse
import logging
import os
import sys

import dkim

formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger("dkim-verify")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def get_txt_from_file_function(txt_file_path: str):
    # noinspection PyUnusedLocal
    def get_txt_from_file(*args, **kwargs):
        with open(txt_file_path, "rb") as txt_file:
            return txt_file.read()

    return get_txt_from_file


def get_txt_function(txt: str = None, version: str = None, key_type: str = None, public_key_data: str = None):
    txt = txt if txt else f"v={version}; k={key_type}; p={public_key_data}"

    # noinspection PyUnusedLocal
    def get_txt(*args, **kwargs):
        return txt.encode()

    return get_txt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify the DKIM signature of an email.")
    parser.add_argument("-e", "--email", type=str, required=True, help="The email to verify.")
    parser.add_argument("-v", "--verbose",
                        action='store_true',
                        help="Verbose mode. Prints debugging messages about the verification process.")

    mutually_exclusive_txt_group = parser.add_mutually_exclusive_group()
    mutually_exclusive_txt_group.add_argument("--txt-file", type=str, help="The file containing the DNS TXT record.")
    mutually_exclusive_txt_group.add_argument("--txt", type=str, help="The DNS TXT record.")
    mutually_exclusive_txt_group.add_argument("-p", "--public-key-data", type=str, help="The public key.")

    args, _ = parser.parse_known_args()

    if args.public_key_data:
        parser.add_argument("--dkim-version",
                            choices=['DKIM1'],
                            default="DKIM1",
                            type=str,
                            help="The version of the DKIM.")
        parser.add_argument("-k", "--key-type",
                            choices=['rsa'],
                            default="rsa",
                            type=str,
                            help="The key type.")

    args = parser.parse_args()

    if not os.path.exists(args.email):
        logger.error("%s not exist", args.email)
        sys.exit(1)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.txt_file and not os.path.exists(args.txt_file):
        logger.error("%s not exist", args.txt_file)
        sys.exit(1)

    if args.txt_file:
        dnsfunc = get_txt_from_file_function(args.txt_file)

    elif args.txt:
        dnsfunc = get_txt_function(txt=args.txt)

    elif args.public_key_data:
        dnsfunc = get_txt_function(version=args.dkim_version,
                                   key_type=args.key_type,
                                   public_key_data=args.public_key_data)
    else:
        dnsfunc = None

    with open(args.email, "rb") as email:
        message = email.read()
        d = dkim.DKIM(message, logger=logger)

        if not dnsfunc and d.verify():
            print("The DKIM-Signature is \033[92mVALID\033[0m")
        elif dnsfunc and d.verify(dnsfunc=dnsfunc):
            print("The DKIM-Signature is \033[92mVALID\033[0m")
        else:
            print("The DKIM-Signature verification \033[91mFAILED\033[0m")
            sys.exit(1)
