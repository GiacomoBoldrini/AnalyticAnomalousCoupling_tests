import ROOT 
import os
import numpy as np
from itertools import combinations
from copy import deepcopy
import argparse

from copy import deepcopy
class HistoBuilder:
    
    def __init__(self):
        self.pois = []
        self.ppois = []
        self.shapes = {}

        self.bins = 20
        
        self.minimPoisValue = {}
        self.historyHistos = {}
         
        self.historySingleHistos = {}
        
        self.dueDHistos =  {}
        
        self.shNames = ["sm", "sm_lin_quad", "sm_lin_quad_mixed", "quad"]

        self.o = "."

    def setPoiOfInt(self,  interestPOI):
        self.interestPOI = interestPOI
        
    def setPoi(self,  pois, interestPOI):
        self.pois = pois
        self.ppois = list(combinations(pois, 2))
        self.interestPOI = interestPOI

        self.PoisValue = {}
        for i in self.pois + [self.interestPOI]: self.PoisValue[i] = [] 
        
    def setShapes(self, file):

        f = ROOT.TFile(file)
        for i in f.GetListOfKeys():
            name = i.GetName()
            self.shapes[name] = deepcopy(f.Get(name))
        
        f.Close()
        
        print("Initialized shapes in memory")
        
    def setScan(self, file, tree):
        self.file = file
        self.tree = tree
        
        print("Initialized LL scan in memory")
        
    def returnShapes(self):
        return self.shapes
    
    def getScan(self):
        
        f = ROOT.TFile(self.file)
        t = f.Get(self.tree)
        
        if isinstance(self.interestPOI, str):

            to_draw = ROOT.TString("2*deltaNLL:{}".format(self.interestPOI))
            n = t.Draw( to_draw.Data() , "deltaNLL<{} && deltaNLL>{}".format(1e10,-30), "l")


            x = np.ndarray((n), 'd', t.GetV2())[1:] #removing first element (0,0)
            y_ = np.ndarray((n), 'd', t.GetV1())[1:] #removing first element (0,0)

            x, ind = np.unique(x, return_index = True)
            y_ = y_[ind]
            y = np.array([i-min(y_) for i in y_]) #shifting likelihood toward 0

            graphScan = ROOT.TGraph(x.size,x,y)
            graphScan.GetXaxis().SetTitle(self.interestPOI)
            graphScan.GetYaxis().SetTitle("-2#DeltaLL")
            graphScan.SetTitle("")
            graphScan.SetLineColor(ROOT.kRed)
            graphScan.SetMarkerSize(1)
            graphScan.SetMarkerColor(ROOT.kRed)
            graphScan.SetMarkerStyle(8)
            graphScan.SetLineWidth(2)
            
            f.Close()

            return graphScan
        
    def compute(self, poiInterest):
        
        #self.historySingleHistos = {}
        #sm 
        bench = deepcopy(self.shapes["histo_sm"])
        #bench = self.shapes["histo_sm"].Clone("histo_sm_{}".format(poiInterest))
        #bench.SetDirectory(0)

        fact = 1
        poi_sum = 0
        poiPair_sum = 0
        for poi in self.pois:
            poi_sum +=  self.minimPoisValue[poi]

        fact -= poi_sum

        for pois in self.ppois:
            poiPair_sum += self.minimPoisValue[pois[0]]*self.minimPoisValue[pois[1]]

        fact += poiPair_sum

        bench.Scale(fact)
        #self.historySingleHistos["SM"] = deepcopy(bench)
        #self.historySingleHistos["SM"] = deepcopy(bench)


        #sm + li + qu
        for poi in self.pois:
            h = deepcopy(self.shapes["histo_sm_lin_quad_" + poi.strip("k_")])
            #h = self.shapes["histo_sm_lin_quad_" + poi.strip("k_")].Clone("histo_sm_lin_quad_" + poi.strip("k_") + "_{}".format(poiInterest))
            #h.SetDirectory(0)
            poiVal = self.minimPoisValue[poi]
            fact = poiVal
            for  j in self.pois:
                if j != poi:
                    fact -= poiVal * self.minimPoisValue[j]

            h.Scale(fact)
            #self.historySingleHistos["sm_lin_quad_"+ poi.strip("k_")] = h
            bench.Add(h)

        #qu
        for poi in self.pois:
            h = deepcopy(self.shapes["histo_quad_" + poi.strip("k_")])
            #h = self.shapes["histo_quad_" + poi.strip("k_")].Clone("histo_quad_" + poi.strip("k_") + "_{}".format(poiInterest))
            #h.SetDirectory(0)
            h.Scale(self.minimPoisValue[poi]*self.minimPoisValue[poi] - self.minimPoisValue[poi])
            #self.historySingleHistos["quad_"+ poi.strip("k_")] = h
            
            bench.Add(h)
        
        #mixed
        for ppair in self.ppois:

            name = "histo_sm_lin_quad_mixed_" + ppair[0].strip("k_") + "_" + ppair[1].strip("k_")

            if name not in  self.shapes.keys():
                name = "histo_sm_lin_quad_mixed_" + ppair[1].strip("k_") + "_" + ppair[0].strip("k_")

                if name not in  self.shapes.keys():
                    print ("No shape for {} {}".format(ppair[0], ppair[1]))
                    continue

            h = deepcopy(self.shapes[name])
            #h = self.shapes[name].Clone(name + "_{}".format(poiInterest))
            #h.SetDirectory(0)
            fact = self.minimPoisValue[ppair[0]] * self.minimPoisValue[ppair[1]]
            h.Scale(fact)
            #self.historySingleHistos[name.split("histo_")[1]] = h

            bench.Add(h)


        if bench.GetMinimum() < 0:
            print ("foundBin < 0" + str(bench.GetMinimum()) )

        """
        ROOT.gStyle.SetPalette(ROOT.kRainBow)
        ROOT.gStyle.SetOptStat(0)

        c = ROOT.TCanvas("c_{}".format(poiInterest), "c_{}".format(poiInterest), 1000, 1000)
        leg = ROOT.TLegend(1.0, 0.11, 0.7, 0.93)

        ROOT.gPad.SetFrameLineWidth(3)

        pad1 = ROOT.TPad("pad", "pad", 0, 0.3, 1, 1)
        pad1.SetFrameLineWidth(2)
        pad1.SetBottomMargin(0.005)
        pad1.SetRightMargin(0.32)
        pad1.Draw()

        pad2 = ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.3)
        pad2.SetFrameLineWidth(2)
        pad2.SetRightMargin(0.32)

        pad2.SetFrameBorderMode(0)
        pad2.SetBorderMode(0)
        pad2.SetBottomMargin(0.4)
        pad2.Draw()

        pad1.cd()

        min_ = 0
        max_ = 0
        print(self.historySingleHistos)
        print(self.historySingleHistos["sm_lin_quad_mixed_cqq1_cqq31"], self.historySingleHistos["sm_lin_quad_mixed_cqq1_cqq31"].GetMinimum())
        print("zembra  mmarrone")
        for key in self.historySingleHistos:
            #print(self.historySingleHistos)
            a =  self.historySingleHistos[key].GetMinimum()
            b = self.historySingleHistos[key].GetMaximum()
            if a < min_: min_ = a
            if b > max_: max_ = b

        print("bau")
        self.shapes["histo_sm"].SetLineColor(ROOT.kRed)
        self.shapes["histo_sm"].SetLineWidth(5)
        self.shapes["histo_sm"].SetLineStyle(3)
        self.shapes["histo_sm"].Draw("hist")
        self.shapes["histo_sm"].SetMinimum(min_ - 0.2*(abs(min_)))
        self.shapes["histo_sm"].SetMaximum(max_ + 0.2*(abs(max_)))

        i = 0
        for key in self.historySingleHistos.keys():
            if key=="sm": continue
            if i == 0: h = deepcopy(self.historySingleHistos[key])
            self.historySingleHistos[key].SetLineColor(ROOT.kBlue)
            leg.AddEntry(self.historySingleHistos[key], key)
            self.historySingleHistos[key].Draw("hist PLC same")
            if i != 0: h.Add(self.historySingleHistos[key])
            i += 1

        print("heyla")

        h.SetLineColor(ROOT.kBlack)
        h.SetLineWidth(3)
        h.SetLineStyle(2)

        leg.AddEntry(h, "Total")
        leg.AddEntry(self.shapes["histo_sm"], "Real SM")

        h.Draw("hist same")

        pad2.cd()

        hratio = h.Clone("Total")
        hratio.Divide(self.shapes["histo_sm"])

        hratio.GetYaxis().SetTitle("BSM / SM")
        hratio.Draw("hist")

        print("oh god")


        c.Update()

        pad2.Draw()
        c.cd()
        leg.Draw()
        c.Draw()

        c.SaveAs(self.o + "/components_{}.pdf".format(poiInterest))
        c.SaveAs(self.o + "/components_{}.png".format(poiInterest))

        del self.historySingleHistos 

        """
            
        return bench

        

    def runHistoryEFTNeg(self):
        
        f = ROOT.TFile(self.file)
        t = f.Get(self.tree)

        i = 0
        for event in t:
            for poi in self.pois:
                self.minimPoisValue[poi] = getattr(event, poi)
                self.PoisValue[poi].append(getattr(event, poi))
            
            poiVal = getattr(event, self.interestPOI)
            self.PoisValue[self.interestPOI].append(poiVal)

            #histo = self.compute(poiVal)
            histo = self.compute(i)
            self.historyHistos[poiVal] = histo

            i+=1  

        f.Close()

    def run2DHistograms(self):

        f = ROOT.TFile(self.file)
        t = f.Get(self.tree)
        
        for poi in self.pois:
            if poi != self.interestPOI:

                to_draw = ROOT.TString("2*deltaNLL:{}:{}".format(self.interestPOI, poi))
                cuts = ROOT.TString("deltaNLL<{} && deltaNLL>{}".format(10,-30))
                n = t.Draw(to_draw.Data(), cuts.Data(), "goff")

                z_ = np.ndarray((n), 'd', t.GetV1())
                z = np.array([i-min(z_) for i in z_])

                graphScan = ROOT.TGraph2D(n,t.GetV2(),t.GetV3(),z)
                graphScan.SetNpx(200)
                graphScan.SetNpy(200)
                
                graphScan.SetLineWidth(3)
                    
                graphScan.SetTitle("")
                graphScan.GetXaxis().SetTitle(self.interestPOI)
                graphScan.GetYaxis().SetTitle(poi)
                graphScan.GetZaxis().SetTitle("- 2#Delta logL")
                graphScan.GetZaxis().SetRangeUser(0,10)

                myHisto = graphScan.GetHistogram().Clone("histo_{}".format(poi))
                for i  in range(myHisto.GetSize()):
                    myHisto.SetBinContent(i+1, 0)
                
                for i in range(graphScan.GetN()):
                    myHisto.Fill( graphScan.GetX()[i],  graphScan.GetY()[i],  graphScan.GetZ()[i] + 0.001)
                
                myHisto.SetTitle("")
                myHisto.GetXaxis().SetTitle(self.interestPOI)
                myHisto.GetYaxis().SetTitle(poi)
                myHisto.GetZaxis().SetTitle("- 2#Delta logL")

                self.dueDHistos[poi] = deepcopy(myHisto)

        f.Close()
                

                
    def returnHistory(self):
        self.historyHistos["sm"] = self.shapes["histo_sm"]
        return self.historyHistos
    
    def returnComponentHistory(self):
        self.historySingleHistos["sm"] = self.shapes["histo_sm"]
        return self.historySingleHistos
                        

    def return2DHistos(self):
        return self.dueDHistos
                        


