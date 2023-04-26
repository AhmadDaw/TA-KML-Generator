from utm import from_latlon as to_utm, to_latlon as to_geo
from numpy import cos, sin, pi
from simplekml import Kml
import numpy as np 

def define_zone(x,y):
    """
    define the utm zone and the up/down parameters
    :param x: x coordinates
    :param y: y coordinates
    :return: new up/down & utm-zone fields
    """
    updown, zone = [], []
    for i in range(len(x)):
        updown.append('U') if y[i]>0 else updown.append('D')
        zone.append(31+int(x[i]//6))
    return updown,zone

def data_preparation(data, x_field, y_field):
    """
    define utm & updown fields and convert the x/y coordinates to utm
    :param data: the input pandas dataframe
    :param x_field: x array name
    :param y_field: y array name
    """
    x, y = data[x_field], data[y_field]
    data['up_down'], data['utm_zone'] = define_zone(x, y)
    x_utm, y_utm = [], []
    for i in range(len(x)):
        x_, y_ = to_utm(y[i], x[i], data['utm_zone'][i], data['up_down'][i])[:2]
        y_utm.append(y_)
        x_utm.append(x_)
    data['x_utm'], data['y_utm'] = x_utm, y_utm
    #print(data.head())

def find_edge_xy(x,y,z,u,r=0,d=0):

    x_new = x + (d*cos(r))
    y_new = y + (d*sin(r))
    return to_geo(x_new, y_new, z, u)[:2][::-1]

def arc_calculator(data, distance, angle, std, points):

    x, y, u, z = data['x_utm'], data['y_utm'], data['up_down'], data['utm_zone']
    a, s, d, polygons = data[angle], data[std], data[distance], []
    for i in range(len(x)):
        sd = min(180, s[i])
        origin = find_edge_xy(x[i], y[i], z[i], u[i])
        add, tip, arc = (2*sd)/(max(points,2)-1), (180-a[i]+270)-sd, []
        for p in range(points):
            r = ((tip + (p*add)) % 360 * pi) / 180
            arc.append(find_edge_xy(x[i],y[i],z[i],u[i],r,d[i]))
        polygons.append([origin]+arc+[origin])
    data['POLYGON'] = polygons
    #print(data.head())

def create_kml(data,output,names,g):
    if g==2:
        lenx=40
    if g==3:
        lenx=12
    if g==4:
        lenx=8
    
    d_ind=0

    xx=0
    names = list(range(data.shape[0])) if names==None else data[names]
    cells_list=data['name'].unique()
    print(cells_list)
    #lenx=len(data[data['name'==cells_list[0]]])
    print(lenx)
    poly = data['POLYGON']
    file = Kml()
    for p in range(len(poly)):
        if (xx%lenx==0 or xx==0):
            folder = file.newfolder(name=data.loc[data.index[d_ind],'name'])
        samp=data.loc[data.index[d_ind],'Samples']

        des=data.loc[data.index[d_ind],'TA Percent %']
        per_acc=data.loc[data.index[d_ind],'TA Acc. Percent %']
        ecno=data.loc[data.index[d_ind],'ECNO']
        ecno_int=ecno
        rscp=data.loc[data.index[d_ind],'RSCP']
        per_acc = round(per_acc, 2)
        if per_acc > 100:
            per_acc=100
        #desx=des[:-1]
        if des!=np.NaN:
            des=float(des)
            per=des
            des=int(des)
        des=round(des)
        desx=des
        distan=data.loc[data.index[d_ind],'dis']
        des='TA Percent: '+ str(des)+'%'+'\n TA Acc. Percent: '+ str(per_acc) +'%'+'\n TA Samples: '+ str(samp)+'\n Distance: '+ str(distan)+' m'+'\n EcNo: '+ str(ecno)+' dB'+'\n RSCP: '+ str(rscp)+' dBm'
        single = folder.newpolygon(name=str(names[p]),description=des ,outerboundaryis=poly[p])
        if (ecno_int < -14 and desx >= 5):
            single.style.polystyle.color = '64140078' # red

        else:
            single.style.polystyle.color = '6400E614' # light green  

        d_ind=d_ind+1
        xx=xx+1
    file.save(output+'.kml')
# 64F00A14 64F07800 643C8214 6400E614 6414F046 64B478F0 6414F0BE 6414F0FF 6414B4FF 641478FF 64143CFF 64140078 
def create_sector_3g(data,x_field,y_field,angle,distance,std,g,points=36,name=None,output=None):

    data_preparation(data, x_field, y_field)
    arc_calculator(data, distance, angle, std, points)
    if output!=None: create_kml(data, output, name,g)



 # red 641478FF
 # light yellow 6414F0BE
 # blue 64F00A14
 # light green 640EBB54
 # light blue 64C2B140