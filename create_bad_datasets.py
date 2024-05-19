with open('datasets.txt', 'r') as file:
    records = [line.rstrip().split(' ') for line in file]
print(type(records))
for line in records:
    print(line)
    for i in range(len(line)):
        if '.' in line[i]:
            line[i] = '99999.0'
    print(line)
for line in records:
    print(line)
with open('datasets_bad.txt', 'w') as file:
    for line in records:
        s = ' '.join(line) + '\n'
        file.write(s)
