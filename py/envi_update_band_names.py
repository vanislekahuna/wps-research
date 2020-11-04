import os
import sys
args = sys.argv
sep = os.path.sep
exists = os.path.exists
pd = sep.join(__file__.split(sep)[:-1]) + sep

print(pd)

def err(m):
    print("Error: " + m); sys.exit(1)

def run(c):
    print(c)
    a = os.system(c)
    if a != 0: err("failed to run: " + str(c))

if len(args) < 3:
    err("envi_update_band_names.py [.hdr file with band names to use] " +
        "[.hdr file with band names to overwrite]")

def get_band_names_lines(data):
    band_name_lines, in_band_names = [], False
    lines = [x.strip() for x in data.strip().split("\n")]
    for i in range(0, len(lines)):
        if len(lines[i].split("band names =")) > 1:
            in_band_names = True

        if in_band_names:
            print(lines[i])
            band_name_lines.append(lines[i])
            if len(lines[i].split("}")) > 1:
                in_band_names = False
    return band_name_lines

if not exists(args[1]) or not exists(args[2]):
    err("please check input files:\n\t" + args[1] + "\n\t" + args[2])

run('python3 ' + pd + 'envi_header_cleanup.py ' + args[1])
run('python3 ' + pd + 'envi_header_cleanup.py ' + args[2]) # should really call directly, whatever

i_dat, o_dat = open(args[1]).read(),  open(args[2]).read()


print("get band names..")

bn_1 = get_band_names_lines(i_dat)
bn_2 = get_band_names_lines(o_dat)

lines = o_dat.strip().split('\n')

for i in range(0, len(lines)):
    line = lines[i]
    if line in 






