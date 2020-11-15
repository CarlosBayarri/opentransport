# -*- coding: utf-8 -*-
import os
import sys
import psycopg2
import json
from os.path import exists
from os import makedirs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(BASE_DIR)

import mySettings as settings
from pg_operations2 import pg_operations2
from waterWells import waterWells

user = settings.USER
password = settings.PASSWORD
database = settings.DATABASE
port = settings.PORT
host = settings.HOST

def Select(nom_tabla,gid):
    d_conn=pg_operations2.pg_connect2(database, user, password, host, port)
    if (nom_tabla=='tabla.placas'):
        fields = 'gid,motivo,fecha_ini,fecha_fin,zona,st_asgeojson(geom)'
    elif (nom_tabla=='tabla.incidencias'):
        fields = 'gid,descripcion,fecha,tipo,st_asgeojson(geom)'
    elif (nom_tabla=='tabla.zonas_metro'):
        fields = 'gid,zona,precio,st_asgeojson(geom)'
    else:
        fields = '*'
    res = pg_operations2.pg_select2(d_conn, table_name=nom_tabla, string_fields_to_select=fields, cond_where='where gid=%s', list_val_cond_where=[gid])
    print res
    res = res[0]
    #print (js)    
    pg_operations2.pg_disconnect2(d_conn)
    resp_json=json.dumps({"ok":True, 'data':res, 'message':'Select successful', 'gid':gid})
    print 'Selection: ' + resp_json
    return resp_json

def Insert(nom_tabla,tipo_geom,json_data):
    d_form_data = json.loads(json_data)
    d_form_data['geom']=pg_operations2.transform_coords_ol_to_postgis(coords_geom=d_form_data['geom'])

    d_conn=pg_operations2.pg_connect2(database, user, password, host, port)

    d2=pg_operations2.dict_to_string_fields_and_vector_values2(d=d_form_data, list_fields_to_remove=['gid'],geom_field_name='geom', epsg='25830', geometry_type=tipo_geom, epsg_to_reproject=None)
    print "d2"
    print d2
    list_returning=pg_operations2.pgInsert2(d_conn=d_conn,
    nom_tabla=nom_tabla, d_str=d2,str_fields_returning='gid')
    new_gid=list_returning[0][0]

    pg_operations2.pg_disconnect2(d_conn)

    resp_json=json.dumps({"ok":True, 'data':d_form_data, 'message':'Row inserted', 'new_gid':new_gid})
    print 'insert_building: ' + resp_json
    return resp_json

def Update(nom_tabla,tipo_geom,json_data):
    
    d_form_data = json.loads(json_data)
    gidUpdate = int(d_form_data['gid'])
    print gidUpdate
    d_form_data['geom']=pg_operations2.transform_coords_ol_to_postgis(coords_geom=d_form_data['geom'])

    d_conn=pg_operations2.pg_connect2(database, user, password, host, port)

    d2=pg_operations2.dict_to_string_fields_and_vector_values2(d=d_form_data, list_fields_to_remove=['gid'],geom_field_name='geom', epsg='25830', geometry_type=tipo_geom, epsg_to_reproject=None)

    list_returning=pg_operations2.pg_update2(d_conn=d_conn,
    table_name=nom_tabla, str_field_names=d2['str_field_names'], str_s_values=d2['str_s_values'],
    list_field_values=d2['list_field_values'],cond_where='where gid=%s',list_values_cond_where=[gidUpdate])
    #new_gid=list_returning[0][0]

    pg_operations2.pg_disconnect2(d_conn)

    resp_json=json.dumps({"ok":True, 'data':d_form_data, 'message':'Row updated'})
    print 'Updated: ' + resp_json
    return resp_json

def Delete(nom_tabla,gid):
    d_conn=pg_operations2.pg_connect2(database, user, password, host, port)
    print gid
    pg_operations2.pg_delete2(d_conn, table_name=nom_tabla, cond_where='where gid=%s', list_values_cond_where=[gid])   
    pg_operations2.pg_disconnect2(d_conn)
    resp_json=json.dumps({"ok":True, 'message':'Delete successful', 'deleted gid':gid})
    #print 'Selection: ' + resp_json
    return resp_json


if __name__ == '__main__':

    json_data='{"gid":"3","descripcion":"compgas","fecha":"2018-04-03","tipo":"Otros","geom":"300,300"}'
    nom_tabla = 'tabla.incidencias'
    fields = '*'
    where = 'where gid<=10'  
    tipo_geom = 'POINT' 
    gid = 1
    #Insert(nom_tabla,tipo_geom,json_data)
    #Update(nom_tabla,tipo_geom,json_data)
    Select(nom_tabla, gid)
    #Delete(nom_tabla, gid)
    #print 'Selection: ' + resp_json
    print ("Succes")
    
