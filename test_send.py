import sys
obj = sys.argv[1]
with open('data.jsonl', 'a') as f:
    f.write(obj + '\n')
