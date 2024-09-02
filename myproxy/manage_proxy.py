#!/usr/bin/env python

import sys
import argparse
import os
import django

def main():
   
    parser = argparse.ArgumentParser(description='Start the caching proxy server.')
    parser.add_argument('--port', type=int, required=True, help='Port to run the caching proxy server on.')
    parser.add_argument('--origin', type=str, required=True, help='URL of the origin server to forward requests to.')
    args = parser.parse_args()

    
    os.environ['DJANGO_ORIGIN'] = args.origin

   
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproxy.settings')
    django.setup()

 
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], 'runserver', f'127.0.0.1:{args.port}'])

if __name__ == "__main__":
    main()
