#!/usr/bin/python

from __future__ import print_function
import boto
import argparse
import re

def main():
    args = parse_args()
    if args.verbose > 1:
        print(args)

    # Get a complete list of usernames to act on
    if args.usernames is not None:
        usernames = args.usernames
    else:
        usernames = [i.strip() for i in args.username_file.readlines()]

    # Set up the connection to IAM
    conn = boto.connect_iam()

    # Take action on the usernames after asking for confirmation
    confirmation = confirm(
            "{}\nAre you sure you want to {} these users in IAM? [yes/NO]: ".format(
                '\n'.join(usernames), args.action)
            )

    if confirmation or args.no_verify:
        if args.action == "create":
                create_accounts(usernames, conn, verbosity=args.verbose)
        elif args.action == "delete":
            delete_accounts(usernames, conn, verbosity=args.verbose)
        elif args.action == "purge":
            purge_accounts(usernames, conn, verbosity=args.verbose)
        else:
            print("Unknown action '{}'".format(args.action))
            exit(1)

def create_accounts(account_names, conn, verbosity=0):
    """Create a new IAM user account

    :account_names: the list of accounts to create
    :conn: a boto IAM connection from boto.connect_iam()
    """
    for account_name in account_names:
        if verbosity > 1:
            print("Created account {}".format(account_name))
        conn.create_user(account_name)

def delete_accounts(account_names, conn, verbosity=0):
    """Delete IAM user accounts

    :account_names: the list of accounts to delete
    :conn: a boto IAM connection from boto.connect_iam()
    """
    for account_name in account_names:
        if verbosity > 1:
            print("Deleted account {}".format(account_name))
        conn.delete_user(account_name)

def purge_accounts(account_names, conn, verbosity=0):
    """Purge IAM user accounts: delete every resource owned or related to each
    IAM user in the list.

    WARNING: Not implemented yet!!! Only deletes the accounts!!!

    :account_names: the list of accounts to purge
    :conn: a boto IAM connection from boto.connect_iam()
    """
    for account_name in account_names:
        if verbosity > 1:
            print("Purged account {}".format(account_name))
        conn.delete_user(account_name)

def confirm(message, accepted_values='^[yY]+.*$'):
    """Return True if the user confirms, otherwise False

    :message: the message to ask the user,
    :accepted_values: the regex specifying a "continue" response from the user
    """
    print("Purge is not yet implemented!!!")
    return False
    #response = input(message)
    #return re.search(accepted_values, response) is not None

def parse_args():
    parser = argparse.ArgumentParser(
            description="Create and Destroy lots of IAM accounts")

    parser.add_argument('action', type=str,
            help="Action to take on the users or IDs listed. Possible actions are create, delete, and purge")
    parser.add_argument('-nv', '--no-verify', action='store_true', default=False,
            help="Don't prompt for verification before creating/deleting accounts")
    parser.add_argument('-v', '--verbose', action='count', default=0,
            help="how verbose to be when taking actions")

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-u', '--usernames', type=str, nargs='+', default=None,
            help="Usernames to take action on")
    input_group.add_argument('-f', '--username-file',
            type=argparse.FileType('r'), default=None,
            help="The file to write/read usernames to/from")

    return parser.parse_args()

if __name__ == "__main__":
    main()
