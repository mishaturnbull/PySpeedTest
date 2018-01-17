# -*- coding: utf-8 -*-

class Network(object):

    def __init__(self, line):
        fields = line.split(', ')
        self.ssid = int(fields[0])
        self.bssid = int(fields[1])
        self.name = fields[2]
        self.mac = fields[3]
        self.sigstrength = float(fields[4])
        self.channel = int(fields[5])
        self.radio = fields[6]

    def __eq__(self, other):
        return self.mac == other.mac

    #def __hash__(self):
    #    s = ''.join([a for a in self.mac if a != ':'])
    #    return int(s, 16)

    def __repr__(self):
        return self.name + '[' + str(self.bssid) + '/' + str(self.channel) + \
               '/' + self.mac + '] '

    def interferes(self, other):
        channel_diff = min([self.channel, other.channel]) / \
                       max([self.channel, other.channel])
        return channel_diff * (self.sigstrength * 100 +
                               other.sigstrength * 100)


class NetworkInterferenceLocator(object):

    def __init__(self, filename):
        with open(filename, 'r') as data:
            lines = data.readlines()
        self.networks = []
        for line in lines:
            self.networks.append(Network(line))

        self.interferences = {}
        self.interference_levels = []
        self.average_interference_level = 0

    def recompute_average(self):
        for network in self.networks:
            for test in self.networks:
                if test == network:
                    # don't check against the same network
                    continue
                i = self.interference_levels.append(network.interferes(test))
        self.average_interference_level = sum(self.interference_levels) / \
                                          len(self.interference_levels)

    def detect_interference(self):
        self.recompute_average()
        for network in self.networks:
            for test in self.networks:
                if test == network:
                    # don't check against the same network
                    continue
                i = round(network.interferes(test), 1)
                if i >= self.average_interference_level:
                    try:
                        self.interferences[repr(network)].append([repr(test), str(i)])
                    except KeyError:
                        self.interferences[repr(network)] = [[repr(test), str(i)]]

if __name__ == '__main__':
    il = NetworkInterferenceLocator('data.txt')
    il.detect_interference()

    with open('interference_report.txt', 'w') as out:
        for network in il.interferences:
            interferes_with = il.interferences[network]
            print(network + " interferes with:")
            out.write(network + " interferes with:\n")
            for interference in interferes_with:
                print('    ' + ''.join(interference))
                out.write("    " + "".join(interference) + '\n')
