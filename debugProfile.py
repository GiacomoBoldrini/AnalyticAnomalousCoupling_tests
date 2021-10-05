import os
import sys
import argparse
import numpy as np 
import itertools
from glob import glob
import stat
import math
import ROOT

def ConvertOptoLatex(op):

    d = {
        'cHDD': 'Q_{HD} [TeV^{-2}]',
        'cHbox': 'Q_{H#Box} [TeV^{-2}]',
        'cW': 'Q_{W} [TeV^{-2}]',
        'cHB': 'Q_{HB} [TeV^{-2}]',
        'cHW': 'Q_{HW} [TeV^{-2}]',
        'cHWB': 'Q_{HWB} [TeV^{-2}]',
        'cll': 'Q_{ll} [TeV^{-2}]',
        'cll1': 'Q_{ll}^{(1)} [TeV^{-2}]',
        'cqq1': 'Q_{qq}^{(1)} [TeV^{-2}]',
        'cqq11': 'Q_{qq}^{(1,1)} [TeV^{-2}]',
        'cHl1': 'Q_{Hl}^{(1)} [TeV^{-2}]',
        'cHl3': 'Q_{Hl}^{(3)} [TeV^{-2}]',
        'cHq1': 'Q_{Hq}^{(1)} [TeV^{-2}]',
        'cHq3': 'Q_{Hq}^{(3)} [TeV^{-2}]',
        'cHe': 'Q_{He} [TeV^{-2}]',
        'cHu': 'Q_{Hu} [TeV^{-2}]',
        'cHd': 'Q_{Hd} [TeV^{-2}]',
        'cqq3': 'Q_{qq}^{(3)} [TeV^{-2}]',
        'cqq31': 'Q_{qq}^{(3,1)} [TeV^{-2}]',

    }
    if op in d.keys():
        return d[op]
    else: return op

def mkdir(path):
    try:
        os.mkdir(path)
    except:
        pass 

def buildText2W(d, top, fop):

    ops  = ",".join(i for i in fop)
    ops += "," + top
    r = "text2workspace.py {} -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative  -o   model.root         --X-allow-no-signal --PO eftOperators={}".format(d, ops)
    return r

def RetrieveLL(path, op, maxNLL):

    
    f = ROOT.TFile(path)
    limit = f.Get("limit")
    
    to_draw = ROOT.TString("2*deltaNLL:{}".format("k_" + op))
    n = limit.Draw( to_draw.Data() , "deltaNLL<{} && deltaNLL>{}".format(float(maxNLL), -30), "l")
    print(path, n)

    x = np.ndarray((n), 'd', limit.GetV2())[1:] #removing first element (0,0)
    y_ = np.ndarray((n), 'd', limit.GetV1())[1:] #removing first element (0,0)

    x, ind = np.unique(x, return_index = True)
    y_ = y_[ind]
    y = np.array([i-min(y_) for i in y_])

    graphScan = ROOT.TGraph(x.size,x,y)

    graphScan.GetYaxis().SetTitle("-2 #Delta LL")
    graphScan.GetXaxis().SetTitle(ConvertOptoLatex(op))
    graphScan.GetYaxis().SetTitleSize(0.04)
    graphScan.GetXaxis().SetTitleSize(0.04)

    return graphScan


def buildCombine(top, fop, topR, fopR, points):

    ranges = ""
    for i  in fop:
        ranges += "k_{}=-{},{}:".format(i, fopR,fopR)
    ranges += "k_{}=-{},{}".format(top, topR, topR)

    o_n = "_".join(i for i in fop)

    r = "combine -M MultiDimFit model.root -n {}  --algo=grid --points {}  -m 125   -t -1 --robustFit=1 --setRobustFitTolerance=0.01 --cminDefaultMinimizerStrategy=1 --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=9999999 --cminFallbackAlgo Minuit2,Simplex,0:0.1 --stepSize=0.001 --setRobustFitStrategy=1 --robustHesse=1  --maxFailedSteps 1000 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --redefineSignalPOIs k_{}     --freezeParameters r      --setParameters r=1    --setParameterRanges {}:r=1,1  --floatOtherPOI=1  --verbose 3 > combine_logger.txt".format(o_n, points, top, ranges)
    return r

def readLoggerUnderflow(log):

    f =  open(log, "r")
    contents  =  f.readlines()
    for line  in contents:
        if "WARNING: underflow" in line:
            return 1
    
    return 0

