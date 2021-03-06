from http.server import  BaseHTTPRequestHandler, HTTPServer
from cbs_mapf.planner import Planner
import socketserver
import numpy
import pickle
import json
import cgi
import os.path
import yaml

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*',)
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.end_headers()

        def do_OPTIONS(self):
            self._set_headers()

    @staticmethod
    def _draw_rect(v0, v1):
            o = []
            base = abs(v0[0] - v1[0])
            side = abs(v0[1] - v1[1])
            for xx in range(0, base, 30):
                o.append((v0[0] + xx, v0[1]))
                o.append((v0[0] + xx, v0[1] + side - 1))
            o.append((v0[0] + base, v0[1]))
            o.append((v0[0] + base, v0[1] + side - 1))
            for yy in range(0, side, 30):
                o.append((v0[0], v0[1] + yy))
                o.append((v0[0] + base - 1, v0[1] + yy))
            o.append((v0[0], v0[1] + side))
            o.append((v0[0] + base - 1, v0[1] + side))
            return o
    
    def _get_JSON_str(self, room : str) -> str:
        if os.path.isfile(room + '.pkl'):
            filename = room + '.pkl'
            with open(os.path.join(os.path.dirname(__file__),filename), 'rb') as f:
                content = pickle.load(f)
                return json.dumps(content)
            
        elif os.path.isfile(room + '.yaml'):
            filename = room + '.yaml'
            with open (os.path.join(os.path.dirname(__file__),filename), 'rb') as f:
                map_info = yaml.load(f, Loader=yaml.FullLoader)
            start_positions = map_info['START']
            goal_positions = map_info['GOAL']
            obs_map = map_info['RECT_OBSTACLES']
            obs_positions = []
            grid_size = map_info['GRID_SIZE']
            robot_rad = map_info['ROBOT_RADIUS']
            for values in obs_map.values():
                rect = self._draw_rect(values[0], values[1])
                obs_positions.extend(rect)
                
        n_agents = len(start_positions)
        #print(obs_positions)
        planner = Planner(grid_size = grid_size, robot_radius = robot_rad, static_obstacles = obs_positions)
        paths : numpy.ndarray = planner.plan(start_positions, goal_positions)
        # print("foundPath")        
        dump_list = []

        #JSON dump Agents
        for p in paths:
            print(p)
            agent = {
                "type" : "agent",
                "pathFound": True if len(p) != 0 else False,
                "path" : p.tolist() #List[Tuple[int, int]]
            }
            dump_list.append(agent)
        
        #JSON dump obstacles.
        for obs in obs_positions:
            obstacle = {
                "type" : "obstacle",
                "loc" : obs #Tuple[int, int]
            }
            dump_list.append(obstacle)

        room_name = room + '.pkl'
        with open(room_name, 'wb') as f:
            pickle.dump(dump_list, f, protocol=pickle.HIGHEST_PROTOCOL)

        return json.dumps(dump_list)




    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers['content-length'])
        message = json.loads(self.rfile.read(length))
        
        # add a property to the object, just to mess with data
        # message['received'] = 'ok'
        
        room = message['room']
        JSON_str = self._get_JSON_str(room)

        
        self._set_headers()
        self.wfile.write(JSON_str.encode('utf-8'))
        
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
        
