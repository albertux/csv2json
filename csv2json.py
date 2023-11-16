#!python3 

import argparse
import json
import sys
import re

def main():
    parser = argparse.ArgumentParser(description="csv2json")
    parser.add_argument('-f', '--file', required=True, help="csv file to parse")
    parser.add_argument('-o', '--output', required=True, help="json file")
    args = parser.parse_args()
    
    input  = args.file
    output = args.output
    
    obj_lst = []
 
    with open(input, 'r') as csv_file:

        line_count = 0
        rows_count = 0

        for line in csv_file:

            if line_count == 0:
                if '"' in line:
                    line2 = re.sub(r'("[^"]*")', lambda x: x.group(0).replace(',', ';'), line )
                    fields = line2.strip().split(",")
                else:
                    fields = line.strip().split(",")
                rows_count = len(fields)

            if line_count > 0:
                if '"' in line:
                    line2 = re.sub(r'("[^"]*")', lambda x: x.group(0).replace(',', ';'), line )
                    rows = line2.strip().split(",")
                else:    
                    rows = line.strip().split(",")
                if fields:
                    obj_lst.append(dict(map(lambda i,j : (i,j), fields,rows)))
                else:
                    obj_lst.append(",".join(rows))

                if rows_count != len(rows):
                   sys.exit('file {}, line {}: {}'.format(input, line_count + 1 , "The number of fields does not match")) 
                rows_count = len(rows)

            line_count +=1
        
    if line_count == 1:
        sys.exit('file {}, line {}: {}'.format(input, line_count + 1 , "there are only 1 row in this file")) 
    
    with open(output, 'w') as out_file:
        out_file.write(json.dumps(obj_lst))
    
if __name__ == "__main__":
    main()
