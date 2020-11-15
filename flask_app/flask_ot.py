# -*- coding: utf-8 -*-
'''
Created on 16-02-2018
@author: Gaspar Mora-Navarro
Department of Cartographic Engineering Geodesy and Photogrammetry
Higher Technical School of Geodetic, Cartographic and Topographical Engineering
@email: joamona@cgf.upv.es
'''
#system imports
import sys
import os
import json
import psycopg2
import psycopg2.extensions
#Third part imports
#Import Flask classes
from flask import Flask, session, redirect, url_for, escape, request, render_template

#basedir is /home/desweb/www/apps/desweb/dw/flask_building
#this allow import things from this location. For example the py package
DESWEB_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(DESWEB_DIR)

#will not work in production mode if do not add DESWEB_DIR to sys.path
#pg_building contains the functions building_insert and building_select
#pg_building.py is un the /home/desweb/www/apps/desweb/dw/flask_building/py folder
#/home/desweb/www/apps/desweb/dw/flask_building/py is also a package because has the
#empty __init__.py file
from pyCode2 import mySettings, pg_operations2, authentication, funciones
"""
To run this app in develop mode
export FLASK_DEBUG=1;export FLASK_APP=flask_ot.py;flask run
"""

#starts the flask app
app = Flask(__name__)

#will work with: http://localhost:5000/building_help/
@app.route('/getHelp/')
def getHelp():
    return 'This is helpful'

#will work with: http://localhost:5000
@app.route("/")
def home():
    dSettings=mySettings.dSettings
    
    htmlpage=render_template('index.html',dSettings=dSettings)
    return htmlpage

@app.route("/visor")
def visor():
    dSettings=mySettings.dSettings
    
    htmlpage=render_template('visor.html',dSettings=dSettings)
    return htmlpage

@app.route('/login/', methods=['POST'])
def login():
    #autentication required
    resp_json=authentication.login(session, request)
    return resp_json

    
@app.route("/requestRouting/", methods=['POST'])
def requestRouting():
    if request.method == 'POST':
        print ("Entra en server")
        point1=request.form['point1']
        point2=request.form['point2']
        mode=int(request.form['mode'])
        
        # mode = 2
        conn = psycopg2.connect("dbname=OpenTransport user=postgres password=Kowabunga7XPostgres host=127.0.0.1")
        cur = conn.cursor()
        # cur.execute("select ST_AsGeoJSON(ST_Transform(ways.the_geom,25830)) from pgr_dijkstra ('select gid as id, source, target, abs(cost_s) as cost from ways',{point2},{point1}, false),ways where ways.gid = edge;".format(point1=point1,point2=point2))
        if mode == 1:
            cur.execute("select ST_AsGeoJSON(ST_Transform(ways.the_geom,25830)) "+
            " from pgr_dijkstra ('select gid as id, source, target, "+
            "costperson AS cost from ways',{point2},{point1}, false) as dij, ways where ways.gid = edge;".format(point1=point1,point2=point2))
        if mode == 2:
            cur.execute("select ST_AsGeoJSON(ST_Transform(ways.the_geom,25830)) "+
            " from pgr_dijkstra ('select gid as id, source, target, "+
            "costbike AS cost from ways',{point2},{point1}, false) as dij, ways where ways.gid = edge;".format(point1=point1,point2=point2))
        if mode == 3:
            cur.execute("select ST_AsGeoJSON(ST_Transform(ways.the_geom,25830)) "+
            " from pgr_dijkstra ('select gid as id, source, target, "+
            "costcar AS cost from ways',{point2},{point1}, false) as dij, ways where ways.gid = edge;".format(point1=point1,point2=point2))
        
        a = cur.fetchall()
        print a
        conn.commit()
        cur.close()
        conn.close()
        return json.dumps({"response": a, "Point1": point1, "Point2": point2})   

