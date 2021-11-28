'''20211128 plot spectra, labelled by class
input: csv
  * spectra fields are identified by ending in nm
input: field label of class..
...spectra with the same label are given the same color and same key in legend'''
import os
import sys
import csv
import matplotlib
import matplotlib.pyplot as plt
args = sys.argv

'''this should go in the misc.py'''
mcolors = matplotlib.colors
colors = list(mcolors.BASE_COLORS.keys()) + list(mcolors.TABLEAU_COLORS.keys())
colors = colors[0:7] + colors[8:]
markers = [".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s",
           "p", "P", "*", "h", "H", "+", "x", "X", "D", "d", "|", "_", 0, 1,
           2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

'''this should go in the misc.py'''
def read_csv(f):
    data, i = [], 0
    reader = csv.reader(open(f),
                        delimiter=',',
                        quotechar='"')
    for row in reader:
        row = [x.strip() for x in row]
        if i == 0:
            N = len(row)
            I = range(N)
            fields, data = row, [[] for j in I]
        else:
            for j in I:
                data[j].append(row[j])
        i += 1
        if i % 1000 == 0:
            print(i)
    fields = [x.strip().replace(' ', '_') for x in fields] # spaces are always bad!
    return fields, data

'''read the csv and locate the spectra'''
fields, data = read_csv(args[1])
nf = len(fields)  # number of fields
f_i = {fields[i]:i for i in range(nf)}
if args[2] not in fields:
    print("Error: field not found:", fi)
    print(fields)
fi = f_i[args[2]]  # col index of selected field for legending

spec_fi = []
for i in range(nf):
    if fields[i][-2:] == 'nm':
        spec_fi += [i]
print('spectra col-ix', spec_fi)
print('number of cols', len(spec_fi))

'''before we plot, code the categorical possibilities from 0 to however many there are'''
N = len(data[0]) # number of data points
print("number of data points", N)
lookup, next_i = {}, 0
for i in range(N):
    value = data[fi][i]
    if value not in lookup:
        lookup[value] = next_i
        next_i += 1
values = lookup.keys()
reverse_lookup = {lookup[x]: x for x in values}
print("lookup", lookup)   # take categorical value and encode it as int 0,1,..
print("revers", reverse_lookup)  # recover original value from int code!
plt.figure(figsize=(8*1.5,6*1.5))
plt.title("Spectra aggregated by categorical field: " + args[2])
plt.ylabel("Digital number")
plt.xlabel("Date, resolution(m) and Frequency (nm)")

x = range(N)
for i in range(N):
    value = data[fi][i] # categorical value
    spectrum = [data[i][j] for j in spec_fi]
    plt.plot(x, spectrum,
             marker=markers[lookup[value]],
             color=colors[lookup[value]],
             label=value)
    # don't forget to put the spectra field labels on the bottom as ticks!
plt.legend() # loc='lower left') # upper right')
plt.tight_layout()
plt.show()

