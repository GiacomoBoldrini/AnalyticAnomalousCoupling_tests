import os
import sys
import argparse
import numpy as np 
import itertools
from glob import glob
import stat
import ROOT
from copy import deepcopy
from array import array
import math
from collections import OrderedDict
from operator import itemgetter

def ConvertOptoLatex(op):

    d = {
        'cHDD': 'Q_{HD}',
        'cHbox': 'Q_{Hbox}',
        'cW': 'Q_{W}',
        'cHB': 'Q_{HB}',
        'cHW': 'Q_{HW}',
        'cHWB': 'Q_{HWB}',
        'cll': 'Q_{ll}',
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
        "ZV": "ZV+2j",
        "ZZ2e2mu_ZZ2e2muQCD": "ZZ+2j",
        "combined": "Combined",
        "combined_noq": "Combined O(#Lambda^{-2})"
    }

    if proc in d.keys(): return d[proc]
    else: return proc

def RetrieveCont(operators, op, proc, maxNLL):

    file = operators[op][proc]['path']
    op_ = [operators[op][proc]['op'],op]

    f = ROOT.TFile(file)
    t = f.Get("limit")

    for i, event in enumerate(t):
        if i == 0:
            x_min = getattr(event, "k_" + op_[0])
            y_min = getattr(event, "k_" + op_[1])

        else: break

    exp = ROOT.TGraph()
    exp.SetPoint(0, x_min, y_min)
    exp.SetMarkerSize(3)
    exp.SetMarkerStyle(34)
    exp.SetMarkerColor(ROOT.kGray +2)

    to_draw = ROOT.TString("{}:{}:2*deltaNLL".format("k_" + op_[0], "k_" + op_[1]))
    n = t.Draw( to_draw.Data() , "deltaNLL<{} && deltaNLL>{}".format(float(maxNLL),-30), "l")

    x = np.ndarray((n), 'd', t.GetV1())
    y = np.ndarray((n), 'd', t.GetV2())
    z_ = np.ndarray((n), 'd', t.GetV3())

    z = np.array([i-min(z_) for i in z_]) #shifting likelihood toward 0

    graphScan1 = ROOT.TGraph2D(n,x,y,z)
    graphScan1.SetNpx(100)
    graphScan1.SetNpy(100)

    graphScan1.GetZaxis().SetRangeUser(0, float(maxNLL))
    graphScan1.GetHistogram().GetZaxis().SetRangeUser(0, float(maxNLL))

    for i in range(graphScan1.GetHistogram().GetSize()):
        if (graphScan1.GetHistogram().GetBinContent(i+1) == 0):
            graphScan1.GetHistogram().SetBinContent(i+1, 100)

    hist1 = graphScan1.GetHistogram().Clone("arb_hist")
    hist1.SetContour(2, np.array([2.30, 5.99]))
    hist1.Draw("CONT Z LIST")
    ROOT.gPad.Update()

    conts1 = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
    cont_graphs1 = [deepcopy(conts1.At(i).First()) for i in range(2)]

    gs = deepcopy(graphScan1)

    f.Close()

    return cont_graphs1


