import ROOT
import os
import sys
from collections import OrderedDict
import numpy as np
from array import array
from copy import deepcopy
import math as mt

ROOT.gStyle.SetEndErrorSize(0)

def ConvertOptoLatex(op):

    d = {
        'cHDD': 'Q_{HD}',
        'cHbox': 'Q_{Hbox}',
        'cW': 'Q_{W}',
        'cHB': 'Q_{HB}',
        'cHW': 'Q_{HW}',
        'cHWB': 'Q_{HWB}',
        'cll1': 'Q_{ll}\'',
        'cqq1': 'Q_{qq}^{(1)}',
        'cqq11': 'Q_{qq}^{(1)}\'',
        'cHl1': 'Q_{Hl}^{(1)}',
        'cHl3': 'Q_{Hl}^{(3)}',
        'cHq1': 'Q_{Hq}^{(1)}',
        'cHq3': 'Q_{Hq}^{(3)}',
        'cHe': 'Q_{He}',
        'cHu': 'Q_{Hu}',
        'cHd': 'Q_{Hd}',
        'cqq3': 'Q_{qq}^{(3)}',
        'cqq31': 'Q_{qq}^{(3)}\'',

    }

    return d[op]

ROOT.gStyle.SetLineStyleString(11,"7 7")

def AddTgraphBox(op_dict, step_small=0.08, step_big=0.13):

    step = step_small
    y = 10

    for op in op_dict.keys():
        y -= step_big
        for process in op_dict[op].keys():
            y-= step
            os = op_dict[op][process]["1s"]
            ts = op_dict[op][process]["2s"]
            g1 = ROOT.TGraphAsymmErrors(1, array('d', [0]), array('d', [y]), array('d', [abs(os[0])]), array('d', [abs(os[1])]), array('d', [0.022]), array('d', [0.022]))
            g1.SetLineWidth(1)
            g1.SetLineStyle(1)
            g1.SetMarkerStyle(0)
            g1.SetMarkerSize(0)
            #g1.SetFillStyle(1)
            g2 = ROOT.TGraphAsymmErrors(1, array('d', [0]), array('d', [y]), array('d', [abs(ts[0])]), array('d', [abs(ts[1])]), array('d', [0.022]), array('d', [0.022]))
            g2.SetLineWidth(1)
            g2.SetLineStyle(1)
            g2.SetMarkerStyle(0)
            g2.SetMarkerSize(0)
            #g2.SetFillStyle(3002)
            op_dict[op][process]["graph_1s"] = g1
            op_dict[op][process]["graph_2s"] = g2
            op_dict[op][process]["gy"] = y

def AddTgraph(op_dict, step_small=0.08, step_big=0.13):

    step = step_small
    y = 10

    for op in op_dict.keys():
        y -= step_big
        for process in op_dict[op].keys():
            y-= step
            os = op_dict[op][process]["1s"]
            ts = op_dict[op][process]["2s"]
            g1 = ROOT.TGraphAsymmErrors(1, array('d', [0]), array('d', [y]), array('d', [abs(os[0])]), array('d', [abs(os[1])]), array('d', [0]), array('d', [0]))
            g1.SetLineWidth(1)
            g1.SetLineStyle(1)
            g1.SetMarkerStyle(20)
            g1.SetMarkerSize(0.8)
            g2 = ROOT.TGraphAsymmErrors(1, array('d', [0]), array('d', [y]), array('d', [abs(ts[0])]), array('d', [abs(ts[1])]), array('d', [0.]), array('d', [0.0]))
            g2.SetLineWidth(1)
            g2.SetLineStyle(11)
            g2.SetMarkerStyle(20)
            g2.SetMarkerSize(0.8)
            op_dict[op][process]["graph_1s"] = g1
            op_dict[op][process]["graph_2s"] = g2
            op_dict[op][process]["gy"] = y



def builOPGraph(op_dict, processes, plot_dict):

    tgl_1s = dict((i, {}) for i in processes)
    tgl_2s = dict((i, {}) for i in processes)
    for p in processes:
        tgl_1s[p]["x"] = []
        tgl_1s[p]["y"] = []
        tgl_1s[p]["exl"] = []
        tgl_1s[p]["exh"] = []
        tgl_1s[p]["eyl"] = []
        tgl_1s[p]["eyh"] = []

        tgl_2s[p]["x"] = []
        tgl_2s[p]["y"] = []
        tgl_2s[p]["exl"] = []
        tgl_2s[p]["exh"] = []
        tgl_2s[p]["eyl"] = []
        tgl_2s[p]["eyh"] = []

    step = 0.05

    y = 10
    print("OPERATORS TO PLOT: ", op_dict.keys() )
    for op in op_dict.keys():

        y -= 0.3

        for process in op_dict[op].keys():
            
            y-= step
            os = op_dict[op][process]["1s"]
            ts = op_dict[op][process]["2s"]

            tgl_1s[process]["x"].append(0)
            tgl_1s[process]["y"].append(y)

            tgl_1s[process]["exl"].append(abs(os[0]))
            tgl_1s[process]["eyl"].append(0)

            tgl_1s[process]["exh"].append(abs(os[1]))
            tgl_1s[process]["eyh"].append(0)

            tgl_2s[process]["x"].append(0)
            tgl_2s[process]["y"].append(y)

            tgl_2s[process]["exl"].append(abs(ts[0]))
            tgl_2s[process]["eyl"].append(0)

            tgl_2s[process]["exh"].append(abs(ts[1]))
            tgl_2s[process]["eyh"].append(0)

    tg_1 = []
    tg_2 = []

    for key in plot_dict.keys():

        g1 = ROOT.TGraphAsymmErrors(len(tgl_1s[key]["x"]), array('d', tgl_1s[key]["x"]), array('d', tgl_1s[key]["y"]), array('d', tgl_1s[key]["exl"]), array('d', tgl_1s[key]["exh"]),  array('d', tgl_1s[key]["eyl"]), array('d', tgl_1s[key]["eyh"]))

        g1.SetLineWidth(2)
        g1.SetLineStyle(1)
        g1.SetMarkerStyle(20)
        g1.SetMarkerSize(1)
        g1.SetFillColor(plot_dict[key]["Color"])
        g1.SetMarkerColor(plot_dict[key]["Color"])
        g1.SetLineColor(plot_dict[key]["Color"])

        g2 = ROOT.TGraphAsymmErrors(len(tgl_2s[key]["x"]), array('d', tgl_2s[key]["x"]), array('d', tgl_2s[key]["y"]), array('d', tgl_2s[key]["exl"]), array('d', tgl_2s[key]["exh"]),  array('d', tgl_2s[key]["eyl"]), array('d', tgl_2s[key]["eyh"]))
        g2.SetLineWidth(2)
        g2.SetLineStyle(2)
        g2.SetMarkerStyle(20)
        g2.SetMarkerSize(1)
        g2.SetMarkerColor(plot_dict[key]["Color"])
        g2.SetLineColor(plot_dict[key]["Color"])

        tg_1.append(g1)
        tg_2.append(g2)

    print(len(tg_2))

    return tg_1, tg_2
        

