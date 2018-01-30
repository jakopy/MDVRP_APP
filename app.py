from flask import Flask, render_template, request
import json
from mdvrp import *

#get the distance matrix and location names from lat lon coordinates
#coords = "38.888665,-77.076817|38.811768,-77.054556|38.731186,-77.056399|38.891624,-77.101873|38.807791,-77.063039|38.81696,-77.042368|38.835419,-77.053051|38.800536,-77.045838|38.834099,-77.092047|38.820301,-77.052691"
#location_names, distancematrix = matrixmaker(coords).matrix()

coords = "38.888665,-77.076817|38.811768,-77.054556|38.731186,-77.056399|38.891624,-77.101873|38.807791,-77.063039|38.81696,-77.042368|38.835419,-77.053051|38.800536,-77.045838|38.834099,-77.092047|38.820301,-77.052691"
siteNames = ['1220 N Pierce St, Arlington, VA 22209, USA', '541 Colecroft Ct, Alexandria, VA 22314, USA', '8320 Fort Hunt Rd, Fort Hunt, VA 22308, USA', 'Custis Memorial Pkwy, Arlington, VA 22201, USA', '2032-2064 King St, Alexandria, VA 22314, USA', '1101-1105 N Pitt St, Alexandria, VA 22314, USA', '236-240 Evans Ln, Alexandria, VA 22305, USA', '420-426 S Pitt St, Alexandria, VA 22314, USA', '4612 34th St S, Arlington, VA 22206, USA', '1511 Leslie Ave, Alexandria, VA 22301, USA']
dist = [[0, 12677, 21389, 6104, 12655, 11658, 7991, 13079, 9414, 12080], [12935, 0, 10370, 19937, 1409, 1919, 3626, 2053, 5085, 1805], [21572, 10367, 0, 28573, 11651, 10551, 12838, 8704, 15698, 11848], [4861, 15618, 24330, 0, 15481, 14598, 10937, 16020, 12241, 12697], [11650, 1486, 10361, 14571, 0, 3206, 3772, 2056, 4181, 2540], [11413, 1919, 10558, 18414, 2936, 0, 2984, 1851, 14284, 1994], [8107, 3473, 12872, 14139, 3821, 3232, 0, 4566, 4589, 2067], [13261, 2056, 8702, 20262, 2349, 1851, 4529, 0, 6544, 3539], [8494, 5194, 14501, 11415, 4139, 13980, 4899, 6195, 0, 4681], [10232, 1765, 11734, 16264, 2352, 2907, 2289, 3428, 4686, 0]]
demand = [ 0,10, 12, 16, 14, 12, 10, 17, 18, 12, 8]
capacity = 10000
#capacity = 1925010 #Maximum capacity allowed until vrp fails for 1 route

#optimally split even on nodes closest to depot
match_type = ""
depot_capacity_list = None

#pick first 2 to be the depot_list
depot_list = siteNames[1]#:3]#:2]#4]#:4]#:2]#:2] #:1]

#solve mdvrp
routify,master_sol = mdvrp_solve(siteNames,dist,depot_list,demand,capacity,match_type,depot_capacity_list).run()

#geocode the coords
routes_to_map = geocoder(coords,siteNames,routify).run()
#print routes_to_map
app = Flask(__name__)


@app.route('/')
def my_view():
    #data = [["(38.8191,-77.043)","(38.7968,-77.045)","(38.8048,-77.1244)","(38.8098,-77.0845)"],["(38.8191,-77.043)","(38.8143,-77.0504)","(38.8098,-77.0845)","(38.7266,-77.071)"]]
    #return render_template('index.html', route_data=map(json.dumps, data))
    return render_template('map_view.html', route_data=routes_to_map)
if __name__ == "__main__":
    app.run()
