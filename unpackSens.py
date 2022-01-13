#!/usr/bin/env python
import os
import sys
from glob import glob
import argparse

def mkdir(p):
   try:
      os.mkdir(p)
   except:
      return 

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Activate mkDatacards automatically')
    parser.add_argument('-i',     dest='input_',     help='name input folder', 
                       required = True)

    parser.add_argument('-o',     dest='output',     help='name output folder', default = "unpacked", required = False)

    args = parser.parse_args()
     
    mkdir(args.output)
    os.system("cp /afs/cern.ch/user/g/gboldrin/public/index.php " + " " + args.output)
    img = glob(args.input_ + "/*/EFTNeg/LLscans/*.png")
    for i in img: os.system("cp  " + i + " " + args.output)


    
