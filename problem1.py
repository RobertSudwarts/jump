"""
 a script to find out which symbols in fileA are not contained in
 fileB for groupA and exchanges B and C
"""


def parse_line(line):
    '''return group, exchange and codes from the given `line`
    '''
    # remove the trailing newline char
    line = line.rstrip('\n')

    a = line.find('.')  # index of the '.'
    b = line[:a].split('_')
    exchange = b[0]
    group = b[1]

    a = line.find('=')  # index of the '='

    # grab everything after the '=' and split to a list on ' '
    codes = line[a + 1:].split(' ')

    # note! .isdigit() only works here as the numbers given are integers
    #       a try...except ValueError using float/int would be req'd otherwise
    codes = [c for c in codes if not c.isdigit()]

    return group, exchange, codes


def main():
    # a list/array to which we'll add the parsed `codes`
    # if group is `groupA` AND the exchange is either `B` OR `C`
    all_codes = []

    with open('fileB.txt', 'rb') as fh:
        for line in fh:

            grp, ex, codes = parse_line(line)

            if grp == 'groupA':
                if ex == 'exchangeB' or ex == 'exchangeC':
                    all_codes.extend(codes)

    # grab list of codes from fileA
    with open('fileA.txt', 'rb') as fh:
        codes = fh.read().splitlines()

    # a simple set (difference) operation to deduct
    # codes from fileA from those (all_codes) derived from fileB
    missing_codes = set(codes) - set(all_codes)

    print (missing_codes)

if __name__ == '__main__':
    main()
