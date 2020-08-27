import argparse

parser = argparse.ArgumentParser(description='Downloader for HathiTrust')

parser.add_argument('--url', help='Download url')

parser.add_argument('--file', help='Add text file with books')

args = parser.parse_args()

print(args.url)
print(args.file)
