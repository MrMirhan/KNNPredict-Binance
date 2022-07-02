import json
lines = open('x.txt', 'r').readlines()
lines = [x.split('::')[1] for x in lines]

a = list()
b = list()

for line in lines:
    line = str(str(line.replace("\n", "")).replace(" ", "")).replace('%', '')
    if line == '-':
        c = b.copy()
        a.append(c)
        b.clear()
        continue
    data = line.split(":")[1]
    try:
        data = float(data)
    except:
        pass
    b.append(data)
    
a = [x for x in a if x[2] != x[3]]

with open('check.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(a, indent=4))