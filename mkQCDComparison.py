from glob import glob
from array import array
import json
import argparse
import ROOT
import os
import sys

ROOT.gStyle.SetEndErrorSize(0)

def mkdir(path):
    try:
        os.mkdir(path)
    except:
        print("failed")
        pass 

def ConvertProc(proc):

    d = {
        "SSWW": "W^{#pm}W^{#pm}+2j",
        "OSWW_OSWWQCD": "W^{#pm}W^{#mp}+2j",
        "OSWW": "W^{#pm}W^{#mp}+2j",
        "OSWWQCD": "W^{#pm}W^{#mp}+2j",
        "WZ_WZQCD": "W^{#pm}Z+2j",
        "WZ": "W^{#pm}Z+2j",
        "WZQCD": "W^{#pm}Z+2j",
        "inWW": "W^{#pm}W^{#mp}+0j",
        "WW": "W^{#pm}W^{#mp}+0j",
        "ZZ": "ZZ+2j",
        "ZZ2e2mu_ZZ2e2muQCD": "ZZ+2j",
        "ZV": "ZV+2j",
        "ZV_ZVQCD": "ZV+2j",
        "combined": "Combined (No ZV)",
    }

    if proc in d.keys(): return d[proc]
    else: return proc

def ConvertOptoLatex(op):

    d = {
        'cHDD': 'c_{HD}',
        'cHbox': 'c_{Hbox}',
        'cW': 'c_{W}',
        'cHB': 'c_{HB}',
        'cHW': 'c_{HW}',
        'cHWB': 'c_{HWB}',
        'cll1': 'c_{ll}^{(1)}',
        'cll': 'c_{ll}',
        'cqq1': 'c_{qq}^{(1)}',
        'cqq11': 'c_{qq}^{(1,1)}',
        'cHl1': 'c_{Hl}^{(1)}',
        'cHl3': 'c_{Hl}^{(3)}',
        'cHq1': 'c_{Hq}^{(1)}',
        'cHq3': 'c_{Hq}^{(3)}',
        'cHe': 'c_{He}',
        'cHu': 'c_{Hu}',
        'cHd': 'c_{Hd}',
        'cqq3': 'c_{qq}^{(3)}',
        'cqq31': 'c_{qq}^{(3,1)}',

    }

    return d[op]


def read_results(rf):
    
    res = {}
    f = open(rf, "r")
    content = f.readlines()[2:-2]
    c = [i.split("\t") for i in content] #0: op #1: var #2: 1sigma #3: 2 sigma
    for i in c:
        op = i[0].strip(" ")
        
        #1s
        os = json.loads(i[2])
        #2s
        ts = json.loads(i[3])
        res[op] = {}
        res[op]["1s"] = os
        res[op]["2s"] = ts
        
    return res

def buildBlack(x, y, eyl, eyh, level=1):
    g = ROOT.TGraphAsymmErrors(1, array('d', [x+0.002]), array('d', [y]), array('d', [0]), array('d', [0]),  array('d', [eyl]), array('d', [eyh]))
    if level == 1:
        g.SetMinimum(-10)
        g.SetMaximum(15)
        g.SetLineColor(ROOT.kBlack)
        g.SetLineWidth(3)
        g.SetLineStyle(1)
        g.GetYaxis().SetRangeUser(-10,10)
    elif level == 2:
        g.SetMinimum(-10)
        g.SetMaximum(15)
        g.SetLineColor(ROOT.kBlack)
        g.SetLineWidth(3)
        g.SetLineStyle(2)
        g.GetYaxis().SetRangeUser(-10,10)
        
    else:
        print("Incorrect Level, must be 1 for 68% or 2 for 95%")
        return None
        
    return g
        
        

def buildBraz(x, y, eyl, eyh, level = 1):
    g = ROOT.TGraphAsymmErrors(1, array('d', [x]), array('d', [y]), array('d', [0.25]), array('d', [0.25]),  array('d', [eyl]), array('d', [eyh]))
    if level == 1:
        g.SetMinimum(-10)
        g.SetMaximum(15)
        g.SetFillColor(ROOT.kGray+1)
        g.SetLineColor(ROOT.kGray+1)
        g.SetLineWidth(0)
        g.SetMarkerStyle(20)
        g.SetMarkerColor(ROOT.kBlack)
        g.SetMarkerSize(1.3)
        g.GetYaxis().SetRangeUser(-10,10)
        
    elif level == 2:
        g.SetFillColor(ROOT.kGray)
        g.SetLineWidth(0)
        g.SetMarkerStyle(20)
        g.SetMarkerColor(ROOT.kGray)
        g.SetMarkerSize(3)
        g.GetYaxis().SetRangeUser(-15,15)
        
    else:
        print("Incorrect Level, must be 1 for 68% or 2 for 95%")
        return None
        
    return g



