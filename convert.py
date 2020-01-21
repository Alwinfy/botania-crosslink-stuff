#!/usr/bin/python3

from sys    import argv, stderr, stdout
from json   import load as load_json
from re     import sub, match, compile as re_compile

if len(argv) < 2:
    print("Usage: {} <mappings file> [<output file> [<error file]]".format(argv[0]))
    exit()


def resolve_file(index, mode, default=None):
    return open(argv[index], mode) if len(argv) > index else default

with resolve_file(1, "r") as fin:
    data = load_json(fin)
unknowns = set() # so they're buffered all after stdout
errors = []

item_pattern = re_compile(r"(?<!\))\$\(item\)([^$]+)\$\([0r]\)(?!\$)")

with open(data["file"], "r") as fin, \
        resolve_file(2, "w", stdout) as out:
    for line in fin:
        line = line[:-1] # strip newline
        if '"botania.page.' not in line:
            print(line, file=out)
            continue
        def item_cb(matcher):
            whole = matcher.group(0)
            phrase = matcher.group(1)
            if phrase in data["ignore"]: return whole
            if phrase not in data["names"]:
                unknowns.add('    "{}",'.format(phrase))
                return whole
            key = data["names"][phrase]
            if key not in data["paths"]:
                errors.append("'{}' ({}) doesn't have a corresponding entry!".format(phrase, key))
                return whole
            suffix = key[1+key.rindex('.'):]
            if match(r"\.{}\d*\"\s*:".format(suffix), line):
                return whole
            return "$(l:{})$(item){}$(0)$(/l)".format(data["paths"][key], phrase)
        print(sub(item_pattern, item_cb, line), file=out)
with resolve_file(3, "w", stderr) as err:
    if unknowns:
        print("===UNKNOWN ITEMS:===", file=err)
        for warn in sorted(unknowns):
            print(warn, file=err)
    if errors:
        print("===ERRORS:===", file=err)
        for bad in sorted(errors):
            print(bad, file=err)
