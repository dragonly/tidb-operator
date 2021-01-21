#!python3
import json
import re
import sys


def remove_format(s):
    s = re.sub(r'\x1b\[.*?m', '', s)
    return s


def extract_ginkgo_specs(dryrun):
    i = 0
    # find the line "Will run x of y specs"
    while(not dryrun[i].startswith('Will run ')):
        i += 1
    # print(repr(dryrun[i]))
    specs = int(re.search('Will run (\d+) of \d+ specs', dryrun[i]).group(1))
    # print('specs', specs)

    # find start of the first spec
    while 'TiDBCluster' not in dryrun[i]:
        i += 1

    # extract specs
    ret = []
    for j in range(specs):
        name = '{} {}'.format(dryrun[i], dryrun[i+1])
        ret.append(name.replace(' ', '.').replace('[', '\[').replace(']', '\]'))
        # print(j, 1, name)
        # print(j, 2, dryrun[i+2])
        i += 5

    return ret


if __name__ == '__main__':
    stdin = list(map(lambda x: x.strip(), sys.stdin.readlines()))
    # for line in stdin:
    #     print(line)
    ginkgo_dryrun = list(map(lambda x: remove_format(x), stdin))
    # print(ginkgo_dryrun)
    spec_names = extract_ginkgo_specs(ginkgo_dryrun)
    github_action_matrix = {
        'job': spec_names
    }
    print('::set-output name=matrix::{}'.format(json.dumps(github_action_matrix).replace('"', '\\"')))