if __name__ == "__main__":

    ROOT.gROOT.SetBatch(1)

    parser = argparse.ArgumentParser(description='Command line parser for QCD comparison plotter')
    parser.add_argument('--eq',     dest='ewk_qcd',     help='Path to EWK+QCD results.txt', required = True)
    parser.add_argument('--e',     dest='ewk',     help='Path to EWK-only results.txt', required = True)
    parser.add_argument('--p',     dest='process',     help='Process name, this will be converted', required = True)
    parser.add_argument('--outf',     dest='outf',     help='out folder name', required = False, default = "summaryQCD")
    parser.add_argument('--ops',     dest='ops',     help='Do plot for only these operators', required = False, nargs="+")
    parser.add_argument('--scale',     dest='scale',     help='1-1 list with the operators, scale limits by this amount', required = False, nargs="+")
    parser.add_argument('--ylimit',     dest='ylimit',     help='max-min symmetric y of the final plot', required = False, default = "2")
    args = parser.parse_args()

    combos = [args.process]

    mkdir(args.outf)

    print("----> EWK + QCD <-----")
    d = dict.fromkeys(combos)
    d[args.process] = read_results(args.ewk_qcd)

    print("----> EWK <-----")
    combos_2 = [args.process + "_QCD"]
    d2 = dict.fromkeys(combos_2)
    d2[args.process + "_QCD"] = read_results(args.ewk)
    
    print(d[args.process].keys())   
    ops = list(d[args.process].keys())
    
    if args.ops:
        ops = args.ops
    
    one_s = []
    two_s = []

    one_s_prof = []
    two_s_prof = []

    #for op in d["OSWW"].keys():
    for op in ops:
        #print(op)
        #ops.append(op)
        one_s.append(d[args.process][op]["1s"]) #QCD as EFT
        two_s.append(d[args.process][op]["2s"])
        one_s_prof.append(d2[args.process + "_QCD"][op]["1s"]) #QCD as Bkg
        two_s_prof.append(d2[args.process + "_QCD"][op]["2s"])
        
    final_plot_y_max = abs(float(args.ylimit))
    final_plot_y_min = -final_plot_y_max
    #ROOT.gStyle.SetLineScalePS(2)
    
    ROOT.gStyle.SetLineStyleString(11,"4 4")

    c = ROOT.TCanvas("c", "c", 1000, 800)
    #c.SetGrid()
    leg = ROOT.TLegend(0.67, 0.89, 0.89, 0.11)
    margins = 0.11
    #ROOT.gPad.SetRightMargin(0.35)
    ROOT.gPad.SetRightMargin(0.11)
    ROOT.gPad.SetLeftMargin(margins)
    ROOT.gPad.SetBottomMargin(0.1983)
    ROOT.gPad.SetTopMargin(margins)
    ROOT.gPad.SetFrameLineWidth(3)

    xs = []
    ys = []

    #scale = [.1, .1, 1, .1, 1, .1, 1, .01, 1]
    scale = [1]*len(ops)

    if args.scale:
        if not len(args.scale) == len(args.ops): sys.exit("[ERROR] Scale and ops should have the same length ...")
        scale = [float(i) for i in args.scale]

    base = 0.5
    for j in range(len(ops)):
        xs.append(j+base)
        ys.append(0)

        
    g1 = []
    g2 = []
    g11 = []
    g21 = []
    print(ops)
    for idx in range(len(ops)):
        
        y_scale = scale[idx]
        # 1 sigma brazilian
        ###################
        if isinstance(one_s[idx][0], float):
            g1.append(buildBraz(xs[idx], ys[idx], abs(one_s[idx][0])*y_scale, abs(one_s[idx][1])*y_scale))
        elif isinstance(one_s[idx][0], list):
            
            for l in one_s[idx]:
                #check if its a second minima -*- = +, +*+ = +, -*+ = -
                if l[0]*l[1] > 0:
                    y = (l[0]+l[1])/2
                    eyl = (abs(abs(l[0])-abs(l[1])))/2
                    eyh = eyl
                    g1.append(buildBraz(xs[idx], y*y_scale, abs(eyl)*y_scale, abs(eyh)*y_scale))
                else: 
                    g1.append(buildBraz(xs[idx], ys[idx], abs(l[0])*y_scale, abs(l[1])*y_scale))
                    
        # 2 sigma brazilian
        ###################
        if isinstance(two_s[idx][0], float):
            g2.append(buildBraz(xs[idx], ys[idx], abs(two_s[idx][0])*y_scale, abs(two_s[idx][1])*y_scale, level=2))
        elif isinstance(two_s[idx][0], list):
                    
            for l in two_s[idx]:
                #check if its a second minima -*- = +, +*+ = +, -*+ = -
                if l[0]*l[1] > 0:
                    y = (l[0]+l[1])/2
                    eyl = (abs(abs(l[0])-abs(l[1])))/2
                    eyh = eyl
                    g2.append(buildBraz(xs[idx], y*y_scale, abs(eyl)*y_scale, abs(eyh)*y_scale, level=2))
                else: 
                    g2.append(buildBraz(xs[idx], ys[idx], abs(l[0])*y_scale, abs(l[1])*y_scale, level=2))
        
        # 1 sigma black
        ###################
        if isinstance(one_s_prof[idx][0], float):
            g11.append(buildBlack(xs[idx], ys[idx], abs(one_s_prof[idx][0])*y_scale, abs(one_s_prof[idx][1])*y_scale))
        elif isinstance(one_s_prof[idx][0], list):
            
            for l in one_s_prof[idx]:
                #check if its a second minima -*- = +, +*+ = +, -*+ = -
                if l[0]*l[1] > 0:
                    y = (l[0]+l[1])/2
                    eyl = (abs(abs(l[0])-abs(l[1])))/2
                    eyh = eyl
                    g11.append(buildBlack(xs[idx], y*y_scale, abs(eyl)*y_scale, abs(eyh)*y_scale))
                else: 
                    g11.append(buildBlack(xs[idx], ys[idx], abs(l[0])*y_scale, abs(l[1])*y_scale))
                    
                    
                    
        # 2 sigma black
        ###################
        if isinstance(two_s_prof[idx][0], float):
            g21.append(buildBlack(xs[idx], ys[idx], abs(two_s_prof[idx][0])*y_scale, abs(two_s_prof[idx][1])*y_scale, level=2))
        elif isinstance(two_s_prof[idx][0], list):
            
            for l in two_s_prof[idx]:
                #check if its a second minima -*- = +, +*+ = +, -*+ = -
                if l[0]*l[1] > 0:
                    y = (l[0]+l[1])/2
                    eyl = (abs(abs(l[0])-abs(l[1])))/2
                    eyh = eyl
                    g21.append(buildBlack(xs[idx], y*y_scale, abs(eyl)*y_scale, abs(eyh)*y_scale, level=2))
                else: 
                    g21.append(buildBlack(xs[idx], ys[idx], abs(l[0])*y_scale, abs(l[1])*y_scale, level=2))
                    
        
    leg.AddEntry(g1[0], "#pm 68% EWK+QCD", "F")
    leg.AddEntry(g2[0], "#pm 95% EWK+QCD", "F")
    leg.AddEntry(g11[0], "#pm 68% EWK", "L")
    leg.AddEntry(g21[0], "#pm 95% EWK", "L")
    leg.AddEntry(g1[0], "SM", "P")
    leg.SetBorderSize(0)
    leg.SetTextSize(0.04)
    leg.SetTextFont(42)

    h = ROOT.TH1F("h", "h", len(xs)+2, -1, len(xs)+1)
    h.SetFillColor(0)
    h.SetCanExtend(ROOT.TH1.kAllAxes)
    h.SetStats(0)
    for idx in  range(h.GetNbinsX()):
        if idx == 0: h.GetXaxis().SetBinLabel(idx + 1, "")
        if idx < len(ops)+1 and idx > 0: 
            if scale[idx-1] != 1: h.GetXaxis().SetBinLabel(idx + 1, ConvertOptoLatex(ops[idx-1]) + "#times" + str(scale[idx-1]))
            else: h.GetXaxis().SetBinLabel(idx + 1, ConvertOptoLatex(ops[idx-1]))
        else: h.GetXaxis().SetBinLabel(idx + 1, "")
            
    h.GetYaxis().SetTitle("Best Confidence Interval [TeV^{-2}]")
    h.GetXaxis().SetLabelSize(0.07)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetLabelSize(0.05)
    #h.LabelsDeflate("X")
    #h.LabelsDeflate("Y")
    h.LabelsOption("v")

    h.GetYaxis().SetRangeUser(final_plot_y_min,final_plot_y_max)
    #g1.SetHistogram(h)


    ROOT.gStyle.SetOptStat(0)

    h.GetYaxis().SetNdivisions(504, ROOT.kTRUE)


    h.Draw("AXIS")
    #c.SetGrid()
    ROOT.gPad.RedrawAxis("g")
    for g in g2:
        g.Draw("2 same")

    for g in g1:
        g.Draw("2 same")
        
    for g in g1:
        g.Draw("P same")
        
    for g in g11:
        g.Draw("L same")

    for g in g21:
        g.Draw("L same")

    c.SetTicks()
    #leg.Draw()

    #for item in cpm.optionals:
    #    item.Draw("same")

    tex = ROOT.TLatex(0.73,0.918, "#Lambda = 1 TeV, L = 100 fb^{-1}")
    tex.SetNDC()
    tex.SetTextAlign(31)
    tex.SetTextFont(42)
    tex.SetTextSize(0.05)
    tex.SetLineWidth(2)

    tex2 = ROOT.TLatex(0.88,0.918,"(" + str(13) + " TeV)")
    tex2.SetNDC()
    tex2.SetTextAlign(31)
    tex2.SetTextFont(42)
    tex2.SetTextSize(0.05)
    tex2.SetLineWidth(2)

    tex3 = ROOT.TLatex(0.28,0.918,ConvertProc(args.process))
    tex3.SetNDC()
    tex3.SetTextAlign(31)
    tex3.SetTextFont(52)
    tex3.SetTextSize(0.06)
    tex3.SetLineWidth(2)


    tex.Draw()
    tex2.Draw()
    tex3.Draw()


    c.Draw()
    c.SaveAs(args.outf + "/QCD_Effect_{}.png".format(args.process))
    c.SaveAs(args.outf + "/QCD_Effect_{}.pdf".format(args.process))

