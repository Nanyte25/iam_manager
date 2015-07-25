#!/usr/bin/python

from __future__ import print_function
import boto
import argparse

def main():
    #args = parse_args()
    boto.set_stream_logger('boto')
    conn = boto.connect_iam('us-east-1')
    print(conn.get_account_summary())
    #conn.create_user("mckeimic_test_1")

def parse_args():
    parser = argparse.ArgumentParser(description="Create and Destroy lots of IAM accounts")
    parser.add_argument('-a', '--action', type=str, default=None,
            help="Action to take on the users or IDs listed. Possible actions are create, delete, and purge")
    #parser.add_argument('--creds-file', type=str, nargs=1, default="~/.aws/credentials",
            #help="Path to the AWS credentials file to use)

    return parser.parse_args()

if __name__ == "__main__":
    main()
