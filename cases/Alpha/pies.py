#
# file to visualize cost breakdown
#
# acquisition costs
# annual (fixed) costs
# operating costs (fixed and variable)

import yaml,sys,os
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
#rc('font',**{'sans-serif':['Helvetica']})
#rc('text', usetex=True)


kts2fps = 1.68781
fps2kts = 1.0/kts2fps
fps2nm  = 0.000164579
#font    = {'useTex' : True,
#           'weight' : 'normal',
#           'size'   : 18}
#matplotlib.rc('font',**font)

class costs:
   
# ===================================================================
# initialize 
# ===================================================================

   def __init__(self,n):

      DIR         = 'output/logs/'
      fname       = DIR+'log'+str(n)+'.yaml'
      print(" -- Chosen design ID",n)

      try:
         with open(fname) as f:
            fyaml=yaml.load(f)
      except:
         print('looked for file',fname)
         print('CRITICAL ERROR: file does not exist')
         quit()

# ===================================================================
# basic dictionary pointers and parameters
# ===================================================================

      self.costs        = fyaml['Costs']
      self.id           = n 

#====================================================================
# This function creates a pie chart for acquisition cost breakdown
#====================================================================

   def var_cost_pie(self): 

      var               = self.costs['variable_cost_breakdown']
      var_total         = self.costs['Variable_operating_costs']
      labels            = []
      values            = []
      expl              = []
      misc_val          = [] 
      misc_key          = []
      misc_expl         = []
      misc_total        = 0.0
      expl_val          = 0.3

#====================================================================
#loop over all elements in acquisition cost
#====================================================================

      for key in var.keys():#[-1:0:-1]:

         value          = var[key]
         percent        = value[1]
         labels.append(key.replace('_',' ') + ': ' + str(round(value[1],2)) + '%')
         values.append(value[1])
         expl.append(expl_val)
      
      fname             = 'var_cost_design_' + str(self.id) + '.png'

#====================================================================
# calculate miscellaneous percentages
# plot secondary pie if applicable
#====================================================================

      Total             = float(var_total[0])

#====================================================================
# draw primary pie
#====================================================================

      t1                = 'Operating cost:' + str(int(Total)) + \
                          '(USD/hr) : breakdown'
      data              = {'values':values,'labels':labels,'expl':expl}

      self.draw_pie(data,fname,0.1,t1)      

#====================================================================
# This function creates a pie chart for acquisition cost breakdown
#====================================================================

   def fixed_cost_pie(self): 

      fix               = self.costs['fixed_cost_breakdown']
      fix_total         = self.costs['Fixed_operating_costs']
      labels            = []
      values            = []
      expl              = []
      misc_val          = [] 
      misc_key          = []
      misc_expl         = []
      misc_total        = 0.0
      expl_val          = 0.3

#====================================================================
#loop over all elements in acquisition cost
#====================================================================

      for key in fix.keys():

         value          = fix[key]
         percent        = value[1]
         labels.append(key.replace('_',' ') + ': ' + str(round(value[1],2)) + '%')
         values.append(value[1])
         expl.append(expl_val)
      
      fname             = 'fixed_cost_design_' + str(self.id) + '.png'
      title             = 'fixed cost breakdown'

#====================================================================
# calculate miscellaneous percentages
# plot secondary pie if applicable
#====================================================================

      Total             = float(fix_total[0])

#====================================================================
# draw primary pie
#====================================================================

      t1                = 'Annual fixed cost:' + str(round(Total/1e3,0)) + \
                          '(Thousands of USD) : breakdown'
      data              = {'values':values,'labels':labels,'expl':expl}
      self.draw_pie(data,fname,0.05,t1)      

#=================================================
# remember total fixed cost in USD
#=================================================

