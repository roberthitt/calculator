import logging
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *

#Once the graph is created with X traces, the update will only apply to X traces and any extra traces in dic will be ignored.

# 1. create_graph Notes:
#  a. With fileopt='new', Plotly will always create a new file ==>  plot_url = py.plot(data, filename='new plot', fileopt='new')
#  b. If a graph named 'my plot' already exists in your account, then it will be overwritten with this new version and the URL of the graph will persist. ==> plot_url = py.plot(data, filename='my plot')

# 2. update_graph Notes:
#  a. if there is no data in the plot, 'extend' will create new traces. ==> plot_url = py.plot(data, filename='extend plot', fileopt='extend')
#  b. extend the traces on the plot with the data in the order supplied.==> plot_url = py.plot(data, filename='extend plot', fileopt='extend')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Graph():
    def __init__(self, username, api_key):
	""" Initializes the Graph using the www.plot.ly.com's account username and account's api key. """
    	self.username = username
    	self.api_key = api_key
	try:
	    py.sign_in(self.username, self.api_key)
	except Exception, e:
	    logger.error("In function _init_, Sign in to 'www.plot.ly.com' Failed!.\nPlease verify that the username and API-Key are correct" , exc_info=True)

    def create_graph(self, graph_name, graph_title, dic_data={} ):
	""" Creates a graph using the graph_name, graph_title, graph_x_data, and graph_y_data. Returns the graph's url in string format. """
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

    def update_graph(self, graph_name, dic_data={}):
        """ updates the selected graph's (graph's name) data. Returns the graph's url in string format. """
        self.graph_name = graph_name
        trace_list=[]
        for key,val in dic_data.items():
                key = Scatter(x=val[0], y=val[1], name=key)
                trace_list.append(key)
        data = Data(trace_list)
        plot_url=py.plot(data, filename=graph_name, fileopt="extend")
        return plot_url.encode('utf-8')

#    def delete_graph(self, username, api_key, graph_url_to_delete):
#        """ Return the response code <200=ok> (graph successfully deleted) """
#        self.username = username
#        self.api_key = api_key
#        self.graph_url_to_delete = graph_url_to_delete
#        auth = HTTPBasicAuth(self.username, self.api_key)
#        headers = {'Plotly-Client-Platform': 'python'}
#        plotly.tools.set_credentials_file(username=self.username, api_key=self.api_key)
#        response = requests.post(self.graph_url_to_delete +'trash', auth=auth, headers=headers)
#        return response





