#!/usr/bin/python3
""" Usage:

    $ xml2dict input-file.xml
"""
import sys
from pprint import pprint
import xml.etree.ElementTree as E

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    inp = sys.argv[1]
    tree = E.parse(inp)
    root = tree.getroot()
    key = inp.replace(".xml", "").replace("-", "_")
    out = {key: []}
    for field in root:
        prefix = field.get("name")
        record = {"prefix": prefix}
        for property in field:
            pname = property.get("name")
            if pname not in record:
                values = []
                for element in property:
                    evalue = element.get("value")
                    values.append(evalue)
                if values:
                    record[pname] = values
                else:
                    record[pname]=property.text
        out[key].append(record)
    pprint(out)
