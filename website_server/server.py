from http.server import  BaseHTTPRequestHandler, HTTPServer
from cbs_mapf.planner import Planner
import socketserver
import numpy
import pickle
import json
import cgi

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    
    def _get_JSON_str(room : str) -> str:
        filename = room + '.pkl'
        with open(filename, 'rb') as f:
            content = pickle.load(f)
        start_positions = content[0]
        goal_positions = content[1]
        obs_positions = content[2]
        n_agents = len(start_positions)
        planner = Planner(grid_size = 60, robot_radius = 60, static_obstacles = obs_positions)
        paths : numpy.ndarray = planner.plan(start_positions, goal_positions)
        
        dump_list = []

        #JSON dump Agents
        for p in paths:
            agent = {
                "type" : "agent",
                "pathFound": True if len(p) != 0 else False,
                "path" : p #List[Tuple[int, int]]
            }
            dump_list.append(agent)
        
        #JSON dump obstacles.
        for obs in obs_positions:
            obstacle = {
                "type" : "obstacle",
                "loc" : obs #Tuple[int, int]
            }
            dump_list.append(obstacle)

        return json.dump(dump_list)




    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))
        
        # add a property to the object, just to mess with data
        # message['received'] = 'ok'
        
        room = message['room']
        JSON_str = _get_JSON_path(room)

        
        self._set_headers()
        self.wfile.write(JSON_str)
        
def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
        