def Retrieve2DLikelihood(operators, op, maxNLL):

    canvas_d = []

    for proc in operators[op].keys():

        cont_graphs1 = RetrieveCont(operators, op, proc, maxNLL)

        x_min = cont_graphs1[0].GetXaxis().GetXmin()
        x_max = cont_graphs1[0].GetXaxis().GetXmax()
        delta = max(abs(x_min),abs(x_max))

        #JUST FOR THE MOMENT NO SCALES ON X
        delta = -100

        if delta > 1:
            if 1 < delta < 2:
                xscale = 0.5
            elif 2 < delta < 10:
                xscale = 0.1
            elif 10 < delta < 80:
                xscale = 0.01
            elif delta > 80 :
                xscale = 0.001
        else:
            xscale = 1

        file = operators[op][proc]['path']
        op_ = [operators[op][proc]['op'],op]

        f = ROOT.TFile(file)
        t = f.Get("limit")

        for i, event in enumerate(t):
            if i == 0:
                x_min = getattr(event, "k_" + op_[0])
                y_min = getattr(event, "k_" + op_[1])

            else: break

        exp = ROOT.TGraph()
        exp.SetPoint(0, x_min, y_min)
        exp.SetMarkerSize(3)
        exp.SetMarkerStyle(34)
        exp.SetMarkerColor(ROOT.kGray +2)

        to_draw = ROOT.TString("{}:{}:2*deltaNLL".format("k_" + op_[0], "k_" + op_[1]))
        n = t.Draw( to_draw.Data() , "deltaNLL<{} && deltaNLL>{}".format(float(maxNLL),-30), "l")

        x = np.ndarray((n), 'd', t.GetV1())
        y = np.ndarray((n), 'd', t.GetV2())
        z_ = np.ndarray((n), 'd', t.GetV3())
 
        z = np.array([i-min(z_) for i in z_]) #shifting likelihood toward 0
        x = np.array([i*xscale for i in x])
        graphScan = ROOT.TGraph2D(n,x,y,z)

        graphScan.SetNpx(100)
        graphScan.SetNpy(100)

        graphScan.GetZaxis().SetRangeUser(0, float(maxNLL))
        graphScan.GetHistogram().GetZaxis().SetRangeUser(0, float(maxNLL))

        for i in range(graphScan.GetHistogram().GetSize()):
            if (graphScan.GetHistogram().GetBinContent(i+1) == 0):
                graphScan.GetHistogram().SetBinContent(i+1, 100)

        hist = graphScan.GetHistogram().Clone("arb_hist")
        hist.SetContour(2, np.array([2.30, 5.99]))
        hist.Draw("CONT Z LIST")
        ROOT.gPad.Update()

        conts = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
        cont_graphs = [deepcopy(list(conts.At(i))) for i in range(2)]

        gs = deepcopy(graphScan)

        f.Close()

        y_min = 0
        y_max = 0

        for i in range(len(cont_graphs[0])):
            if cont_graphs[0][i].GetYaxis().GetXmin() < y_min: y_min = cont_graphs[0][i].GetYaxis().GetXmin()
            if cont_graphs[0][i].GetYaxis().GetXmax() > y_max: y_max = cont_graphs[0][i].GetYaxis().GetXmax()

        #y_min = abs(cont_graphs[0].GetYaxis().GetXmin())
        #y_max = abs(cont_graphs[0].GetYaxis().GetXmax())
        extreme = max(abs(y_min), abs(y_max))

        print(operators[op][proc]['op'],op)
        color = operators[op][proc]['linecolor']
        lines = operators[op][proc]['linesize']
        ls = operators[op][proc]['linestyle']
        print("color: ", color)
        for i in range(len(cont_graphs[0])):
            cont_graphs[0][i].SetLineWidth(5)
            cont_graphs[0][i].SetLineColor(color)
            cont_graphs[0][i].SetLineStyle(ls)

        canvas_d.append({
            '1sg' : cont_graphs[0],
            'min' : exp,
            'names' : operators[op][proc]['name'],
            'base_op' : op,
            'n_op' : operators[op][proc]['op'],
            'scale' : xscale,
            'extr' : extreme,
        })

    canvas_d = sorted(canvas_d, key=itemgetter('extr'))

    canvas_ord = {
        '1sg' : [],
        'min' : [],
        'names' : [],
        'base_op' : op,
        'n_op' : [],
        'scale' : [],
        'extr' : [],
    }

    for i in range(len(canvas_d)):
        for key in canvas_ord.keys():
            if key is not 'base_op':
                canvas_ord[key].append(canvas_d[i][key])

    return canvas_ord


def Retrieve2DLikelihoodCombined(file, op, maxNLL, xscale, yscale):

    f = ROOT.TFile(file)
    t = f.Get("limit")

    for i, event in enumerate(t):
        if i == 0:
            x_min = getattr(event, "k_" + op[0])
            y_min = getattr(event, "k_" + op[1])

        else: break

    exp = ROOT.TGraph()
    exp.SetPoint(0, x_min, y_min)
    exp.SetMarkerSize(3)
    exp.SetMarkerStyle(34)
    exp.SetMarkerColor(ROOT.kGray +2)

    to_draw = ROOT.TString("{}:{}:2*deltaNLL".format("k_" + op[0], "k_" + op[1]))
    n = t.Draw( to_draw.Data() , "deltaNLL<{} && deltaNLL>{}".format(float(maxNLL),-30), "l")

    x = np.ndarray((n), 'd', t.GetV1())
    y = np.ndarray((n), 'd', t.GetV2())
    z_ = np.ndarray((n), 'd', t.GetV3())

    z = np.array([i-min(z_) for i in z_]) #shifting likelihood toward 0
    x = np.array([i*xscale for i in x])
    y = np.array([i*yscale for i in y])

    graphScan = ROOT.TGraph2D(n,x,y,z)

    graphScan.SetNpx(100)
    graphScan.SetNpy(100)

    graphScan.GetZaxis().SetRangeUser(0, float(maxNLL))
    graphScan.GetHistogram().GetZaxis().SetRangeUser(0, float(maxNLL))

    for i in range(graphScan.GetHistogram().GetSize()):
        if (graphScan.GetHistogram().GetBinContent(i+1) == 0):
            graphScan.GetHistogram().SetBinContent(i+1, 100)

    hist = graphScan.GetHistogram().Clone("arb_hist")
    hist.SetContour(2, np.array([2.30, 5.99]))
    hist.Draw("CONT Z LIST")
    ROOT.gPad.Update()

    conts = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
    cont_graphs = [deepcopy(list(conts.At(i))) for i in range(2)]

    gs = deepcopy(graphScan)

    f.Close()

    return gs, cont_graphs, exp