if __name__ == "__main__":
    plotting_nq = OrderedDict()
    
    plotting_nq["ZZ"] = {
        "file_" : "/eos/user/g/gboldrin/www/New/ZZ_noQuad/results.txt",
        "models" : ["EFTNeg"],
        "Color" : ROOT.kViolet-4,
        "LineColor" : ROOT.kViolet-5,
    }

    plotting_nq["WZ"] = {
        "file_" : "/eos/user/g/gboldrin/www/New/WZ_noQuad/results.txt",
        "models" : ["EFTNeg"],
        "Color" : ROOT.kPink+9,
        "LineColor" : ROOT.kPink+8
    }

    plotting_nq["SSWW"] = {
        "file_" : "/eos/user/g/gboldrin/www/New/SSWW_noQuad/results.txt",
        "models" : ["EFTNeg"],
        "Color" : ROOT.kAzure+10,
        "LineColor" : ROOT.kAzure+1,
    }

    plotting_nq["OSWW"] = {
        "file_" : "/eos/user/g/gboldrin/www/New/OSWW_noQuad/results.txt",
        "models" : ["EFTNeg"],
        "Color" : ROOT.kOrange-3,
        "LineColor" : ROOT.kOrange+8,
    }
    # plotting_nq["ZV"] = {
    #     "file_" : "/eos/user/g/gboldrin/www/New/ZV_noQuad/results.txt",
    #     "models" : ["EFTNeg"],
    #     "Color" : ROOT.kCyan+1,
    #     "LineColor" : ROOT.kCyan-5,

    # }
    plotting_nq["WW"] = {
        "file_" : "/eos/user/g/gboldrin/www/New/inWW_noQuad/results.txt",
        "models" : ["EFTNeg"],
        "Color" : ROOT.kSpring+9,
        "LineColor" : ROOT.kSpring+4,

    }
    # plotting_nq["Combined"] = {
    #     "file_" : "/eos/user/g/gboldrin/www/New/SSWW_OSWW_OSWWQCD_inWW_WZeu_WZQCD_ZV_ZZ_noQuad/results.txt",
    #     "models" : ["EFTNeg"],
    #     "Color" : ROOT.kGray+1,
    #     "LineColor" : ROOT.kGray+2,
        
    # }
    plotting_nq["Combined"] = {
        "file_" : "/eos/user/g/gboldrin/www/New/SSWW_OSWW_OSWWQCD_inWW_WZeu_WZQCD_ZZ_noQuad/results.txt",
        "models" : ["EFTNeg"],
        "Color" : ROOT.kGray+1,
        "LineColor" : ROOT.kGray+2,
        
    }

    plotting = OrderedDict()
    
    plotting["ZZ"] = {
        "file_" : "/eos/user/g/gboldrin/www/New/ZZ/results.txt",
        "models" : ["EFTNeg"],
        "Color" : ROOT.kViolet-6,
    }

    plotting["WZ"] = {
        #"file_" : "sensPlots_SSWW_noQuad/results.txt",
        "file_" : "/eos/user/g/gboldrin/www/New/WZ/results.txt",
        "models" : ["EFTNeg"],
        "Color" : ROOT.kMagenta+3,
    }

    plotting["SSWW"] = {
        #"file_" : "sensPlots_SSWW_noQuad/results.txt",
        "file_" : "/eos/user/g/gboldrin/www/New/SSWW/results.txt",
        "models" : ["EFTNeg"],
        "Color" : ROOT.kBlue,
    }

    plotting["OSWW"] = {
        #"file_" : "sensPlots_OSWW_OSWWQCD_noQuad/results.txt",
        "file_" : "/eos/user/g/gboldrin/www/New/OSWW/results.txt",
        "models" : ["EFTNeg"],
        "Color" : ROOT.kRed,
    }
    # plotting["ZV"] = {
    #     #"file_" : "sensPlots_inWW_noQuad/results.txt",
    #     "file_" : "/eos/user/g/gboldrin/www/New/ZV/results.txt",
    #     "models" : ["EFTNeg"],
    #     "Color" : ROOT.kCyan+3,
    # } 
    plotting["WW"] = {
        #"file_" : "sensPlots_inWW_noQuad/results.txt",
        "file_" : "/eos/user/g/gboldrin/www/New//inWW/results.txt",
        "models" : ["EFTNeg"],
        "Color" : ROOT.kGreen+2,
    }   
    # plotting["Combined"] = {
    #     #"file_" : "sensPlots_SSWW_OSWW_inWW_noQuad/results.txt",
    #     "file_" : "/eos/user/g/gboldrin/www/New/SSWW_OSWW_OSWWQCD_inWW_WZeu_WZQCD_ZV_ZZ/results.txt",
    #     "models" : ["EFTNeg"],
    #     "Color" : ROOT.kBlack,
    # }
    plotting["Combined"] = {
        #"file_" : "sensPlots_SSWW_OSWW_inWW_noQuad/results.txt",
        "file_" : "/eos/user/g/gboldrin/www/New/SSWW_OSWW_OSWWQCD_inWW_WZeu_WZQCD_ZZ/results.txt",
        "models" : ["EFTNeg"],
        "Color" : ROOT.kBlack,
    }

    plotting_dict = OrderedDict()

    all_ops = []

    for process in plotting.keys():
        f_ = plotting[process]["file_"]
        models = plotting[process]["models"]

        f = open(f_, 'r')
        contents = f.readlines()
        f.close()

        contents = [i.strip("\n") for i in contents]
        #contents.pop(1)

        plotting_dict[process] = OrderedDict()

        print('Process: ', process)
        for model in models:
            try:
                start = contents.index("[MODEL RESULTS] {}".format(model))
            except:
                print("[ERROR] model {} not in results ... ".format(model))
                continue

            i = start + 1
            print(contents, contents[i])
            contents.pop(i)
            print(contents, contents[i])
            ops = []
            best_v = []
            one_s = []
            two_s = []
            while "[MODEL RESULTS]" not in contents[i]:
                line = contents[i]
                print(line)
                #ops, best var, 1s, 2s
                line = line.split("\t")
                line = [j.strip(" ") for j in line]
                if len(line) > 1: #avoid empty lines at the end of file
                    ops.append(line[0])
                    best_v.append(line[1])
                    os = [float(j) for j in line[2][1:-1].split(',')]
                    one_s.append([os[0], os[1]])
                    ts = [float(j) for j in line[3][1:-1].split(',')]
                    two_s.append([ts[0] , ts[1]])
                i+=1

                if i == len(contents): break

            all_ops.append(ops)

            for i,j,k,z in zip(ops, best_v, one_s, two_s):
                plotting_dict[process][i] = OrderedDict()
                plotting_dict[process][i]["var"] = j
                plotting_dict[process][i]["1s"] = k
                plotting_dict[process][i]["2s"] = z

    result = all_ops[-1]
    for s in all_ops[:-1]:
        result = sorted(set(result).intersection(s) ,key=lambda x:result.index(x))

    gd = OrderedDict((i, OrderedDict()) for i in result)

    # NO Quadratic 
    ##################

    plotting_dict_nq = OrderedDict()

    for process in plotting_nq.keys():
        f_ = plotting_nq[process]["file_"]
        models = plotting_nq[process]["models"]

        f = open(f_, 'r')
        contents = f.readlines()
        f.close()

        contents = [i.strip("\n") for i in contents]
        #contents.pop(1)

        plotting_dict_nq[process] = OrderedDict()

        print('Process: ', process)
        for model in models:
            try:
                start = contents.index("[MODEL RESULTS] {}".format(model))
            except:
                print("[ERROR] model {} not in results ... ".format(model))
                continue

            i = start + 1
            print(contents, contents[i])
            contents.pop(i)
            print(contents, contents[i])
            ops = []
            best_v = []
            one_s = []
            two_s = []
            while "[MODEL RESULTS]" not in contents[i]:
                line = contents[i]
                print(line)
                #ops, best var, 1s, 2s
                line = line.split("\t")
                line = [j.strip(" ") for j in line]
                if len(line) > 1: #avoid empty lines at the end of file
                    ops.append(line[0])
                    best_v.append(line[1])
                    os = [float(j) for j in line[2][1:-1].split(',')]
                    one_s.append([os[0], os[1]])
                    ts = [float(j) for j in line[3][1:-1].split(',')]
                    two_s.append([ts[0] , ts[1]])
                i+=1

                if i == len(contents): break

            all_ops.append(ops)

            for i,j,k,z in zip(ops, best_v, one_s, two_s):
                plotting_dict_nq[process][i] = OrderedDict()
                plotting_dict_nq[process][i]["var"] = j
                plotting_dict_nq[process][i]["1s"] = k
                plotting_dict_nq[process][i]["2s"] = z


    gd_q = OrderedDict((i, OrderedDict()) for i in result)

    ###########################


    for process in plotting_dict.keys():
        for op in plotting_dict[process].keys():
            if op in result:
                gd[op][process] = OrderedDict()
                gd[op][process]["var"] = plotting_dict[process][op]["var"]
                gd[op][process]["1s"] = plotting_dict[process][op]["1s"]
                gd[op][process]["2s"] = plotting_dict[process][op]["2s"]  

                gd_q[op][process] = OrderedDict()
                gd_q[op][process]["var"] = plotting_dict_nq[process][op]["var"]
                gd_q[op][process]["1s"] = plotting_dict_nq[process][op]["1s"]
                gd_q[op][process]["2s"] = plotting_dict_nq[process][op]["2s"]  

    step = len(gd.keys())/2

    #AddTgraph(gd)
    #AddTgraphBox(gd_q)
    AddTgraph(gd_q)
    AddTgraphBox(gd)

    first_names = gd.keys()[:5]
    first = OrderedDict()
    for name in first_names:
        first[name] = gd[name]

    first_nq = OrderedDict()
    for name in first_names:
        first_nq[name] = gd_q[name]

    """
    second_names = gd.keys()[3:5]
    second = OrderedDict()
    for name in second_names:
        second[name] = gd[name]

    third_names = gd.keys()[5:]
    third = OrderedDict()
    for name in third_names:
        third[name] = gd[name]

    """

    second_names = gd.keys()[5:]
    second = OrderedDict()
    for name in second_names:
        second[name] = gd[name]

    second_nq = OrderedDict()
    for name in second_names:
        second_nq[name] = gd_q[name]

    pad_fraction = float(step)/len(gd.keys())

    c = ROOT.TCanvas("c", "c", 1200, 2000)
    #pad1 = ROOT.TPad("pad1", "20",0.0, 0.0,1.0, 1.0 -2*pad_fraction-0.1805)
    #pad2 = ROOT.TPad("pad2", "20",0.0, 1.0-2*pad_fraction-0.18, 1.0,  1.0 - pad_fraction-0.2705)
    #pad3 = ROOT.TPad("pad3", "20",0.0,1.0-pad_fraction-0.27,1.0, 1)
    pad2 = ROOT.TPad("pad1", "20",0.0, 0.0,1.0, 1.0-pad_fraction-0.055)
    pad3 = ROOT.TPad("pad2", "20",0.0,1.0-pad_fraction-0.05, 1.0, 1.0)

    # pad1.SetTopMargin(0)
    # pad1.SetBottomMargin(0.25)
    # pad2.SetTopMargin(0)
    # pad3.SetTopMargin(0.1)

    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.08)
    pad3.SetTopMargin(0.1)
    pad3.SetBottomMargin(0.03)

    #pad1.Draw()
    pad2.Draw()
    pad3.Draw()

    pad3.cd()

    min_x = 0
    max_x = 0
    y = []
    for op in first.keys():
        for process in first[op]:
            if first[op][process]["2s"][1] > max_x: max_x = first[op][process]["2s"][1]
            if first[op][process]["2s"][0] < min_x: min_x = first[op][process]["2s"][0] 
            if first_nq[op][process]["2s"][1] > max_x: max_x = first_nq[op][process]["2s"][1]
            if first_nq[op][process]["2s"][0] < min_x: min_x = first_nq[op][process]["2s"][0] 
            y.append(first[op][process]["gy"])
            y.append(first_nq[op][process]["gy"])

    #min_x = -max(abs(max_x), abs(min_x))
    #max_x = -min_x
    min_x = -4
    max_x = 4
    
    mx = min_x - 0.5*abs(max_x - min_x)
    mxx =  max_x + 1.6*abs(max_x - min_x)
    my = min(y) - 0.2*abs(max(y) - min(y))
    myy = max(y) + 0.4*abs(max(y) - min(y))


    
    frame = pad3.DrawFrame(mx, my , mxx, myy)

    frame.GetXaxis().SetTickLength(0)
    frame.GetXaxis().SetLabelSize(0)

    f2=ROOT.TF1("f2","TMath::Power(TMath::Abs(x), [0])",0, abs(mx))
    f2.SetParameter(0, 1./2)
    A2 = ROOT.TGaxis(0,min(y) - 0.2*abs(max(y) - min(y)), abs(mx) , min(y) - 0.2*abs(max(y) - min(y)),"f2")
    A2.SetLabelSize(0.02)
    A2.SetTitleSize(0.03)
    A2.SetTitleOffset(1.2)
    A2.Draw()

    f3=ROOT.TF1("f3","-TMath::Power(TMath::Abs(x), [0])",mx,0)
    f3.SetParameter(0, 1./2)
    A3 = ROOT.TGaxis(mx ,min(y) - 0.2*abs(max(y) - min(y)),  0  ,min(y) - 0.2*abs(max(y) - min(y)),"f3")
    A3.SetLabelSize(0.02)
    A3.SetTitleSize(0.03)
    A3.SetTitleOffset(1.2)
    A3.Draw()

    #frame.GetXaxis().SetLabelFont( 63  )
    #frame.GetXaxis().SetLabelSize(18)
    frame.GetYaxis().SetLabelSize(0)
    frame.GetYaxis().SetTickLength(0)

    line3 = ROOT.TLine(0,ROOT.gPad.GetUymin() + 0.001,0, ROOT.gPad.GetUymax() - 0.001)
    line3.SetLineColor(ROOT.kGray)
    line3.SetLineWidth(2)
    line3.Draw()

    leg = ROOT.TLegend(0.88, 0.89, 0.11, 0.76)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(.022)
    leg.SetNColumns(2)

    g_l = ROOT.TGraph()
    g_l.SetLineColor(ROOT.kBlack)
    g_l.SetLineWidth(2)
    g_l.SetMarkerColor(ROOT.kBlack)
    g_l.SetMarkerStyle(20)
    leg.AddEntry(g_l, "Linear 68% C.L.", "LP")

    g_l2 = ROOT.TGraph()
    g_l2.SetLineColor(ROOT.kBlack)
    g_l2.SetLineStyle(3)
    g_l2.SetLineWidth(2)
    g_l2.SetMarkerColor(ROOT.kBlack)
    g_l2.SetMarkerStyle(20)
    leg.AddEntry(g_l2, "Linear 95% C.L.", "LP")

    g_l3 = ROOT.TH1F("h", "h", 10, 0, 10)
    g_l3.SetLineWidth(1)
    g_l3.SetLineColor(ROOT.kBlack)
    g_l3.SetLineStyle(1)
    g_l3.SetMarkerStyle(0)
    g_l3.SetMarkerSize(0)
    g_l3.SetFillColorAlpha(0, 1)
    leg.AddEntry(g_l3, "Linear+Quadratic 68% C.L.", "F")

    g_l4 = ROOT.TH1F("h2", "h", 10, 0, 10)
    g_l4.SetLineWidth(1)
    g_l4.SetLineColor(ROOT.kBlack)
    g_l4.SetLineStyle(1)
    g_l4.SetMarkerStyle(0)
    g_l4.SetMarkerSize(0)
    g_l4.SetFillColorAlpha(ROOT.kBlack, 0.8)
    leg.AddEntry(g_l4, "Linear+Quadratic 95% C.L.", "F")


    txt1 = []
    limits1 = []
    name_proc = []

    for i,op in enumerate(first.keys()):
        ys = []

        for process in first[op]:

            name = process 

            # g2 = first[op][process]["graph_2s"]
            # g2.SetLineColor(plotting[process]["Color"])
            # g2.SetMarkerColor(plotting[process]["Color"])
            # g2.SetFillColorAlpha(plotting[process]["Color"], 0.5)
            # g1 = first[op][process]["graph_1s"]
            # g1.SetLineColor(plotting[process]["Color"])
            # g1.SetMarkerColor(plotting[process]["Color"])
            # g1.SetFillColor(plotting[process]["Color"])
            # ys.append(first[op][process]['gy'])

            # g2_f = first_nq[op][process]["graph_2s"]
            # g2_f.SetLineColor(plotting_nq[process]["LineColor"])
            # #g2_f.SetMarkerColor(plotting_nq[process]["Color"])
            # g2_f.SetFillColorAlpha(plotting_nq[process]["Color"], 0.8)
            # g1_f = first_nq[op][process]["graph_1s"]
            # g1_f.SetLineColor(plotting_nq[process]["LineColor"])
            # #g1_f.SetMarkerColor(plotting_nq[process]["Color"])
            # g1_f.SetFillColor(plotting_nq[process]["Color"])
            # g1_f.SetFillColorAlpha(0, 1)
            # ys.append(first_nq[op][process]['gy'])

            g2 = first_nq[op][process]["graph_2s"]
            g2.SetLineColor(plotting[process]["Color"])
            g2.SetMarkerColor(plotting[process]["Color"])
            g2.SetFillColorAlpha(plotting[process]["Color"], 0.5)
            g1 = first_nq[op][process]["graph_1s"]
            g1.SetLineColor(plotting[process]["Color"])
            g1.SetMarkerColor(plotting[process]["Color"])
            g1.SetFillColor(plotting[process]["Color"])
            ys.append(first_nq[op][process]['gy'])

            g2_f = first[op][process]["graph_2s"]
            g2_f.SetLineColor(plotting_nq[process]["LineColor"])
            #g2_f.SetMarkerColor(plotting_nq[process]["Color"])
            g2_f.SetFillColorAlpha(plotting_nq[process]["Color"], 0.8)
            g1_f = first[op][process]["graph_1s"]
            g1_f.SetLineColor(plotting_nq[process]["LineColor"])
            #g1_f.SetMarkerColor(plotting_nq[process]["Color"])
            g1_f.SetFillColor(plotting_nq[process]["Color"])
            g1_f.SetFillColorAlpha(0, 1)
            ys.append(first[op][process]['gy'])

            if op == "cHq1":
                name += " #times 0.1"
                per = 0.1
                g2.SetPointError(0, g2.GetErrorXlow(0)*per, g2.GetErrorXhigh(0)*per, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                g1.SetPointError(0, g1.GetErrorXlow(0)*per, g1.GetErrorXhigh(0)*per, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
                g2_f.SetPointError(0, g2_f.GetErrorXlow(0)*per, g2_f.GetErrorXhigh(0)*per, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1_f.SetPointError(0, g1_f.GetErrorXlow(0)*per, g1_f.GetErrorXhigh(0)*per, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))

            #if first[op][process]["graph_2s"].GetErrorXhigh(0) < max_x / 22 or first[op][process]["graph_2s"].GetErrorXlow(0) < min_x / 22: 
            #    name += " #times 10"
            #    g2.SetPointError(0, g2.GetErrorXlow(0)*10, g2.GetErrorXhigh(0)*10, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
            #    g1.SetPointError(0, g1.GetErrorXlow(0)*10, g1.GetErrorXhigh(0)*10, g1.GetErrorYlow(0), g1.GetErrorYhigh(0)) 
            #    g2_f.SetPointError(0, g2_f.GetErrorXlow(0)*10, g2_f.GetErrorXhigh(0)*10, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0)) 
            #    g1_f.SetPointError(0, g1_f.GetErrorXlow(0)*10, g1_f.GetErrorXhigh(0)*10, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))

            # if i == 0:
            #     leg.AddEntry(g1, "68% {}".format(process), "L")
            #     leg.AddEntry(g2, "95% {}".format(process), "L")

            # scaling
            per = mt.sqrt(abs(mx))

            if op == "cHWB" and process not in ["ZV+2j", "Combined"]:
                name += "#times 0.1"
                g2.SetPointError(0, mt.sqrt(g2.GetErrorXlow(0)*0.1)*per, mt.sqrt(g2.GetErrorXhigh(0)*0.1)*per, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                g1.SetPointError(0, mt.sqrt(g1.GetErrorXlow(0)*0.1)*per, mt.sqrt(g1.GetErrorXhigh(0)*0.1)*per, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
                g2_f.SetPointError(0, mt.sqrt(g2_f.GetErrorXlow(0)*0.1)*per, mt.sqrt(g2_f.GetErrorXhigh(0)*0.1)*per, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1_f.SetPointError(0, mt.sqrt(g1_f.GetErrorXlow(0)*0.1)*per, mt.sqrt(g1_f.GetErrorXhigh(0)*0.1)*per, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))

            else:
                g2.SetPointError(0, mt.sqrt(g2.GetErrorXlow(0))*per, mt.sqrt(g2.GetErrorXhigh(0))*per, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                g1.SetPointError(0, mt.sqrt(g1.GetErrorXlow(0))*per, mt.sqrt(g1.GetErrorXhigh(0))*per, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
                g2_f.SetPointError(0, mt.sqrt(g2_f.GetErrorXlow(0))*per, mt.sqrt(g2_f.GetErrorXhigh(0))*per, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1_f.SetPointError(0, mt.sqrt(g1_f.GetErrorXlow(0))*per, mt.sqrt(g1_f.GetErrorXhigh(0))*per, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))
                



            g2_f.Draw("2 same")
            g1_f.Draw("5 same")

            g2.Draw("P same")
            g1.Draw("PZ same")

            tex_1s = ROOT.TLatex(max_x + 0.6*max_x, first[op][process]['gy'] ,"[{:.2f}({:.2f}),{:.2f}({:.2f})]".format(first[op][process]['1s'][0], first_nq[op][process]['1s'][0], first[op][process]['1s'][1], first_nq[op][process]['1s'][1]))
            tex_1s.SetTextFont(42)
            tex_1s.SetTextSize(0.014)
            tex_1s.SetLineWidth(2)

            tex_2s = ROOT.TLatex(max_x + 1.85*max_x, first[op][process]['gy'] ,"[{:.2f}({:.2f}),{:.2f}({:.2f})]".format(first[op][process]['2s'][0], first_nq[op][process]['2s'][0], first[op][process]['2s'][1], first_nq[op][process]['2s'][1]))
            tex_2s.SetTextFont(42)
            tex_2s.SetTextSize(0.014)
            tex_2s.SetLineWidth(2)

            tex_n = ROOT.TLatex(min_x - 0.4*abs(max_x - min_x), first[op][process]['gy'] - 0.02 ,"{}".format(name))
            tex_n.SetTextFont(42)
            tex_n.SetTextSize(0.014)
            tex_n.SetLineWidth(2)
            tex_n.SetTextAlign(10)

            

            limits1.append(tex_1s)
            limits1.append(tex_2s)
            name_proc.append(tex_n)

        my = np.mean(ys)
        tex = ROOT.TLatex(max_x + 0.2*max_x, my,"{}".format(ConvertOptoLatex(op)))
        tex.SetTextFont(52)
        tex.SetTextSize(0.018)
        tex.SetLineWidth(2)
        txt1.append(tex)

    leg.Draw()

    pad3.Update()

    for t in txt1:
        t.Draw()

    for t in limits1:
        t.Draw()

    for t in name_proc:
        t.Draw()

    

    pad3.Draw()

    pad2.cd()

    min_x = 0
    max_x = 0
    y = []
    for op in second.keys():
        for process in second[op]:
            if second[op][process]["2s"][1] > max_x: max_x = second[op][process]["2s"][1]
            if second[op][process]["2s"][0] < min_x: min_x = second[op][process]["2s"][0] 
            if second_nq[op][process]["2s"][1] > max_x: max_x = second_nq[op][process]["2s"][1]
            if second_nq[op][process]["2s"][0] < min_x: min_x = second_nq[op][process]["2s"][0] 
            y.append(second[op][process]["gy"])
            y.append(second_nq[op][process]["gy"])

    #min_x = -max(abs(max_x), abs(min_x))
    #max_x = -min_x
    min_x = -60
    max_x = 60

    mx = min_x - 0.5*abs(max_x - min_x) 
    my  = min(y) - 0.2*abs(max(y) - min(y))
    mxx = max_x + 1.6*abs(max_x - min_x)
    myy = max(y) + 0.2*abs(max(y) - min(y))

    
    frame = pad2.DrawFrame(mx, my , mxx, myy)

    frame.GetXaxis().SetTickLength(0)
    frame.GetXaxis().SetLabelSize(0)

    f4=ROOT.TF1("f4","TMath::Power(TMath::Abs(x), [0])",0, abs(mx))
    f4.SetParameter(0, 1./2)
    A4 = ROOT.TGaxis(0,min(y) - 0.2*abs(max(y) - min(y)), abs(mx) , min(y) - 0.2*abs(max(y) - min(y)),"f4")
    A4.SetLabelSize(0.02)
    A4.SetTitleSize(0.03)
    A4.SetTitleOffset(1.2)
    A4. SetTickSize(0.2)
    A4.Draw()

    f5=ROOT.TF1("f5","-TMath::Power(TMath::Abs(x), [0])",mx,0)
    f5.SetParameter(0, 1./2)
    A5 = ROOT.TGaxis(mx ,min(y) - 0.2*abs(max(y) - min(y)),  0  ,min(y) - 0.2*abs(max(y) - min(y)),"f5")
    A5.SetLabelSize(0.02)
    A5.SetTitleSize(0.03)
    A5.SetTitleOffset(1.2)
    A5.SetTickLength(1)
    A5.Draw()

    #frame.GetXaxis().SetLabelFont( 63  )
    #frame.GetXaxis().SetLabelSize(18)
    frame.GetYaxis().SetLabelSize(0)
    frame.GetYaxis().SetTickLength(0)

    line2 = ROOT.TLine(0,ROOT.gPad.GetUymin() + 0.001,0, ROOT.gPad.GetUymax() - 0.001)
    line2.SetLineColor(ROOT.kGray)
    line2.SetLineWidth(2)
    line2.Draw()

    txt2 = []
    limits2 = []
    name_proc_2 = []

    for op in second.keys():
        ys = []
        for process in second[op]:
            name = process
            # g2 = second[op][process]["graph_2s"]
            # g2.SetLineColor(plotting[process]["Color"])
            # g2.SetMarkerColor(plotting[process]["Color"])
            # g1 = second[op][process]["graph_1s"]
            # g1.SetLineColor(plotting[process]["Color"])
            # g1.SetMarkerColor(plotting[process]["Color"])
            # ys.append(second[op][process]['gy'])

            # g2_f = second_nq[op][process]["graph_2s"]
            # g2_f.SetLineColor(plotting_nq[process]["LineColor"])
            # #g2_f.SetMarkerColor(plotting_nq[process]["Color"])
            # g2_f.SetFillColorAlpha(plotting_nq[process]["Color"], 0.8)
            # g1_f = second_nq[op][process]["graph_1s"]
            # g1_f.SetLineColor(plotting_nq[process]["LineColor"])
            # #g1_f.SetMarkerColor(plotting_nq[process]["Color"])
            # g1_f.SetFillColor(plotting_nq[process]["Color"])
            # g1_f.SetFillColorAlpha(0, 1)
            # ys.append(second_nq[op][process]['gy'])

            g2 = second_nq[op][process]["graph_2s"]
            g2.SetLineColor(plotting[process]["Color"])
            g2.SetMarkerColor(plotting[process]["Color"])
            g1 = second_nq[op][process]["graph_1s"]
            g1.SetLineColor(plotting[process]["Color"])
            g1.SetMarkerColor(plotting[process]["Color"])
            ys.append(second_nq[op][process]['gy'])

            g2_f = second[op][process]["graph_2s"]
            g2_f.SetLineColor(plotting_nq[process]["LineColor"])
            #g2_f.SetMarkerColor(plotting_nq[process]["Color"])
            g2_f.SetFillColorAlpha(plotting_nq[process]["Color"], 0.8)
            g1_f = second[op][process]["graph_1s"]
            g1_f.SetLineColor(plotting_nq[process]["LineColor"])
            #g1_f.SetMarkerColor(plotting_nq[process]["Color"])
            g1_f.SetFillColor(plotting_nq[process]["Color"])
            g1_f.SetFillColorAlpha(0, 1)
            ys.append(second[op][process]['gy'])

            """
            if second[op][process]["graph_2s"].GetErrorXhigh(0) < max_x / 35 or second[op][process]["graph_2s"].GetErrorXlow(0) < min_x / 20: 
                name += " #times 50"
                g2.SetPointError(0, g2.GetErrorXlow(0)*50, g2.GetErrorXhigh(0)*50, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                g1.SetPointError(0, g1.GetErrorXlow(0)*50, g1.GetErrorXhigh(0)*50, g1.GetErrorYlow(0), g1.GetErrorYhigh(0)) 
                g2_f.SetPointError(0, g2_f.GetErrorXlow(0)*50, g2_f.GetErrorXhigh(0)*50, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0)) 
                g1_f.SetPointError(0, g1_f.GetErrorXlow(0)*50, g1_f.GetErrorXhigh(0)*50, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))

            if second[op][process]["graph_2s"].GetErrorXhigh(0) < max_x / 12 or second[op][process]["graph_2s"].GetErrorXlow(0) < min_x / 12: 
                name += " #times 10"
                g2.SetPointError(0, g2.GetErrorXlow(0)*10, g2.GetErrorXhigh(0)*10, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                g1.SetPointError(0, g1.GetErrorXlow(0)*10, g1.GetErrorXhigh(0)*10, g1.GetErrorYlow(0), g1.GetErrorYhigh(0)) 
                g2_f.SetPointError(0, g2_f.GetErrorXlow(0)*10, g2_f.GetErrorXhigh(0)*10, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0)) 
                g1_f.SetPointError(0, g1_f.GetErrorXlow(0)*10, g1_f.GetErrorXhigh(0)*10, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))
            
            if op == "cHl1" and process == "SSWW":
                name += " #times 0.1"
                g2.SetPointError(0, g2.GetErrorXlow(0)*0.1, g2.GetErrorXhigh(0)*0.1, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                g1.SetPointError(0, g1.GetErrorXlow(0)*0.1, g1.GetErrorXhigh(0)*0.1, g1.GetErrorYlow(0), g1.GetErrorYhigh(0)) 
                g2_f.SetPointError(0, g2_f.GetErrorXlow(0)*0.1, g2_f.GetErrorXhigh(0)*0.1, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0)) 
                g1_f.SetPointError(0, g1_f.GetErrorXlow(0)*0.1, g1_f.GetErrorXhigh(0)*0.1, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))

            if op == "cHl1" and process == "OSWW":
                name += " #times 0.1"
                g2.SetPointError(0, g2.GetErrorXlow(0)*0.1, g2.GetErrorXhigh(0)*0.1, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                g1.SetPointError(0, g1.GetErrorXlow(0)*0.1, g1.GetErrorXhigh(0)*0.1, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
                g2_f.SetPointError(0, g2_f.GetErrorXlow(0)*0.1, g2_f.GetErrorXhigh(0)*0.1, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1_f.SetPointError(0, g1_f.GetErrorXlow(0)*0.1, g1_f.GetErrorXhigh(0)*0.1, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))
            
            if op == "cHl1" and process == "WW":
                name += " #times 0.1"
                g2.SetPointError(0, g2.GetErrorXlow(0)*0.1, g2.GetErrorXhigh(0)*0.1, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                g1.SetPointError(0, g1.GetErrorXlow(0)*0.1, g1.GetErrorXhigh(0)*0.1, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
                g2_f.SetPointError(0, g2_f.GetErrorXlow(0)*0.1, g2_f.GetErrorXhigh(0)*0.1, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1_f.SetPointError(0, g1_f.GetErrorXlow(0)*0.1, g1_f.GetErrorXhigh(0)*0.1, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))

            
            if op == "cHW" and process == "WZ":
                name += " #times 0.5"
                per = 0.5
                g2.SetPointError(0, g2.GetErrorXlow(0)*per, g2.GetErrorXhigh(0)*per, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                g1.SetPointError(0, g1.GetErrorXlow(0)*per, g1.GetErrorXhigh(0)*per, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
                g2_f.SetPointError(0, g2_f.GetErrorXlow(0)*per, g2_f.GetErrorXhigh(0)*per, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1_f.SetPointError(0, g1_f.GetErrorXlow(0)*per, g1_f.GetErrorXhigh(0)*per, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))
            if op == "cHW" and process == "ZZ":
                name += " #times 0.5"
                per = 0.5
                g2.SetPointError(0, g2.GetErrorXlow(0)*per, g2.GetErrorXhigh(0)*per, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                g1.SetPointError(0, g1.GetErrorXlow(0)*per, g1.GetErrorXhigh(0)*per, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
                g2_f.SetPointError(0, g2_f.GetErrorXlow(0)*per, g2_f.GetErrorXhigh(0)*per, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1_f.SetPointError(0, g1_f.GetErrorXlow(0)*per, g1_f.GetErrorXhigh(0)*per, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))

            if op == "cHbox" and process == "WZ":
                name += " #times 0.5"
                per = 0.5
                #g2.SetPointError(0, g2.GetErrorXlow(0)*per, g2.GetErrorXhigh(0)*per, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                #g1.SetPointError(0, g1.GetErrorXlow(0)*per, g1.GetErrorXhigh(0)*per, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
                g2_f.SetPointError(0, g2_f.GetErrorXlow(0)*per, g2_f.GetErrorXhigh(0)*per, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1_f.SetPointError(0, g1_f.GetErrorXlow(0)*per, g1_f.GetErrorXhigh(0)*per, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))
                g2.SetPointError(0, 15, 15, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1.SetPointError(0, 15, 15, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))
            if op == "cHbox" and process == "ZZ":
                name += " #times 0.5"
                per = 0.5
                #g2.SetPointError(0, g2.GetErrorXlow(0)*per, g2.GetErrorXhigh(0)*per, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                #g1.SetPointError(0, g1.GetErrorXlow(0)*per, g1.GetErrorXhigh(0)*per, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
                g2_f.SetPointError(0, g2_f.GetErrorXlow(0)*per, g2_f.GetErrorXhigh(0)*per, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1_f.SetPointError(0, g1_f.GetErrorXlow(0)*per, g1_f.GetErrorXhigh(0)*per, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))
                g2.SetPointError(0, 15, 15, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1.SetPointError(0, 15, 15, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))
            if op == "cHbox" and process == "SSWW":
                name += " #times 0.5"
                per = 0.5
                g2.SetPointError(0, g2.GetErrorXlow(0)*per, g2.GetErrorXhigh(0)*per, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                g1.SetPointError(0, g1.GetErrorXlow(0)*per, g1.GetErrorXhigh(0)*per, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
                g2_f.SetPointError(0, g2_f.GetErrorXlow(0)*per, g2_f.GetErrorXhigh(0)*per, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1_f.SetPointError(0, g1_f.GetErrorXlow(0)*per, g1_f.GetErrorXhigh(0)*per, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))

            """

            per = mt.sqrt(abs(mx))

            if op == "cHl1" and process == "WZ":
                print("IMAOOOO")
                g2_extended_wz = deepcopy(g2_f)
                x = g2_extended_wz.GetX()
                #computed offline for second minima
                #x[0] = -mt.sqrt(17.885)*per
                x[0] = -mt.sqrt(17)*per
                x2 = -mt.sqrt(18)*per
                #g2_extended_wz.SetPointError(0, mt.sqrt(0.655)*per, mt.sqrt(0.655)*per, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g2_extended_wz.SetPointError(abs(x2-x[0]), 0, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g2_extended_wz.SetMarkerSize(0)

            if op == "cHDD" and process == "OSWW":
                g2_extended = deepcopy(g2_f)
                x = g2_extended.GetX()
                #computed offline for second minima
                x[0] = mt.sqrt(16.124)*per 
                x2 = mt.sqrt(21.713)*per
                g2_extended.SetPointError(0, 0, x2-x[0], g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g2_extended.SetMarkerSize(0)

            if op == "cHl1" and process == "OSWW":
                #g2.SetPointError(0, g2.GetErrorXlow(0)*per, g2.GetErrorXhigh(0)*per, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                #g1.SetPointError(0, g1.GetErrorXlow(0)*per, g1.GetErrorXhigh(0)*per, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
                g2.SetPointError(0, 35, 35, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1.SetPointError(0, 35, 35, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))

            if op == "cHl1" and process == "SSWW":
                #g2.SetPointError(0, g2.GetErrorXlow(0)*per, g2.GetErrorXhigh(0)*per, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
                #g1.SetPointError(0, g1.GetErrorXlow(0)*per, g1.GetErrorXhigh(0)*per, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
                g2.SetPointError(0, 35, 35, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
                g1.SetPointError(0, 35, 35, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))

            
            g2.SetPointError(0, mt.sqrt(g2.GetErrorXlow(0))*per, mt.sqrt(g2.GetErrorXhigh(0))*per, g2.GetErrorYlow(0), g2.GetErrorYhigh(0))
            g1.SetPointError(0, mt.sqrt(g1.GetErrorXlow(0))*per, mt.sqrt(g1.GetErrorXhigh(0))*per, g1.GetErrorYlow(0), g1.GetErrorYhigh(0))
            g2_f.SetPointError(0, mt.sqrt(g2_f.GetErrorXlow(0))*per, mt.sqrt(g2_f.GetErrorXhigh(0))*per, g2_f.GetErrorYlow(0), g2_f.GetErrorYhigh(0))
            g1_f.SetPointError(0, mt.sqrt(g1_f.GetErrorXlow(0))*per, mt.sqrt(g1_f.GetErrorXhigh(0))*per, g1_f.GetErrorYlow(0), g1_f.GetErrorYhigh(0))

            g2_f.Draw("2 same")
            g1_f.Draw("5 same")

            g2.Draw("P same")
            g1.Draw("PZ same")

            if op == "cHDD" and process == "OSWW":
                g2_extended.Draw("2 same")


            if op == "cHl1" and process == "WZ":
                g2_extended_wz.Draw("2 same")
            
            if op == "cHbox" and process == "WZ":
               tex_1s = ROOT.TLatex(max_x + 0.6*max_x, second[op][process]['gy'] ,"[{:.2g}({}),{:.2g}({})]".format(second[op][process]['1s'][0], ">100", second[op][process]['1s'][1], ">100"))
               tex_1s.SetTextFont(42)
               tex_1s.SetTextSize(0.017)
               tex_1s.SetLineWidth(2)

               tex_2s = ROOT.TLatex(max_x + 1.85*max_x, second[op][process]['gy'] ,"[{:.2g}({}),{:.2g}({})]".format(second[op][process]['2s'][0], ">100", second[op][process]['2s'][1], ">100"))
               tex_2s.SetTextFont(42)
               tex_2s.SetTextSize(0.017)
               tex_2s.SetLineWidth(2)
            elif op == "cHbox" and process == "ZZ":
               tex_1s = ROOT.TLatex(max_x + 0.6*max_x, second[op][process]['gy'] ,"[{:.2g}({}),{:.2g}({})]".format(second[op][process]['1s'][0], ">100", second[op][process]['1s'][1], ">100"))
               tex_1s.SetTextFont(42)
               tex_1s.SetTextSize(0.017)
               tex_1s.SetLineWidth(2)

               tex_2s = ROOT.TLatex(max_x + 1.85*max_x, second[op][process]['gy'] ,"[{:.2g}({}),{:.2g}({})]".format(second[op][process]['2s'][0], ">100", second[op][process]['2s'][1], ">100"))
               tex_2s.SetTextFont(42)
               tex_2s.SetTextSize(0.017)
               tex_2s.SetLineWidth(2)
            elif op == "cHl1" and process == "SSWW":
               tex_1s = ROOT.TLatex(max_x + 0.6*max_x, second[op][process]['gy'] ,"[{:.2g}({}),{:.2g}({})]".format(second[op][process]['1s'][0], ">100", second[op][process]['1s'][1], ">100"))
               tex_1s.SetTextFont(42)
               tex_1s.SetTextSize(0.017)
               tex_1s.SetLineWidth(2)

               tex_2s = ROOT.TLatex(max_x + 1.85*max_x, second[op][process]['gy'] ,"[{:.2g}({}),{:.2g}({})]".format(second[op][process]['2s'][0], ">100", second[op][process]['2s'][1], ">100"))
               tex_2s.SetTextFont(42)
               tex_2s.SetTextSize(0.017)
               tex_2s.SetLineWidth(2)
            elif op == "cHl1" and process == "OSWW":
               tex_1s = ROOT.TLatex(max_x + 0.6*max_x, second[op][process]['gy'] ,"[{:.2g}({}),{:.2g}({})]".format(second[op][process]['1s'][0], ">100", second[op][process]['1s'][1], ">100"))
               tex_1s.SetTextFont(42)
               tex_1s.SetTextSize(0.017)
               tex_1s.SetLineWidth(2)

               tex_2s = ROOT.TLatex(max_x + 1.85*max_x, second[op][process]['gy'] ,"[{:.2g}({}),{:.2g}({})]".format(second[op][process]['2s'][0], ">100", second[op][process]['2s'][1], ">100"))
               tex_2s.SetTextFont(42)
               tex_2s.SetTextSize(0.017)
               tex_2s.SetLineWidth(2)
            elif op == "cHl1" and process == "WW":
               tex_1s = ROOT.TLatex(max_x + 0.6*max_x, second[op][process]['gy'] ,"[{:.2g}({}),{:.2g}({})]".format(second[op][process]['1s'][0], int(second_nq[op][process]['1s'][0]), second[op][process]['1s'][1], int(second_nq[op][process]['1s'][1])))
               tex_1s.SetTextFont(42)
               tex_1s.SetTextSize(0.017)
               tex_1s.SetLineWidth(2)

               tex_2s = ROOT.TLatex(max_x + 1.85*max_x, second[op][process]['gy'] ,"[{:.2g}({}),{:.2g}({})]".format(second[op][process]['2s'][0], int(second_nq[op][process]['2s'][0]), second[op][process]['2s'][1], int(second_nq[op][process]['2s'][1])))
               tex_2s.SetTextFont(42)
               tex_2s.SetTextSize(0.017)
               tex_2s.SetLineWidth(2)

            elif op == "cHl1" and process == "WZ":
               tex_1s = ROOT.TLatex(max_x + 0.6*max_x, second[op][process]['gy'] ,"[{:.2f}({:.2f}),{:.2f}({:.2f})]".format(second[op][process]['1s'][0], second_nq[op][process]['1s'][0], second[op][process]['1s'][1], second_nq[op][process]['1s'][1]))
               tex_1s.SetTextFont(42)
               tex_1s.SetTextSize(0.017)
               tex_1s.SetLineWidth(2)
            
               tex_2s = ROOT.TLatex(max_x + 1.85*max_x, second[op][process]['gy'] ,"[-18,-17],[{:.2f}({:.2f}),{:.2f}({:.2f})]".format(second[op][process]['2s'][0], second_nq[op][process]['2s'][0], second[op][process]['2s'][1], second_nq[op][process]['2s'][1]))
               tex_2s.SetTextFont(42)
               tex_2s.SetTextSize(0.017)
               tex_2s.SetLineWidth(2)

            elif op == "cHDD" and process == "OSWW":
            
               tex_1s = ROOT.TLatex(max_x + 0.6*max_x, second[op][process]['gy'] ,"[{:.2g}({:.2g}),{:.2g}({:.2g})]".format(second[op][process]['1s'][0], second_nq[op][process]['1s'][0], second[op][process]['1s'][1], second_nq[op][process]['1s'][1]))
               tex_1s.SetTextFont(42)
               tex_1s.SetTextSize(0.017)
               tex_1s.SetLineWidth(2)

               tex_2s = ROOT.TLatex(max_x + 1.85*max_x, second[op][process]['gy'] ,"[{:.2g}({:.2g}),{:.2g}({:.2g})],[16.1,22.7]".format(second[op][process]['2s'][0], second_nq[op][process]['2s'][0], second[op][process]['2s'][1], second_nq[op][process]['2s'][1]))
               tex_2s.SetTextFont(42)
               tex_2s.SetTextSize(0.017)
               tex_2s.SetLineWidth(2)

            else:
               tex_1s = ROOT.TLatex(max_x + 0.6*max_x, second[op][process]['gy'] ,"[{:.2g}({:.2g}),{:.2g}({:.2g})]".format(second[op][process]['1s'][0], second_nq[op][process]['1s'][0], second[op][process]['1s'][1], second_nq[op][process]['1s'][1]))
               tex_1s.SetTextFont(42)
               tex_1s.SetTextSize(0.017)
               tex_1s.SetLineWidth(2)

               tex_2s = ROOT.TLatex(max_x + 1.85*max_x, second[op][process]['gy'] ,"[{:.2g}({:.2g}),{:.2g}({:.2g})]".format(second[op][process]['2s'][0], second_nq[op][process]['2s'][0], second[op][process]['2s'][1], second_nq[op][process]['2s'][1]))
               tex_2s.SetTextFont(42)
               tex_2s.SetTextSize(0.017)
               tex_2s.SetLineWidth(2)

            tex_n = ROOT.TLatex(min_x - 0.4*abs(max_x - min_x), second[op][process]['gy'] - 0.02 ,"{}".format(name))
            tex_n.SetTextFont(42)
            tex_n.SetTextSize(0.017)
            tex_n.SetLineWidth(2)
            tex_n.SetTextAlign(10)

            limits2.append(tex_1s)
            limits2.append(tex_2s)
            name_proc_2.append(tex_n)

        my = np.mean(ys)
        tex = ROOT.TLatex(max_x + 0.2*max_x, my,"{}".format(ConvertOptoLatex(op)))
        tex.SetTextFont(52)
        tex.SetTextSize(0.022)
        tex.SetLineWidth(2)
        txt2.append(tex)

    pad2.Update()

    for t in txt2:
        t.Draw()

    for t in limits2:
        t.Draw()

    for t in name_proc_2:
        t.Draw()

    pad2.Draw()

    """
    pad1.cd()

    min_x = 0
    max_x = 0
    y = []
    for op in third.keys():
        for process in third[op]:
            if third[op][process]["2s"][1] > max_x: max_x = third[op][process]["2s"][1]
            if third[op][process]["2s"][0] < min_x: min_x = third[op][process]["2s"][0] 
            y.append(third[op][process]["gy"])

    min_x =  -max(abs(max_x), abs(min_x))
    max_x = -min_x

    frame = pad3.DrawFrame(min_x - 0.1*abs(max_x - min_x), min(y) - 0.2*abs(max(y) - min(y)), max_x + 0.8*abs(max_x - min_x), max(y) + 0.2*abs(max(y) - min(y)))
    frame.GetXaxis().SetLabelFont( 63  )
    frame.GetXaxis().SetLabelSize(14)
    frame.GetYaxis().SetLabelSize(0)
    frame.GetYaxis().SetTickLength(0)

    line1 = ROOT.TLine(0,ROOT.gPad.GetUymin() + 0.001,0, ROOT.gPad.GetUymax() - 0.001)
    line1.SetLineColor(ROOT.kGray)
    line1.SetLineWidth(2)
    line1.Draw()

    txt = []
    limits3 = []

    for op in third.keys():
        ys = []
        for process in third[op]:
            g2 = third[op][process]["graph_2s"]
            g2.SetLineColor(plotting[process]["Color"])
            g2.SetMarkerColor(plotting[process]["Color"])
            g1 = third[op][process]["graph_1s"]
            g1.SetLineColor(plotting[process]["Color"])
            g1.SetMarkerColor(plotting[process]["Color"])

            ys.append(third[op][process]["gy"])

            g2.Draw("PZ same")
            g1.Draw("PZ same")

            tex_1s = ROOT.TLatex(max_x + 0.6*max_x, third[op][process]['gy'] ,"[{:.2f},{:.2f}]".format(third[op][process]['1s'][0], third[op][process]['1s'][1]))
            tex_1s.SetTextFont(42)
            tex_1s.SetTextSize(0.044)
            tex_1s.SetLineWidth(2)

            tex_2s = ROOT.TLatex(max_x + 1.1*max_x, third[op][process]['gy'] ,"[{:.2f},{:.2f}]".format(third[op][process]['2s'][0], third[op][process]['2s'][1]))
            tex_2s.SetTextFont(42)
            tex_2s.SetTextSize(0.044)
            tex_2s.SetLineWidth(2)

            limits3.append(tex_1s)
            limits3.append(tex_2s)

        my = np.mean(ys)
        tex = ROOT.TLatex(max_x + 0.2*max_x, my,"{}".format(ConvertOptoLatex(op)))
        tex.SetTextFont(52)
        tex.SetTextSize(0.044)
        tex.SetLineWidth(2)
        txt.append(tex)


    pad1.Update()

    for t in txt:
        t.Draw()

    for t in limits3:
        t.Draw()

    pad1.Draw()
    """

    c.cd()

    # tex = ROOT.TLatex(0.13,.978,"Simulation")
    # tex.SetNDC()
    # tex.SetTextFont(52)
    # tex.SetTextSize(0.05)
    # tex.SetLineWidth(2)
    # tex.SetTextAlign(13)
    # tex.Draw()

    # tex2 = ROOT.TLatex  (0.25, .972, "Preliminary")
    # tex2.SetNDC()
    # tex2.SetTextSize(0.76 * 0.05)
    # tex2.SetTextFont(52)
    # tex2.SetTextColor(ROOT.kBlack)
    # tex2.SetTextAlign(13)
    # tex2.Draw()

    tex3 = ROOT.TLatex(0.87,.955,"#Lambda=1 TeV   100 fb^{-1}   (13 TeV)")
    tex3.SetNDC()
    tex3.SetTextAlign(31)
    tex3.SetTextFont(42)
    tex3.SetTextSize(0.03)
    tex3.SetLineWidth(2)
    tex3.Draw()

    tex4 = ROOT.TLatex(0.453,.01, "Parameter Estimate")
    tex4.SetNDC()
    tex4.SetTextAlign(31)
    tex4.SetTextFont(42)
    tex4.SetTextSize(0.023)
    tex4.SetLineWidth(2)
    tex4.Draw()

    #tex5 = ROOT.TLatex(0.74,.79, "1#sigma")
    tex5 = ROOT.TLatex(0.675,.84, "68% L+Q (L)")
    tex5.SetNDC()
    tex5.SetTextAlign(31)
    tex5.SetTextFont(42)
    tex5.SetTextSize(0.019)
    tex5.SetLineWidth(2)
    tex5.Draw()

    #tex6 = ROOT.TLatex(0.85,.79, "2#sigma")
    tex6 = ROOT.TLatex(0.84,.84, "95% L+Q (L)")
    tex6.SetNDC()
    tex6.SetTextAlign(31)
    tex6.SetTextFont(42)
    tex6.SetTextSize(0.019)
    tex6.SetLineWidth(2)
    tex6.Draw()


    c.Draw()
    c.Print("prova.pdf")




            

        
