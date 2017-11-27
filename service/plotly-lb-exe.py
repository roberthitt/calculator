#from my_test import Graph
from plotly_lib import Graph
import time
import datetime, calendar
from plotly.graph_objs import *
from datetime import date, timedelta
import plotly.plotly as py
#username and API key for your plotly account
username     = 'cs-321-project'
api_key      = 'Gz4cBfP7yMcMtNudNV84'
py.sign_in(username, api_key)
Graph('username','api_key')
#create_graph('graph_name', 'graph_title', graph_x_data, graph_y_data)
s=[datetime.datetime.now()+ timedelta(1),datetime.datetime.now()+ timedelta(2),datetime.datetime.now()+ timedelta(3),datetime.datetime.now()+ timedelta(4)]
ss=[1,4,8,22]

a=[datetime.datetime.now()- timedelta(1),datetime.datetime.now()- timedelta(2),datetime.datetime.now()- timedelta(3)]
aa=[121,125,25]


q=[datetime.datetime.now()+ timedelta(1)]
qq=[1]

w=[datetime.datetime.now()- timedelta(1),datetime.datetime.now()- timedelta(2)]
ww=[121,125]

t0 = {'tr0': [q,qq], 'tr1': [w,ww], 'tr2': [q,aa], 'tr3': [s,ww]}
t = {'tr0': [q,qq], 'tr1': [w,ww], 'tr2': [q,aa], 'tr3': [s,ww],'tr4': [s,aa], 'tr5': [a,ss]}
t2 = {'tr0': [a,qq], 'tr1': [q,ww], 'tr2': [q,ss], 'tr3': [s,ss],'tr4': [s,ww], 'tr5': [a,aa]}

g = Graph('cs-321-project','Gz4cBfP7yMcMtNudNV84')
url = g.create_graph('behrad1 trace','working',t2)
#url = g.create_graph('behrad','working','d' ,[1,5,56,7])

#print url

#s=[datetime.datetime.now(),datetime.datetime.now(),datetime.datetime.now()]

#g.update_graph('behrad1 trace',t2)
#time.sleep(5)
#print g.delete_graph('bbehmardi','FZNXgwBSwnCM0fNWg7MH',url)
