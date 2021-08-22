#!/usr/local/bin/python3
import argparse
from sorter import FileSorter

parser = argparse.ArgumentParser(
    description="Sorts unsorted, random files into a date ordered folder structure",
)

parser.add_argument(
    "-i", type=str, metavar="input", help="Input directory", required=True
)
parser.add_argument(
    "-o", type=str, metavar="output", help="Output location", required=True
)
args = parser.parse_args()


def main():
    sorter = FileSorter(input_dir=args.i, output_dir=args.o)
    sorter.sort()


if __name__ == "__main__":
    main()