#====================================================================
# This function creates a pie chart for acquisition cost breakdown
#====================================================================

   def acqusition_pie(self): 

      acq               = self.costs['acquisition_cost_breakdown']
      acq_total         = self.costs['Frame_acquisition']
      labels            = []
      values            = []
      expl              = []
      misc_val          = [] 
      misc_key          = []
      misc_expl         = []
      misc_total        = 0.0
      expl_val          = 0.3
#====================================================================
#loop over all elements in acquisition cost
#====================================================================

      for key in acq.keys():

         value          = acq[key]
#====================================================================
# if % of acquisition cost < 2%, groups separately
#====================================================================

         percent        = value[1]
         if(percent < 2.5):
            misc_key.append(key.replace('_',' ') + ': ' + str(round(value[1],2)) + '%')
            misc_val.append(value[1])
            misc_expl.append(expl_val)
            misc_total += value[1]
         else:
            labels.append(key.replace('_',' ') + ': ' + str(round(value[1],2)) + '%')
            values.append(value[1])
            expl.append(expl_val)
      
      fname             = 'acquisition_design_' + str(self.id) + '.png'
      fname2            = 'acquisition_miscel_' + str(self.id) + '.png'

      title             = 'acquisition cost breakdown'

#====================================================================
# calculate miscellaneous percentages
# plot secondary pie if applicable
#====================================================================

      Total             = float(self.costs['Frame_acquisition'][0])*1e6
      if(misc_total > 0):
         values.append(misc_total)
         labels.append('misc: ' + str(round(misc_total,2)) + '%')
         expl.append(expl_val)
         for il,l in enumerate(misc_key):
            misc_val[il]   = misc_val[il]/misc_total*100.0

         t2                = 'Misc. breakdown: ' + str(round(misc_total,2)) + '% of total cost'
         data              = {'values':misc_val,'labels':misc_key,'expl':misc_expl}
         self.draw_pie(data,fname2,0.1,t2)      

#====================================================================
# draw primary pie
#====================================================================

      t1                = 'Acquisition cost = ' + str(round(Total/1e3,4)) + \
                          '(Thousands of USD): breakdown'
      data              = {'values':values,'labels':labels,'expl':expl}
      self.draw_pie(data,fname,0.2,t1)      

#====================================================================
# This function creates a pie chart from a dictionary and saves it 
# to a png file of given name
#====================================================================

   def draw_pie(self,inp, savefile, expl,titlestr): 

#====================================================
      fig, ax        = plt.subplots(figsize=(10, 6), subplot_kw=dict(aspect="equal"))

      recipe         = inp['labels']  
      data           = inp['values']
      exp            = np.ones(len(inp['labels']))*expl

      wedges, texts  = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40, explode=exp)

      bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
      kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
             bbox=bbox_props, zorder=0, va="center")

      for i, p in enumerate(wedges):
         ang = (p.theta2 - p.theta1)/2. + p.theta1
         y = np.sin(np.deg2rad(ang))
         x = np.cos(np.deg2rad(ang))
         horizontalalignment  = {-1: "right", 1: "left"}[int(np.sign(x))]
         connectionstyle      = "angle,angleA=0,angleB={}".format(ang)
         kw["arrowprops"].update({"connectionstyle": connectionstyle})
         ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)

         ax.set_title(titlestr,y = 1.1,fontweight='bold')

#      plt.show()

#====================================================
#      fig1, ax1 = plt.subplots()
#      ax1.pie(data['values'], labels=data['labels'], explode=data['expl'],autopct='%1.1f%%',
#              shadow=True, startangle=0)
#      ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
      plt.savefig(savefile)
#      plt.close()

      return None
#====================================================================
# Driver program
#====================================================================

from sys import argv

if len(argv) < 2:
   print(" -- Error: performance.py requires a design ID")
   print(" -- Usage: 'python performance.py <ID> '")

#====================================================================
# get design ID
#====================================================================

n           = int(argv[1])
design      = costs(n)

#====================================================================
# draw acquisition pie chart
#====================================================================

design.acqusition_pie()
design.fixed_cost_pie()
design.var_cost_pie()