if __name__ == "__main__":

    ROOT.gROOT.SetBatch(1)

    parser = argparse.ArgumentParser(description='Command line parser for 2D plotting scans')
    parser.add_argument('--t',     dest='t',     help='target datacard', required = True)
    parser.add_argument('--s',     dest='s',     help='shapes target folder', required = True)
    parser.add_argument('--o',     dest='o',     help='output  folder', required = True)
    parser.add_argument('--top',     dest='top',     help='target op to profile', required = True)
    parser.add_argument('--fp',     dest='fp',     help='comma separated list of floating pois', required = True)
    parser.add_argument('--p',     dest='p',     help='fit points,default 100', required = False, default = "100")
    parser.add_argument('--toprange',     dest='toprange',     help='target op range def 1 ([-1,1])', required = False, default = "1" )
    parser.add_argument('--prange',     dest='prange',     help='symmetric range for floating p def 5 ([-5,5])', required = False, default = "5")

    args = parser.parse_args()

    points = int(args.p)
    fop = args.fp.split(",")
    toprange = float(args.toprange)
    floatrange = float(args.prange)

    mkdir(args.o)

    os.chdir(args.o)

    mkdir("plots")

    outDatacard = "datacard.txt"

    os.system("cp "  +  args.t  + " " + outDatacard)
    os.system("cp -r "  +  args.s  + " .")

    combs = []
    for L in range(1, len(fop)+1):
        for subset in itertools.combinations(fop, L):
            combs += [list(subset)]

    
    print(">>>>>>>>>>>>>>>>>> STARTING DEBUGGING: {} FITS <<<<<<<<<<<<<<<<<<<<<".format(len(combs)))
    for c in combs:

        t2w = buildText2W( outDatacard, args.top, c)
        os.system(t2w)
        combine  = buildCombine(args.top, c, toprange, floatrange, points)
        print(combine)
        os.system(combine)

        # Check for warnings on underflows
        underF = readLoggerUnderflow("combine_logger.txt")

        print(">>>>>>>>>>>>>>>>>> {} <<<<<<<<<<<<<<<<<<<<<".format(underF))


        name = "_".join(i for i  in c)
        LL = RetrieveLL("higgsCombine{}.MultiDimFit.mH125.root".format(name), args.top, 5)

        c1 = ROOT.TCanvas("c_{}".format(name), "c_{}".format(name), 1000, 1000)

        margins = 0.13

        ROOT.gPad.SetRightMargin(margins)
        ROOT.gPad.SetLeftMargin(margins)
        ROOT.gPad.SetBottomMargin(margins)
        ROOT.gPad.SetTopMargin(margins)
        ROOT.gPad.SetFrameLineWidth(3)
        ROOT.gPad.SetTicks()

        min_x, max_x = LL.GetXaxis().GetXmin(), LL.GetXaxis().GetXmax() 
        #min_y, max_y = LL.GetYaxis().GetXmin(), LL.GetYaxis().GetXmax()
        min_y, max_y = LL.GetYaxis().GetXmin(), 10

        #Because otherwise they wold overlap with the frame
        LL.GetYaxis().SetRangeUser(min_y - 0.05 , max_y)

        LL.SetLineColor(ROOT.kBlack)
        LL.SetMarkerColor(ROOT.kBlack)

        if underF:
            LL.SetLineColor(ROOT.kRed)
            LL.SetMarkerColor(ROOT.kRed)

        LL.SetMarkerStyle(8)
        LL.SetMarkerSize(2)
        LL.SetLineWidth(2)
        LL.SetLineStyle(2)
        LL.GetYaxis().SetTitleOffset(1.1)
        LL.GetXaxis().SetTitleOffset(1.1)
        LL.SetTitle("")
        LL.Draw("APL")

        o_sigma = ROOT.TLine(min_x, 1, max_x, 1)
        o_sigma.SetLineStyle(2)
        o_sigma.SetLineWidth(2)
        o_sigma.SetLineColor(ROOT.kGray+2)
        t_sigma = ROOT.TLine(min_x, 3.84, max_x, 3.84)
        t_sigma.SetLineStyle(2)
        t_sigma.SetLineWidth(2)
        t_sigma.SetLineColor(ROOT.kGray+2)

        tex3 = ROOT.TLatex(0.86,.89,"Underflow: {}".format("yes" if underF else "no"))
        tex3.SetNDC()
        tex3.SetTextAlign(31)
        tex3.SetTextFont(42)
        tex3.SetTextSize(0.02)
        tex3.SetLineWidth(2)
        tex3.Draw()

        tex4 = ROOT.TLatex(0.25,.89,"Floating: {}".format(",".join(i for i in c)))
        tex4.SetNDC()
        tex4.SetTextAlign(31)
        tex4.SetTextFont(42)
        tex4.SetTextSize(0.02)
        tex4.SetLineWidth(2)
        tex4.Draw()

        o_sigma.Draw("L same")
        t_sigma.Draw("L same")

        c1.SaveAs("plots/" + name + ".png")
        c1.SaveAs("plots/" + name + ".pdf")
