import ROOT

ws = ROOT.RooWorkspace()
ws.factory("Gaussian::_g1(x[-5,5],_m1[-1,-3,3],res[1,0.1,2])")
ws.factory("Gaussian::_g2(x,_m2[1,-3,3],expr::_resm('1.5*res',{res}))")
ws.factory("Uniform::_p_res(res)")
ws.factory("SUM::_punzi_model(_f[0.3,0,1] * PROD::_cat1(_g1|res,_p_res),PROD::_cat2(_g2|res,_p_res))")
ws.defineSet("observables","x,res")
ws.saveSnapshot("param_point","_f,_m1,_m2")

pdf = ws.pdf("_punzi_model")
d = pdf.generate(ROOT.RooArgSet(ws.var("x"),ws.var("res")),2000)
out = ROOT.TFile.Open("example.root","recreate")
out.cd()
d.SetName("punzi_example")
getattr(ws,"import")(d)
ws.Write("ws")
out.Close()
