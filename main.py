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


def confirm_recon(recon) -> bool:
    inp = input(
        "Recon report\n=====\nTotal file(s) found: %i\nTotal size: %f GiB\nContinue? (Y/n): "
        % (len(recon[0]), recon[1])
    )
    if inp == "n":
        return False
    return True


def main():
    sorter = FileSorter(input_dir=args.i, output_dir=args.o)
    recon = sorter.dorecon()
    if not confirm_recon(recon):
        exit(0)
    sorter.dosort(recon)


if __name__ == "__main__":
    main()