@app.route("/selectPlacas/", methods=['POST'])
def selectPlacas():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['idSelectPlacas']
        print gid
        nombre_tabla="tabla.placas"
        resp_json=funciones.Select(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json

@app.route("/selectIncidencias/", methods=['POST'])
def selectIncidencias():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['idSelectIncidencias']
        print gid
        nombre_tabla="tabla.incidencias"
        resp_json=funciones.Select(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json
    
@app.route("/selectZonasmetro/", methods=['POST'])
def selectZonasmetro():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['idSelectZonasmetro']
        print gid
        nombre_tabla="tabla.zonas_metro"
        resp_json=funciones.Select(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json
    
@app.route("/insertPlacas/", methods=['POST'])
def insertPlacas():
    if request.method == 'POST':
        print ("Entra en server")
        #motivo=request.form['inputMotivoInsertPlacas']
        #fecha_ini=request.form['inputFechainiInsertPlacas']
        #fecha_fin=request.form['inputFechafinInsertPlacas']
        #zona=request.form['inputZonaInsertPlacas']
        #coordenadas=request.form['inputCoordenadasInsertPlacas']
        motivo=request.form['motivoPlacas']
        fecha_ini=request.form['fechaIniPlacas']
        fecha_fin=request.form['fechaFinPlacas']
        zona=request.form['zonaPlacas']
        coordenadas=request.form['coordenadasPlacas']
        print coordenadas
        nombre_tabla="tabla.placas"
        #json_data = '{"motivo":'+str(motivo)+',"fecha_ini":'+str(fecha_ini)+',"fecha_fin":'+str(fecha_fin)+',"zona":'+str(zona)+',"geom":'+str(coordenadas)+'}'
        json_data = '{"gid":"1","motivo":"'+str(motivo)+'","fecha_ini":"'+str(fecha_ini)+'","fecha_fin":"'+str(fecha_fin)+'","zona":"'+str(zona)+'","geom":"'+str(coordenadas)+'"}'
        print (json_data)
        resp_json=funciones.Insert(nombre_tabla,'LINESTRING',json_data)
        print (resp_json)
        #returned answer to the client. Is a json
        return resp_json
    
@app.route("/insertIncidencias/", methods=['POST'])
def insertIncidencias():
    if request.method == 'POST':
        print ("Entra en server")
        #descripcion=request.form['inputDescripcionInsertIncidencias']
        #fecha=request.form['inputFechaInsertIncidencias']
        #tipo=request.form['inputTipoInsertIncidencias']
        #coordenadas=request.form['inputCoordenadasInsertIncidencias']
        descripcion=request.form['descripcionIncidencias']
        fecha=request.form['fechaIncidencias']
        tipo=request.form['tipoIncidencias']
        coordenadas=request.form['coordenadasIncidencias']
        nombre_tabla="tabla.incidencias"
        #json_data = '{"motivo":'+str(motivo)+',"fecha_ini":'+str(fecha_ini)+',"fecha_fin":'+str(fecha_fin)+',"zona":'+str(zona)+',"geom":'+str(coordenadas)+'}'
        json_data = '{"gid":"1","descripcion":"'+str(descripcion)+'","fecha":"'+str(fecha)+'","tipo":"'+str(tipo)+'","geom":"'+str(coordenadas)+'"}'
        print (json_data)
        resp_json=funciones.Insert(nombre_tabla,'POINT',json_data)
        print (resp_json)
        #returned answer to the client. Is a json
        return resp_json

@app.route("/insertZonasmetro/", methods=['POST'])
def insertZonasmetro():
    if request.method == 'POST':
        print ("Entra en server")
        zona=request.form['inputZonaInsertZonasmetro']
        precio=request.form['inputPrecioInsertZonasmetro']
        coordenadas=request.form['inputCoordenadasInsertZonasmetro']
        nombre_tabla="tabla.zonas_metro"
        #json_data = '{"motivo":'+str(motivo)+',"fecha_ini":'+str(fecha_ini)+',"fecha_fin":'+str(fecha_fin)+',"zona":'+str(zona)+',"geom":'+str(coordenadas)+'}'
        json_data = '{"gid":"1","zona":"'+str(zona)+'","precio":"'+str(precio)+'","geom":"'+str(coordenadas)+'"}'
        print (json_data)
        resp_json=funciones.Insert(nombre_tabla,'POLYGON',json_data)
        print (resp_json)
        #returned answer to the client. Is a json
        return resp_json
    
@app.route("/updatePlacas/", methods=['POST'])
def updatePlacas():
    if request.method == 'POST':
        print ("Entra en server")
        #gid=request.form['inputGidUpdatePlacas']
        #motivo=request.form['inputMotivoUpdatePlacas']
        #fecha_ini=request.form['inputFechainiUpdatePlacas']
        #fecha_fin=request.form['inputFechafinUpdatePlacas']
        #zona=request.form['inputZonaUpdatePlacas']
        #coordenadas=request.form['inputCoordenadasUpdatePlacas']
        gid=request.form['idPlacas']
        gid=gid.split(".",1)[1] 
        motivo=request.form['motivoPlacas']
        fecha_ini=request.form['fechaIniPlacas']
        fecha_fin=request.form['fechaFinPlacas']
        zona=request.form['zonaPlacas']
        coordenadas=request.form['coordenadasPlacas']
        nombre_tabla="tabla.placas"
        #json_data = '{"motivo":'+str(motivo)+',"fecha_ini":'+str(fecha_ini)+',"fecha_fin":'+str(fecha_fin)+',"zona":'+str(zona)+',"geom":'+str(coordenadas)+'}'
        json_data = '{"gid":"'+str(gid)+'","motivo":"'+str(motivo)+'","fecha_ini":"'+str(fecha_ini)+'","fecha_fin":"'+str(fecha_fin)+'","zona":"'+str(zona)+'","geom":"'+str(coordenadas)+'"}'
        print (json_data)
        resp_json=funciones.Update(nombre_tabla,'LINESTRING',json_data)
        print (resp_json)
        #returned answer to the client. Is a json
        return resp_json

@app.route("/updateIncidencias/", methods=['POST'])
def updateIncidencias():
    if request.method == 'POST':
        print ("Entra en server")
        #gid=request.form['inputGidUpdateIncidencias']
        #descripcion=request.form['inputDescripcionInsertIncidencias']
        #fecha=request.form['inputFechaInsertIncidencias']
        #tipo=request.form['inputTipoInsertIncidencias']
        #coordenadas=request.form['inputCoordenadasInsertIncidencias']
        gid=request.form['idIncidencias']
        gid=gid.split(".",1)[1] 
        descripcion=request.form['descripcionIncidencias']
        fecha=request.form['fechaIncidencias']
        tipo=request.form['tipoIncidencias']
        coordenadas=request.form['coordenadasIncidencias']
        nombre_tabla="tabla.incidencias"
        #json_data = '{"motivo":'+str(motivo)+',"fecha_ini":'+str(fecha_ini)+',"fecha_fin":'+str(fecha_fin)+',"zona":'+str(zona)+',"geom":'+str(coordenadas)+'}'
        json_data = '{"gid":"'+str(gid)+'","descripcion":"'+str(descripcion)+'","fecha":"'+str(fecha)+'","tipo":"'+str(tipo)+'","geom":"'+str(coordenadas)+'"}'
        print (json_data)
        resp_json=funciones.Update(nombre_tabla,'POINT',json_data)
        print (resp_json)
        #returned answer to the client. Is a json
        return resp_json
    
@app.route("/updateZonasmetro/", methods=['POST'])
def updateZonasmetro():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['inputGidUpdateZonasmetro']
        zona=request.form['inputZonaUpdateZonasmetro']
        precio=request.form['inputPrecioUpdateZonasmetro']
        coordenadas=request.form['inputCoordenadasUpdateZonasmetro']
        nombre_tabla="tabla.zonas_metro"
        #json_data = '{"motivo":'+str(motivo)+',"fecha_ini":'+str(fecha_ini)+',"fecha_fin":'+str(fecha_fin)+',"zona":'+str(zona)+',"geom":'+str(coordenadas)+'}'
        json_data = '{"gid":"'+str(gid)+'","zona":"'+str(zona)+'","precio":"'+str(precio)+'","geom":"'+str(coordenadas)+'"}'
        print (json_data)
        resp_json=funciones.Update(nombre_tabla,'POLYGON',json_data)
        print (resp_json)
        #returned answer to the client. Is a json
        return resp_json
    
@app.route("/deletePlacas/", methods=['POST'])
def deletePlacas():
    if request.method == 'POST':
        print ("Entra en server")
        #gid=request.form['gidDeletePlacas']
        gid=request.form['idPlacas']
        gid=gid.split(".",1)[1] 
        print gid
        nombre_tabla="tabla.placas"
        resp_json=funciones.Delete(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json

@app.route("/deleteIncidencias/", methods=['POST'])
def deleteIncidencias():
    if request.method == 'POST':
        print ("Entra en server")
        #gid=request.form['gidDeleteIncidencias']
        gid=request.form['idIncidencias']
        gid=gid.split(".",1)[1] 
        print gid
        nombre_tabla="tabla.incidencias"
        resp_json=funciones.Delete(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json
    
@app.route("/deleteZonasmetro/", methods=['POST'])
def deleteZonasmetro():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['gidDeleteZonasmetro']
        print gid
        nombre_tabla="tabla.zonas_metro"
        resp_json=funciones.Delete(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json
    
'''
@app.route("/selectIncidencias/", methods=['POST'])
def selectIncidencias():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['idSelectIncidencias']
        print gid
        nombre_tabla="tabla.incidencias"
        resp_json=funciones.Select(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json
    
@app.route("/selectZonasmetro/", methods=['POST'])
def selectZonasmetro():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['idSelectZonasmetro']
        print gid
        nombre_tabla="tabla.zonas_metro"
        resp_json=funciones.Select(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json
    
    @app.route("/selectPlacas/", methods=['POST'])
def selectPlacas():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['idSelectPlacas']
        print gid
        nombre_tabla="tabla.placas"
        resp_json=funciones.Select(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json

@app.route("/selectIncidencias/", methods=['POST'])
def selectIncidencias():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['idSelectIncidencias']
        print gid
        nombre_tabla="tabla.incidencias"
        resp_json=funciones.Select(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json
    
@app.route("/selectZonasmetro/", methods=['POST'])
def selectZonasmetro():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['idSelectZonasmetro']
        print gid
        nombre_tabla="tabla.zonas_metro"
        resp_json=funciones.Select(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json
    
    @app.route("/selectPlacas/", methods=['POST'])
def selectPlacas():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['idSelectPlacas']
        print gid
        nombre_tabla="tabla.placas"
        resp_json=funciones.Select(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json

@app.route("/selectIncidencias/", methods=['POST'])
def selectIncidencias():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['idSelectIncidencias']
        print gid
        nombre_tabla="tabla.incidencias"
        resp_json=funciones.Select(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json
    
@app.route("/selectZonasmetro/", methods=['POST'])
def selectZonasmetro():
    if request.method == 'POST':
        print ("Entra en server")
        gid=request.form['idSelectZonasmetro']
        print gid
        nombre_tabla="tabla.zonas_metro"
        resp_json=funciones.Select(nombre_tabla,gid)
        #returned answer to the client. Is a json
        return resp_json
 '''
    
#will work with: http://localhost:5000/building_insert/
if __name__ == "__main__":
    app.run(debug=mySettings.PYTHON_DEBUG_MODE)
    
    
    
    
    
    