def mkdir(path):
    try:
        os.mkdir(path)
    except:
        pass 

if __name__ == "__main__":

    ROOT.gROOT.SetBatch(1)

    parser = argparse.ArgumentParser(description='Command line parser for 2D plotting scans')
    parser.add_argument('--cfg',     dest='cfg',     help='the config file', required = True)
    parser.add_argument('--maxNLL',     dest='maxNLL',     help='Max likelihood', required = False, default = "20")
    parser.add_argument('--outf',     dest='outf',     help='out folder name', required = False, default = "summary2D")
    parser.add_argument('--lumi',     dest='lumi',     help='lumi to plot', required = False, default = "100")
    parser.add_argument('--splitLeg',     dest='splitLeg',     help='Do not plot legend on canvas but in a sepaerate plot', action="store_true", default = False)

    args = parser.parse_args()

    is_combo = False
    operators = OrderedDict()
    plt_options = {}

    ROOT.gStyle.SetPalette(ROOT.kDarkRainBow)


    execfile(args.cfg)

    mkdir(args.outf)

    ROOT.gStyle.SetLineStyleString(11,"20 20 50")
    ROOT.gStyle.SetLineStyleString(12,"30 10 60")
    ROOT.gStyle.SetLineStyleString(13,"10 5 20")
    ROOT.gStyle.SetLineStyleString(14,"30 80")
    ROOT.gStyle.SetLineStyleString(15,"10 30")

    if not is_combo:

        op_colors = {}
        for op in  operators.keys():
            for op2 in operators[op].keys():
                op_colors[op2] = {}
                op_colors[op2]['color'] = operators[op][op2]['linecolor']
                op_colors[op2]['ls'] = operators[op][op2]['linestyle']

        print(op_colors)

        for op in operators.keys():

            canvas_d = Retrieve2DLikelihood (operators, op, args.maxNLL)

            mkdir(args.outf + "/" + op)

            #create as many canvas as necessary each containing up to 7 contours
            n_ = math.ceil(float(len(canvas_d['1sg']))/7)
            step = 7

            for idx in range(0,int(n_)):

                c = ROOT.TCanvas("c_{}_{}".format(op, idx), "c_{}_{}".format(op, idx), 1000, 1000)

                margins = 0.13

                ROOT.gPad.SetRightMargin(margins)
                ROOT.gPad.SetLeftMargin(margins)
                ROOT.gPad.SetBottomMargin(margins)
                ROOT.gPad.SetTopMargin(margins)
                ROOT.gPad.SetFrameLineWidth(3)
                ROOT.gPad.SetTicks()

                leg = ROOT.TLegend(0.15, 0.8, 0.85, 0.85)
                leg.SetBorderSize(0)
                leg.SetNColumns(len(canvas_d['1sg'][ idx*step: (idx*step) + step]))
                leg.SetTextSize(0.025)

                #find mminimu
                y_min = 0
                y_max = 0
                for gid in range(len(canvas_d['1sg'][idx*step])):
                    if canvas_d['1sg'][idx*step][gid].GetYaxis().GetXmin() < y_min : y_min = canvas_d['1sg'][idx*step][gid].GetYaxis().GetXmin()
                    if canvas_d['1sg'][idx*step][gid].GetYaxis().GetXmax() < y_max : y_max = canvas_d['1sg'][idx*step][gid].GetYaxis().GetXmax()

                y_min_new = 1.1*y_min
                y_max_new = 1.3*y_max

                print(canvas_d['1sg'])
                canvas_d['1sg'][idx*step][0].GetXaxis().SetLimits(-1, 1)
                canvas_d['1sg'][idx*step][0].GetYaxis().SetRangeUser(y_min_new, y_max_new) #add legend space
                canvas_d['1sg'][idx*step][0].GetYaxis().SetTitleOffset(1.4)
                canvas_d['1sg'][idx*step][0].GetXaxis().SetTitleOffset(1.1)
                canvas_d['1sg'][idx*step][0].GetYaxis().SetTitle(ConvertOptoLatex(op))
                canvas_d['1sg'][idx*step][0].GetYaxis().SetTitleSize(.04)
                canvas_d['1sg'][idx*step][0].GetXaxis().SetTitleSize(.04)
                canvas_d['1sg'][idx*step][0].GetXaxis().SetTitle("2nd Operator")
                canvas_d['1sg'][idx*step][0].SetTitle("")
                canvas_d['1sg'][idx*step][0].Draw("AL")
                canvas_d['min'][idx*step].Draw("P")

                name = ConvertOptoLatex(canvas_d['n_op'][idx*step])
                if canvas_d['scale'][idx*step] != 1: name = str(canvas_d['scale'][idx*step]) + " #times " + name

                leg.AddEntry(canvas_d['1sg'][idx*step][0], name, "L")

                for i,j, n, scale in zip(canvas_d['1sg'][idx*step +1:  (idx*step) + step], canvas_d['min'][idx*step +1:  (idx*step) + step], canvas_d['n_op'][idx*step +1:  (idx*step) + step], canvas_d['scale'][idx*step +1:  (idx*step) + step]):
                    for g in i:
                        #g.SetLineStyle(ls)
                        #g.SetLineColor(col)
                        g.Draw("L same")
                        if g.GetYaxis().GetXmin() < y_min : 
                            y_min = g.GetYaxis().GetXmin()
                        if g.GetYaxis().GetXmax() > y_max :
                            y_max = g.GetYaxis().GetXmax()
                    j.Draw("P same")
                    name = ConvertOptoLatex(n) 
                    if scale !=1 : name =  str(scale) + " #times " + ConvertOptoLatex(n)
                    leg.AddEntry(i[0], name, "L")

                #Draw fancy

                tex3 = ROOT.TLatex(0.86,.89,"100 fb^{-1}   (13 TeV)")
                tex3.SetNDC()
                tex3.SetTextAlign(31)
                tex3.SetTextFont(42)
                tex3.SetTextSize(0.04)
                tex3.SetLineWidth(2)
                tex3.Draw()

                if "process" in plt_options.keys():
                    if 'xpos' not in  plt_options.keys(): xpos = 0.35
                    else: xpos = plt_options['xpos']
                    if 'size' not in  plt_options.keys(): size = 0.04
                    else: size = plt_options['size']
                    if 'font' not in  plt_options.keys(): font = 42
                    else: font = plt_options['font']
                    tex4 = ROOT.TLatex(xpos,.89,plt_options['process'])
                    tex4.SetNDC()
                    tex4.SetTextAlign(31)
                    tex4.SetTextFont(font)
                    tex4.SetTextSize(size)
                    tex4.SetLineWidth(2)
                    tex4.Draw()

                if not args.splitLeg: leg.Draw()
                c.Draw()
                canvas_d['1sg'][idx*step][0].GetYaxis().SetRangeUser(-1.1*abs(y_min), 1.1*abs(y_max))
                c.Print(args.outf + "/" + op + "/r_" + op + "{}.pdf".format(idx))

                canvas_d['1sg'][idx*step][0].GetYaxis().SetRangeUser(-1.5*abs(y_min), 1.5*abs(y_max))
                c.Draw()
                c.Print(args.outf + "/" + op + "/" + op + "{}.pdf".format(idx))

        if args.splitLeg:

            c = ROOT.TCanvas("c_legend", "c_legend", 1000, 300)
            margins = 0.13

            ROOT.gPad.SetRightMargin(margins)
            ROOT.gPad.SetLeftMargin(margins)
            ROOT.gPad.SetBottomMargin(margins)
            ROOT.gPad.SetTopMargin(margins)
            ROOT.gPad.SetFrameLineWidth(1)
            ROOT.gPad.SetTicks()

            leg = ROOT.TLegend(0.15, 0.15, 0.85, 0.85)
            leg.SetBorderSize(0)
            leg.SetNColumns(5)
            leg.SetTextSize(0.06)

            #fakeGa = deepcopy(canvas_d['1sg'][0][0])
            #fakeGa.GetYaxis().SetTitleOffset(1.1)
            #fakeGa.GetYaxis().SetTitleOffset(1.1)
            #fakeGa.SetLineColor(0)
            #fakeGa.GetXaxis().SetLabelSize(0)
            #fakeGa.GetYaxis().SetLabelSize(0)
            #fakeGa.GetXaxis().SetTitle("")
            #fakeGa.GetYaxis().SetTitle("")
            #fakeGa.SetTitle("")
            #fakeGa.Draw("AL")
            
            frame = c.DrawFrame(-1,-1,1,1)
            frame.GetXaxis().SetLabelSize(0)
            frame.GetYaxis().SetLabelSize(0)
            frame.GetYaxis().SetNdivisions(505)
            frame.GetXaxis().SetTitle("")
            frame.GetYaxis().SetTitle("")
            graphs = []

            for idx, key in enumerate(op_colors.keys()):
                color = op_colors[key]["color"]
                ls = op_colors[key]["ls"]

                fakeG = ROOT.TGraph()
                fakeG.SetLineColor(color)
                fakeG.SetLineStyle(ls)
                fakeG.SetLineWidth(3)
                graphs.append(deepcopy(fakeG))
                leg.AddEntry(graphs[idx], ConvertOptoLatex(key), "F")


            #tex3 = ROOT.TLatex(0.86,.89,"100 fb^{-1}   (13 TeV)")
            #tex3.SetNDC()
            #tex3.SetTextAlign(31)
            #tex3.SetTextFont(42)
            #tex3.SetTextSize(0.04)
            #tex3.SetLineWidth(2)
            #tex3.Draw()

            leg.Draw()

            c.Draw()
            c.Print(args.outf + "/legend.pdf")
            c.Print(args.outf + "/legend.png")

        
    else:
        
        for op_pair in operators.keys():

            print("[INFO]: Generating plots for {}".format(op_pair))

            #mkdir(args.outf + "/" + op_pair)

            ops = op_pair.split("_")
            op_x = ops[0]
            op_y = ops[1]

            channels = operators[op_pair].keys()


            graphs = []

            max_x = max_y = min_y = min_x = 0
            
            #cycling on all the channels in the cfg
            for key in channels:
                print("... Retrieving channel {} ...".format(key))

                #extrapolate gs (the full 2d scan), contours (2 graphs [1sigma and 2 sigma])
                # and the minimum (0,0) by construction
                gs, cont_graphs, exp = Retrieve2DLikelihoodCombined(operators[op_pair][key]['path'], 
                                                                [op_x, op_y], args.maxNLL, 1., 1.)


                print(len(cont_graphs))
                """
                for j in cont_graphs:
                    for item in j:
                        if item.GetXaxis().GetXmin() < min_x: min_x = item.GetXaxis().GetXmin()
                        if item.GetXaxis().GetXmax() > max_x: max_x = item.GetXaxis().GetXmax()
                        if item.GetYaxis().GetXmin() < min_y: min_y = item.GetYaxis().GetXmin()
                        if item.GetYaxis().GetXmax() > max_y: max_y = item.GetYaxis().GetXmax()
                """

                # min_x, max_x = cont_graphs[0].GetXaxis().GetXmin(), cont_graphs[0].GetXaxis().GetXmax() 
                # min_y, max_y = cont_graphs[0].GetYaxis().GetXmin(), cont_graphs[0].GetYaxis().GetXmax() 

                #set style
                for j in range(len(cont_graphs)):
                    for h in range(len(cont_graphs[j])):
                        cont_graphs[j][h].SetLineWidth(5)

                

                #shaded combination 
                if key == "combined":
                    #for j in range(len(cont_graphs)):
                    for h in range(len(cont_graphs[0])):
                        cont_graphs[0][h].SetLineColorAlpha(int(operators[op_pair][key]['color']), 0.9)
                        cont_graphs[0][h].SetFillStyle(1001) #sollid
                        cont_graphs[0][h].SetFillColorAlpha(int(operators[op_pair][key]['color']), 0.1)
                        if cont_graphs[0][h].GetXaxis().GetXmin() < min_x: min_x = cont_graphs[0][h].GetXaxis().GetXmin()
                        if cont_graphs[0][h].GetXaxis().GetXmax() > max_x: max_x = cont_graphs[0][h].GetXaxis().GetXmax()
                        if cont_graphs[0][h].GetYaxis().GetXmin() < min_y: min_y = cont_graphs[0][h].GetYaxis().GetXmin()
                        if cont_graphs[0][h].GetYaxis().GetXmax() > max_y: max_y = cont_graphs[0][h].GetYaxis().GetXmax()
                        # cont_graphs[0].SetLineColorAlpha(int(operators[op_pair][key]['color']), 0.7)

                    #centering on the combined
                    min_x = 4*min_x
                    max_x = 4*max_x 
                    min_y = 2*min_y 
                    max_y = 2*max_y
                    
                else:
                    for j in range(len(cont_graphs)):
                        for h in range(len(cont_graphs[j])):
                            cont_graphs[j][h].SetLineColor(int(operators[op_pair][key]['color']))
                            cont_graphs[j][h].SetFillStyle(0)
                            cont_graphs[j][h].SetFillColor(0)
                            #cont_graphs[j][h].SetFillColorAlpha(int(operators[op_pair][key]['color']), 0.1)
                            #min_x = cont_graphs[j][h].GetXaxis().GetXmin()
                            #max_x = cont_graphs[j][h].GetXaxis().GetXmax()
                            #min_y = cont_graphs[j][h].GetYaxis().GetXmin()
                            #max_y = cont_graphs[j][h].GetYaxis().GetXmax()
                
                for j in range(len(cont_graphs)):
                        for h in range(len(cont_graphs[j])):
                            cont_graphs[j][h].SetLineStyle(int(operators[op_pair][key]['linestyle']))
                
                #print(cont_graphs[0])
                if len(cont_graphs) == 0:  continue
                graphs.append([key, cont_graphs[0], exp, [min_x, max_x],[min_y, max_y]])

            #zoomed version
            
            # put the combined graph at first position in the list
            # soit will be plotted first
            combo_id = 0
            for idx, g in enumerate(graphs):
                if g[0] == "combined": combo_id = idx 

            combo = graphs.pop(combo_id)
            graphs.insert(0, combo)
            
            # now plotting for real

            c = ROOT.TCanvas("c_{}".format(op_pair), "c_{}".format(op_pair), 1000, 1000)

            margins = 0.13

            ROOT.gPad.SetRightMargin(margins)
            ROOT.gPad.SetLeftMargin(margins)
            ROOT.gPad.SetBottomMargin(margins)
            ROOT.gPad.SetTopMargin(margins)
            ROOT.gPad.SetFrameLineWidth(3)
            ROOT.gPad.SetTicks()

            leg = ROOT.TLegend(0.5, 0.65, 0.85, 0.85)
            leg.SetBorderSize(0)
            leg.SetNColumns((int(len(graphs) + 1)/2))
            leg.SetTextSize(0.03)

            #c.SetGrid()

            #first graph
            for i in range(len(graphs[0][1])):
                graphs[0][1][i].GetYaxis().SetTitleOffset(1.4)
                graphs[0][1][i].GetXaxis().SetTitleOffset(1.1)
                graphs[0][1][i].GetXaxis().SetTitleSize(.04)
                graphs[0][1][i].GetYaxis().SetTitleSize(.04)
                graphs[0][1][i].GetYaxis().SetTitle(ConvertOptoLatex(op_y))
                graphs[0][1][i].GetXaxis().SetTitle(ConvertOptoLatex(op_x))
                graphs[0][1][i].SetTitle("")
                #graphs[0][1].SetLineStyle(linestyles[0])
                if i == 0:
                    #graphs[0][1][i].GetYaxis().SetRangeUser(graphs[0][1][i].GetYaxis().GetXmin(), graphs[0][1][i].GetYaxis().GetXmax() + 0.2*(graphs[0][1][i].GetYaxis().GetXmax()))
                    if graphs[0][0]  == "combined": 
                        graphs[0][1][i].Draw("ALF")
                        #graphs[0][1][i].Draw("A")
                        graphs[0][1][i].GetYaxis().SetRangeUser(graphs[0][4][0], graphs[0][4][1])
                        graphs[0][1][i].GetXaxis().SetLimits(graphs[0][3][0], graphs[0][3][1])
                        graphs[0][1][i].Draw("ALF")
                        #graphs[0][1][i].Draw("A")
                        c.Update()

                    else: 
                        graphs[0][1][i].Draw("AL")
                        graphs[0][1][i].GetYaxis().SetRangeUser(graphs[0][4][0], graphs[0][4][1])
                        graphs[0][1][i].GetXaxis().SetLimits(graphs[0][3][0], graphs[0][3][1])
                        graphs[0][1][i].Draw("AL")
                        c.Update()
                else:
                    if graphs[0][0]  == "combined": graphs[0][1][i].Draw("LF same")
                    else: graphs[0][1][i].Draw("L same")
            graphs[0][2].Draw("P same")

            leg.AddEntry(graphs[0][2], "SM", "P")

            name = graphs[0][0]
            #leg.AddEntry(graphs[0][1][0], name, "L")
            leg.AddEntry(graphs[0][1][0], ConvertProc(name), "F")

            for i in graphs[1:]:
                for j in i[1]:
                    if i[0] == "combined": 
                        print("combined")
                        j.Draw("LF same")
                    else: j.Draw("L same")
                #i[2].Draw("P same")
                name = i[0]
                #if name == "combined": name = "Combined"
                #if scale!=1 : name =  str(scale) + " #times " + n
                #leg.AddEntry(i[1][0], name, "L")
                print(i[0], i[1])
                try:
                    leg.AddEntry(i[1][0], ConvertProc(name), "F")
                except:
                    pass

            #Draw fancy

            tex3 = ROOT.TLatex(0.86,.89,"100 fb^{-1}   (13 TeV)")
            tex3.SetNDC()
            tex3.SetTextAlign(31)
            tex3.SetTextFont(42)
            tex3.SetTextSize(0.04)
            tex3.SetLineWidth(2)
            tex3.Draw()

            if "process" in plt_options.keys():
                if 'xpos' not in  plt_options.keys(): xpos = 0.35
                else: xpos = plt_options['xpos']
                if 'size' not in  plt_options.keys(): size = 0.04
                else: size = plt_options['size']
                if 'font' not in  plt_options.keys(): font = 42
                else: font = plt_options['font']
                tex4 = ROOT.TLatex(xpos,.89,plt_options['process'])
                tex4.SetNDC()
                tex4.SetTextAlign(31)
                tex4.SetTextFont(font)
                tex4.SetTextSize(size)
                tex4.SetLineWidth(2)
                tex4.Draw()

            
            if not args.splitLeg: leg.Draw()
            c.Draw()
            c.Print(args.outf + "/" + op_pair + ".pdf")
            c.Print(args.outf + "/" + op_pair + ".png")

            #unzoomed version

            lower_x = []
            higher_x = []
            lower_y = []
            higher_y = []

            for i in graphs:
                lower_x.append(i[3][0])
                higher_x.append(i[3][1])
                lower_y.append(i[4][0])
                higher_y.append(i[4][1])
            
            min_x  = min(lower_x)
            max_x  = max(higher_x)
            min_y  = min(lower_y)
            max_y  = max(higher_y)

            print(lower_x)

            c = ROOT.TCanvas("c_{}_unzoomed".format(op_pair), "c_{}_unzoomed".format(op_pair), 1000, 1000)

            margins = 0.13

            ROOT.gPad.SetRightMargin(margins)
            ROOT.gPad.SetLeftMargin(margins)
            ROOT.gPad.SetBottomMargin(margins)
            ROOT.gPad.SetTopMargin(margins)
            ROOT.gPad.SetFrameLineWidth(3)
            ROOT.gPad.SetTicks()

            leg = ROOT.TLegend(0.5, 0.65, 0.85, 0.85)
            leg.SetBorderSize(0)
            leg.SetNColumns(int(len(graphs)/2))
            leg.SetTextSize(0.03)

            #c.SetGrid()

            #first graph
            for i in range(len(graphs[0][1])):
                graphs[0][1][i].GetYaxis().SetRangeUser(min_y, max_y + 0.3*max_y)
                graphs[0][1][i].GetXaxis().SetLimits(min_x, max_x)
                graphs[0][1][i].GetYaxis().SetTitleOffset(1.4)
                graphs[0][1][i].GetXaxis().SetTitleOffset(1.1)
                graphs[0][1][i].GetXaxis().SetTitleSize(.04)
                graphs[0][1][i].GetYaxis().SetTitleSize(.04)
                graphs[0][1][i].GetYaxis().SetTitle(ConvertOptoLatex(op_y))
                graphs[0][1][i].GetXaxis().SetTitle(ConvertOptoLatex(op_x))
                graphs[0][1][i].SetTitle("")
                #graphs[0][1].SetLineStyle(linestyles[0])
                if i == 0:
                    graphs[0][1][i].Draw("ALF")
                else:
                    graphs[0][1][i].Draw("LF same")

            graphs[0][2].Draw("P same")
            leg.AddEntry(graphs[0][2], "SM", "P")

            """
            graphs[0][1].GetYaxis().SetRangeUser(min_y, max_y)
            graphs[0][1].GetXaxis().SetRangeUser(min_x, max_x)
            graphs[0][1].GetYaxis().SetTitleOffset(1.5)
            graphs[0][1].GetXaxis().SetTitleOffset(1.2)
            graphs[0][1].GetYaxis().SetTitle(ConvertOptoLatex(op_y))
            graphs[0][1].GetXaxis().SetTitle(ConvertOptoLatex(op_x))
            graphs[0][1].SetTitle("")
            #graphs[0][1].SetLineStyle(linestyles[0])
            graphs[0][1].Draw("AL")
            graphs[0][2].Draw("P same")
            """

            name = graphs[0][0]
            # leg.AddEntry(graphs[0][1][0], name, "L")
            leg.AddEntry(graphs[0][1][0], ConvertProc(name), "F")

            for i in graphs[1:]:
                for j in i[1]:
                    j.Draw("L same")
                #i[2].Draw("P same")
                name = i[0]
                if name == "combined": name = "Combined"
                # if scale!=1 : name =  str(scale) + " #times " + n
                #leg.AddEntry(i[1][0], ConvertProc(name), "F")
                # leg.AddEntry(i[1][0], name, "L")
                try:
                    leg.AddEntry(i[1][0], ConvertProc(name), "F")
                except:
                    pass

            #Draw fancy

            tex3 = ROOT.TLatex(0.86,.89,"100 fb^{-1}   (13 TeV)")
            tex3.SetNDC()
            tex3.SetTextAlign(31)
            tex3.SetTextFont(42)
            tex3.SetTextSize(0.04)
            tex3.SetLineWidth(3)
            tex3.Draw()

            if "process" in plt_options.keys():
                if 'xpos' not in  plt_options.keys(): xpos = 0.35
                else: xpos = plt_options['xpos']
                if 'size' not in  plt_options.keys(): size = 0.04
                else: size = plt_options['size']
                if 'font' not in  plt_options.keys(): font = 42
                else: font = plt_options['font']
                tex4 = ROOT.TLatex(xpos,.89,plt_options['process'])
                tex4.SetNDC()
                tex4.SetTextAlign(31)
                tex4.SetTextFont(font)
                tex4.SetTextSize(size)
                tex4.SetLineWidth(3)
                tex4.Draw()

            if not args.splitLeg: leg.Draw()
            c.Draw()
            c.Print(args.outf + "/" + op_pair + "_unzoomed.pdf")
            c.Print(args.outf + "/" + op_pair + "_unzoomed.png")

        if args.splitLeg:

            c = ROOT.TCanvas("c_legend", "c_legend", 1000, 1000)
            margins = 0.13

            ROOT.gPad.SetRightMargin(margins)
            ROOT.gPad.SetLeftMargin(margins)
            ROOT.gPad.SetBottomMargin(margins)
            ROOT.gPad.SetTopMargin(margins)
            ROOT.gPad.SetFrameLineWidth(3)
            ROOT.gPad.SetTicks()

            leg = ROOT.TLegend(0.15, 0.15, 0.85, 0.85)
            leg.SetBorderSize(0)
            leg.SetNColumns(1)
            leg.SetTextSize(0.06)

            fakeG = deepcopy(graphs[0][1][0])
            fakeG.GetYaxis().SetTitleOffset(1.1)
            fakeG.GetYaxis().SetTitleOffset(1.1)
            fakeG.SetLineColor(0)
            fakeG.GetXaxis().SetLabelSize(0)
            fakeG.GetYaxis().SetLabelSize(0)
            fakeG.GetXaxis().SetTitle("")
            fakeG.GetYaxis().SetTitle("")
            fakeG.SetTitle("")
            fakeG.Draw("AL")

            name = graphs[0][0]
            leg.AddEntry(graphs[0][1][0], ConvertProc(name), "F")

            for i in graphs[1:]:
                name = i[0]
                leg.AddEntry(i[1][0], ConvertProc(name), "F")

            tex3 = ROOT.TLatex(0.86,.89,"100 fb^{-1}   (13 TeV)")
            tex3.SetNDC()
            tex3.SetTextAlign(31)
            tex3.SetTextFont(42)
            tex3.SetTextSize(0.04)
            tex3.SetLineWidth(2)
            tex3.Draw()

            leg.Draw()

            c.Draw()
            c.Print(args.outf + "/legend.pdf")
            c.Print(args.outf + "/legend.png")

    os.system("cp /afs/cern.ch/user/g/gboldrin/index.php " + args.outf)


