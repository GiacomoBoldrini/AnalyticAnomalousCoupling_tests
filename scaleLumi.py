#!/usr/bin/env python
from glob import glob
import os
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Command line parser for model testing')
    parser.add_argument('--b',     dest='b',     help='Base folder e.g. OSWW_1op', required = True)
    parser.add_argument('--m',     dest='m',     help='model', required = False, default = "EFTNeg")
    parser.add_argument('--s',     dest='s',     help='Luminosity scale factor as a * * to the lumiscale rateParam. Default 5.44722 for 3 ab-1 ', required = False, default = "5.47722")
    parser.add_argument('--v',     dest='v',     help='Verbosity', required = False, default = False, action="store_true")
    parser.add_argument('--r',     dest='r',     help='remove the lumi scaling', required = False, default = False, action="store_true")
    args = parser.parse_args()

    subf = glob("{}/*/".format(args.b))

    if args.v: print("@INFO: Scaling by {} datacards in {} for model/s".format(args.b, args.s, args.m))
    models = args.m.split(",")
    for f in subf:
        for model in models:
            dc = glob(f + model + "/datacards/*/*/datacard.txt")
            if len(dc) == 0: 
                print("@WARNING: No cards in folder: {}, skipping".format(f))
                continue
            if args.v: print("@INFO: Editing {} datacards  in {}".format(len(dc), f))
            for datacard in dc:
                if not args.r:
                    fobj = open(datacard, 'a')
                    fobj.write("lumiscale rateParam * * {}\n".format(args.s))
                    fobj.write("nuisance edit freeze lumiscale\n")
                    fobj.close()
                else:
                    fobj = open(datacard, 'r')
                    lines = fobj.readlines()
                    if lines[-1] == "nuisance edit freeze lumiscale\n":
                        del lines[-1]
                    if  "lumiscale rateParam * *"  in lines[-1]:
                        del lines[-1]
                    
                    fobj_new = open(datacard, "w+")
                    for line in lines:
                        fobj_new.write(line)
                    fobj_new.close()
                    



    if args.v: print("@INFO: Terminated successfully")

    

                

