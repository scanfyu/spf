from os import listdir
from os.path import join, isdir
import sys

fits = sys.argv[1]
out = sys.argv[2]

fout = open(out, 'w+')

for dir in sorted(listdir(fits)):
    dirp = join(fits,dir)
    if not isdir(dirp):
        continue
    print dir
    for model in sorted(listdir(dirp)):
        modelp = join(dirp,model)
        if not isdir(modelp):
            continue
        print "\t", model
        f = open(join(modelp, 'summary_eval.dat'))
        for line in f:
            metric, val = line.strip().split('\t')
            fout.write("%s,%s,%s,%s\n" % (dir, model, metric, val))
        f.close()
fout.close()
