
def read(filename):
    lines = []
    with open(filename, 'r', encoding = 'utf-8-sig') as f:
        for line in f:
            if '2021.' in line:
                continue
            else:
                lines.append(line.strip()[6:])
    return lines

def convert(lines):
    new = []
    for line in lines:
        if '陳柏翰(Howard)' in line:
            line = line[12:]
        elif 'Heather 織' in line:
            line = line[10:]
        print(line)
        new.append(line)
    return new

def write_file(filename, lines):
    with open(filename, 'w', encoding = 'utf-8') as f:
        for line in lines:
            f.write(line + '\n')

def main(filename):
    lines = read(filename)
    lines = convert(lines)
    write_file('output.txt', lines)

main('input.txt')