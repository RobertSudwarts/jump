"""
calculate the port number from the ip and compare to the port number in
fileC return any that are not equal
"""


def get_ip_port(str):
    '''
    return the ip addr and port no. parsed from the given `str`

    where `str` eg:
      "transport.groupB_3096.exchangeA_5=53413 ;239.189.17.13 7990"
    '''
    a = str.find('=')  # pos. of the '='
    b = str.find(';')  # pos. of the ';'

    # pull out the port no. and strip whitespace
    port = str[a+1:b-1]

    # and now we'll deal with the ip portion of the string
    # ie from the ';' to the end of the string, ditching
    # everything after the space, and split it into a list
    _ip = str[b+1:]
    ip = _ip[0:_ip.find(' ')].split('.')

    # at this point `ip` is a list of strings, and `port` is a string
    # (and we have a computation/comparison ahead)
    # so we'll convert these to a list of ints and an int respectively
    ip = map(int, ip)
    port = int(port)
    return ip, port


# A lambda function to do the port `computation`
# port = W.X.Y.Z => 50000 + 200(y) +z
# ie [239, 100, 33, 46] => 50000 + 200(33) + 46 = 56646
computed_port = lambda ip: 50000 + (200 * ip[2]) + ip[3]


def main():
    bad_lines = []
    # and we'll iterate and store the line number in case it's needed later...
    n = 1
    with open('fileC.txt', 'rb') as f:
        for line in f:

            ip, port = get_ip_port(line)

            if port != computed_port(ip):
                bad_lines.append([n, line])

            n += 1

    for line in bad_lines:
        print line

if __name__ == '__main__':
    main()