def mkdir(p):
   try:
      os.mkdir(p)
   except:
      return 


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Command line parser for fit inspector')
    parser.add_argument('--f',     dest='f',     help='The fit results with all operators branches', required = True)
    parser.add_argument('--s',     dest='s',     help='The shapes .root file', required = True)
    parser.add_argument('--p',     dest='p',     help='The POI of interest', required = True)
    parser.add_argument('--pf',     dest='pf',     help='The POI floating, default is  all', required = False, default="k_cHDD,k_cHWB,k_cHW,k_cHbox,k_cHl1,k_cHl3,k_cHq1,k_cHq3,k_cW,k_cll1,k_cll,k_cqq11,k_cqq1,k_cqq31,k_cqq3")
    parser.add_argument('--e',     dest='e',     help='Exclude this pois from the scan', required = False, default="")
    parser.add_argument('--o',     dest='o',     help='Out directory name', required = False, default="inspector")
    parser.add_argument('--t',     dest='t',     help='Out directory name', required = False, default="inspector")

    args = parser.parse_args()

    #ROOT.gROOT.SetBatch(1)

    mkdir(args.o)
    os.system("cp /afs/cern.ch/user/g/gboldrin/index.php " + args.o)
    thePOI = args.p 
    floatPOIs = args.pf.split(",")
    excludePOIs = args.e.split(",")
    floatingPOIs = [ i for i in  floatPOIs if i not in excludePOIs]

    print("# ------- INFO ------ #")
    print("Interest POI: {}".format(thePOI))
    print("All other floating POIS: {}".format(floatingPOIs))
    print("# ------- INFO ------ #")

    #initializing
    hh = HistoBuilder()
    hh.setPoi(floatingPOIs, thePOI)
    hh.setShapes(args.s)
    hh.setScan(args.f, "limit")


    #running and saving histos
    hh.runHistoryEFTNeg()
    
    print("Finished saving all histo fro history...")

    #retrieving total histos
    hist  = hh.returnHistory()
    hist["sm"].SetLineStyle(2)
    hist["sm"].SetLineWidth(2)
    hist["sm"].SetLineColor(ROOT.kBlack)

    leg = ROOT.TLegend(0.89, 0.89, 0.7, 0.7)

    leg.AddEntry(hist["sm"], "SM")
    
    i = 0
    for key in hist.keys():
        
        if key ==  "sm" : continue

        h = hist[key]
        h.SetLineColor(ROOT.kRed)

        if i == 0:
            leg.AddEntry(h, "EFT Total")

        c = ROOT.TCanvas("c_{}".format(key), "c_{}".format(key), 1000, 1000)
        
        max_ = hist["sm"].GetMaximum()
        min_ = hist["sm"].GetMinimum()
        if  h.GetMaximum() > max_: max_ =  h.GetMaximum()
        if  h.GetMinimum() < min_: min_ =  h.GetMinimum()

        hist["sm"].SetMaximum(max_)
        hist["sm"].SetMinimum(min_)

        hist["sm"].Draw("hist")
        h.Draw("hist same")

        ltx = ROOT.TLatex()
        ltx.SetTextSize(0.02)
        ltx.SetTextAlign(12)
        ltx.DrawLatex(h.GetXaxis().GetXmin(), h.GetMaximum(), "Integral: {} Minimum: {}".format(h.Integral(), h.GetMinimum()))

        leg.Draw()
        c.Draw()
        c.SaveAs(args.o + "/{}.pdf".format(key))
        c.SaveAs(args.o + "/{}.png".format(key))

        i+=1
    
    hh.run2DHistograms()
    duedH = hh.return2DHistos()
    for val in  duedH.keys():
        c = ROOT.TCanvas("c_{}".format(val), "c_{}".format(val), 1000, 1000)
        c.SetRightMargin(0.15)
        c.SetLeftMargin(0.15)
        c.SetGrid()
        duedH[val].Draw("colz")
        c.Draw()
        c.SaveAs(args.o + "/dued_{}.pdf".format(val))
        c.SaveAs(args.o + "/dued_{}.png".format(val))


    gs = hh.getScan()
    c = ROOT.TCanvas("c_{}".format(thePOI), "c_{}".format(thePOI), 1000, 1000)
    gs.Draw("AP")
    c.Draw()
    c.SaveAs(args.o + "/LL_{}.pdf".format(thePOI))
    c.SaveAs(args.o + "/LL_{}.png".format(thePOI))




    #retrieving single coponents:
    # comp = hh.returnComponentHistory()


    # print(comp)

    
    # for val in comp.keys():

    #     if  val== "sm": continue

    #     ROOT.gStyle.SetPalette(ROOT.kRainBow)
    #     ROOT.gStyle.SetOptStat(0)

    #     c = ROOT.TCanvas("c_{}".format(val), "c_{}".format(val), 1000, 1000)
    #     leg = ROOT.TLegend(1.0, 0.11, 0.7, 0.93)

    #     ROOT.gPad.SetFrameLineWidth(3)

    #     pad1 = ROOT.TPad("pad", "pad", 0, 0.3, 1, 1)
    #     pad1.SetFrameLineWidth(2)
    #     pad1.SetBottomMargin(0.005)
    #     pad1.SetRightMargin(0.32)
    #     pad1.Draw()

    #     pad2 = ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.3)
    #     pad2.SetFrameLineWidth(2)
    #     pad2.SetRightMargin(0.32)

    #     pad2.SetFrameBorderMode(0)
    #     pad2.SetBorderMode(0)
    #     pad2.SetBottomMargin(0.4)
    #     pad2.Draw()

    #     pad1.cd()

    #     min_ = 0
    #     max_ = 0
    #     for key in comp[val].keys():
    #         a =  comp[val][key].GetMinimum()
    #         b = comp[val][key].GetMaximum()
    #         if a < min_: min_ = a
    #         if b > max_: max_ = b

    #     hist["sm"].SetLineColor(ROOT.kRed)
    #     hist["sm"].SetLineWidth(5)
    #     hist["sm"].SetLineStyle(3)
    #     hist["sm"].Draw("hist")
    #     hist["sm"].SetMinimum(min_ - 0.2*(abs(min_)))
    #     hist["sm"].SetMaximum(max_ + 0.2*(abs(max_)))

    #     i = 0
    #     for key in comp[val].keys():
    #         if key=="sm": continue
    #         if i == 0: h = deepcopy(comp[val][key])
    #         comp[val][key].SetLineColor(ROOT.kBlue)
    #         leg.AddEntry(comp[val][key], key)
    #         comp[val][key].Draw("hist PLC same")
    #         if i != 0: h.Add(comp[val][key])
    #         i += 1

    #     h.SetLineColor(ROOT.kBlack)
    #     h.SetLineWidth(3)
    #     h.SetLineStyle(2)

    #     leg.AddEntry(h, "Total")
    #     leg.AddEntry(hist["sm"], "Real SM")

    #     h.Draw("hist same")

    #     pad2.cd()

    #     hratio = h.Clone("Total")
    #     hratio.Divide(hist["sm"])

    #     hratio.GetYaxis().SetTitle("BSM / SM")
    #     hratio.Draw("hist")


    #     c.Update()

    #     pad2.Draw()
    #     c.cd()
    #     leg.Draw()
    #     c.Draw()

    #     c.SaveAs(args.o + "/components_{}.pdf".format(val))
    #     c.SaveAs(args.o + "/components_{}.png".format(val))

    

    print("@INFO: Terminated  successfully")
