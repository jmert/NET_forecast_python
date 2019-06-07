#!/usr/bin/env python
from __future__ import print_function
import os, sys
import os.path as path

# The environment variable NETLIBDIR can be used to override the automatic
# path setup.
NETLIBDIR = os.environ.get("NETLIBDIR")
if NETLIBDIR == None or NETLIBDIR.strip() == "":
    NETLIBDIR = path.realpath(path.join(path.dirname(__file__), '..', '..'))
sys.path.append(NETLIBDIR)

print('Content-Type: text/html;charset=utf-8\r\n\r\n')

import cgi
import cgitb
cgitb.enable()

import matplotlib as mpl
mpl.use('Agg')

import NETlib as nl
n = nl.NETlib()

def main():
    
    form = cgi.FieldStorage()      # standard cgi script lines to here!    
    opts = {}

    v_cen = form.getfirst("v_cen") 
    frac_bw = form.getfirst("frac_bw") 
    opts['band']={}
    opts['band']['v_cen'] = float(v_cen) * 1e9
    opts['band']['frac_bw']= float(frac_bw)
    
    el = form.getfirst("el")
    if form.getvalue('site') == 'preselected':
        site = form.getvalue('sites_dd')
        alt = 0
    else:
        site = form.getvalue('zones_dd')
        alt = form.getfirst("alt")

    opts['atm'] = {}
    opts['atm']['site'] = site
    opts['atm']['el'] =  int(el)
    opts['atm']['alt'] = float(alt)

    T0 = form.getvalue('T0')
    Tc = form.getvalue('Tc')
    sf = form.getvalue('sf')
    beta = form.getvalue('beta')
    Rtes = form.getvalue('Rtes')
    Rshunt = form.getvalue('Rshunt')

    opts['bolo']={}
    opts['bolo']['T0']= float(T0)
    opts['bolo']['Tc']= float(Tc)
    opts['bolo']['beta']=float(beta)
    opts['bolo']['sf']=float(sf)
    opts['bolo']['Rtes']=float(Rtes)
    opts['bolo']['Rshunt']=float(Rshunt)

    if form.getvalue('layers') == 'custom':
        layersDict = {}
        for k in ['name','T','eps','Tx']:
            layersDict[k]=[]
        s = form.getvalue('review')
        sp = s.split('\n')
        for tt in sp:
            if (tt.startswith('#')) or (tt == ''): 
                continue
            ttt = tt.split(',')
            #print ttt
            layersDict['name'].append(ttt[0].strip())
            layersDict['T'].append(float(ttt[1].strip()))
            layersDict['eps'].append(float(ttt[2].strip())/100.)
        opts['s'] = layersDict
    #print opts
       
    print('<pre>')
    out = n.calc_NET(opts)
    print('</pre>')
    #contents = processInput(numStr1, numStr2)   # process input into a page
    #print(contents)

def processInput(numStr1, numStr2):  
    '''Process input parameters and return the final page as a string.'''
    num1 = float(numStr1) # transform input to output data
    num2 = float(numStr2)
    total = num1+num2
    return total
    #return fileToStr('additionTemplate.html').format(**locals())

# standard code for future cgi scripts from here on
def fileToStr(fileName): 
    """Return a string containing the contents of the named file."""
    fin = open(fileName); 
    contents = fin.read();  
    fin.close() 
    return contents

try: 
    print('<html><body>')
    main() 
    #res = fileToStr('/n/home01/dbarkats/work/20170801_S4_NET_forecast_python/output.txt')
    print("</body>  </html>")
except:
    cgi.print_exception()                 # catch and print errors
