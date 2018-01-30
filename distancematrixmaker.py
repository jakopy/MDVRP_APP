###################################################################
#                    Scrape Complete, distance matrix google api
###################################################################

import urllib
import simplejson
import ssl


class matrixmaker():
    def __init__(self,locations):
        self.locations = locations
    def matrix(self):
        ssl._create_default_https_context = ssl._create_unverified_context
	    #YOUR_API_KEY= "PLEASE PLACE YOUR GOOGLE API KEY HERE"
        loc = self.locations
        
        #make request
        urlstring = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+loc+"&destinations="+loc+"&sensor=false&units=imperial"

        #"&key="+YOUR_API_KEY
        #c = urlstring[0:len(urlstring)-12] # +myapikey
	#print c

        a = simplejson.load(urllib.urlopen(urlstring))
        #print a
        times = []
        distances = []
        origins = []
        destinations = []
        #print a

        for i in a:
            if i == 'origin_addresses':
                for i in a[i]:
                    origins.append(i)
            if i == 'destination_addresses':
                for i in a[i]:
                    destinations.append(i)
            if i == "rows":
                rows = a[i]
                for i in rows:
                    elements = i
                    for i in elements:
                        duration = elements[i]
                        for i in duration:
                            distance = i
                            for i in distance:
                                if i == "distance":
                                    distances.append(distance[i])
                                if i == "duration":
                                    times.append(distance[i])
        distancedic = {}
        timedic = {}
        alldest = len(origins)
        routinglist = []
        #origin1->dest1->dest2 origin hold
        for i in range(0,len(origins),1):
            for j in range(0,len(destinations),1):
                routinglist.append(origins[i] + '!!!' + destinations[j])


        ############
        #OLD FORMAT
        ###############
        #goal place1:{place1:0},{place2:4}
        #distancematrix formater

        incompletedistancematrix = {}
        count = 0        
        for i in distances:
            distance = i['value']                
            routes = routinglist[count]
            origin = str(routes.split('!!!')[0])
            destination = str(routes.split('!!!')[1])
            if origin not in incompletedistancematrix.keys():
                incompletedistancematrix[origin]={destination:distance}
            else:
                incompletedistancematrix[origin][destination]=distance
            count+=1
        IDC = incompletedistancematrix
        distancematrix = IDC

        #############
        #NEW FORMAT
        ##############
        #goal: [[d1,d2,d3],[d1,d2,d3],[d1,d2,d3]]
        distance_list = []
        indexer = 0
        counter = 0
        for i in distances:
            dist = i['value']
            if indexer == len(origins):
                indexer = 0
                counter += 1
            if indexer == 0:
                distance_list.append([])            
            distance_list[counter].append(dist)
            indexer += 1


        return origins, distance_list #, distancematrix

if __name__ == "__main__":
    coords = "38.888665,-77.076817|38.811768,-77.054556|38.731186,-77.056399|38.891624,-77.101873|38.807791,-77.063039|38.81696,-77.042368|38.835419,-77.053051|38.800536,-77.045838|38.834099,-77.092047|38.820301,-77.052691"
    location_names, distancematrix = matrixmaker(coords).matrix()

    lat_lon = coords.split("|")
    address_coords = {}
    counter = 0
    for address in location_names:
        address_coords[address] = lat_lon[counter]
        counter += 1
    print "ADDRESS COORDS"
    print "-------------------"
    print address_coords
    print "distance List"
    print "-------------------"
    print distance_list
    print "distance matrix"
    print "--------------------"
    print distancematrix
