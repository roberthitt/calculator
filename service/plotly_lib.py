import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *

#Once the graph is created with X traces, the update will only apply to X traces and any extra traces in dic will be ignored.

# 1. create_graph Notes:
#  a. With fileopt='new', Plotly will always create a new file ==>  plot_url = py.plot(data, filename='new plot', fileopt='new')
#  b. If a graph named 'my plot' already exists in your account, then it will be overwritten with this new version and the URL of the graph will persist. ==> plot_url = py.plot(data, filen$

# 2. update_graph Notes:
#  a. if there is no data in the plot, 'extend' will create new traces. ==> plot_url = py.plot(data, filename='extend plot', fileopt='extend')
#  b. extend the traces on the plot with the data in the order supplied.==> plot_url = py.plot(data, filename='extend plot', fileopt='extend')


class Graph():
	def __init__(self, username, api_key):
		self.username = username
		self.api_key = api_key

	def create_graph(self, graph_name, graph_title, dic_data={} ):
		self.graph_name = graph_name
		self.graph_title = graph_title
		layout1 = go.Layout(
		title = self.graph_title,
		xaxis = dict(autorange = True,),
		yaxis = dict(autorange = True,)	)
		trace_list=[]
		for key,val in dic_data.items():
        		key = Scatter(x=val[0], y=val[1], name=key)
        		trace_list.append(key)
		data = Data(trace_list)
		fig = dict(data=data, layout=layout1)
		plot_url=py.plot(fig, filename=graph_name, fileopt="new")
		return plot_url.encode('utf-8')
