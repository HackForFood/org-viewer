#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web, unirest,os,sys
reload(sys)
sys.setdefaultencoding("utf8")
rutas = (
   '/banco/(.*)', 'banco',
   '/listabancos', 'listaBancos',
   '/updateroute/', 'actualiza'
	)

app = web.application(rutas, globals())
banks = unirest.get("http://46.101.179.35/banco-alimentos").body
class banco:
	def GET(self,idBanco):
		datosDelBanco = self.obtenerBanco(idBanco)
		if datosDelBanco == -1:
			return "<h1> EL BANCO NO EXISTE</H1>"
		else:
			return """
		   <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
			<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es" lang="es">
			<head>
			<LINK REL=StyleSheet HREF="../static/main.css" TYPE="text/css" >
			<script src="../static/js/OpenLayers.js"></script>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
			<title>%s</title>
			</head>
			<body>
			<h1>%s</h1>
			<p>
			%s 
			</p> 
			<h2>%s</h2>
			%s
			%s

			</body>
			</html>
			""" % (datosDelBanco.get('nombre'),datosDelBanco.get('nombre'),datosDelBanco.get('descripcion'),datosDelBanco.get('localizacion'),self.mapaHTML(idBanco),self.obtenerNecesidadesBancoHTML(idBanco))
	def obtenerBanco(self,idBanco):
		salida = -1
		for banco in banks:
			if banco.get('id') == str(idBanco):
				salida = banco
		return salida
	def obtenerNecesidadesBancoHTML(self,idBanco):
		necesidades = unirest.get("http://46.101.179.35/demandas?esNecesario=true").body
		html="""<div id="tablaRecursos">
				<H1>Recursos necesarios</H1>
				<ul>
				"""
		for necesidad in necesidades:
			if(necesidad.get("idBancoAlimentos") == idBanco):
				html = html + "<li>"+ str(necesidad.get("demanda")) +"</li>"
		html = html + "</ul>"
		return html
	def mapaHTML(self,idBanco):
		datosDelBanco = self.obtenerBanco(idBanco)
		html="""
			<div id="Map"></div>
				
				<script>
					var lat            = %s;
					var lon            = %s;
					var zoom           = 18;
				 
					var fromProjection = new OpenLayers.Projection("EPSG:4326");   // Transform from WGS 1984
					var toProjection   = new OpenLayers.Projection("EPSG:900913"); // to Spherical Mercator Projection
					var position       = new OpenLayers.LonLat(lon, lat).transform( fromProjection, toProjection);
				 
					map = new OpenLayers.Map("Map");
					var mapnik         = new OpenLayers.Layer.OSM();
					map.addLayer(mapnik);
				 
					var markers = new OpenLayers.Layer.Markers( "%s" );
					map.addLayer(markers);
					markers.addMarker(new OpenLayers.Marker(position));
				 
					map.setCenter(position, zoom);
				</script> 
				<a href="http://www.openstreetmap.org/?mlat=%s&mlon=%s" target="_blank">Ver mapa en grande</a>
			""" % (datosDelBanco.get('lon'),datosDelBanco.get('lat'),datosDelBanco.get('nombre'),datosDelBanco.get('lon'),datosDelBanco.get('lat'))
		return html
class actualiza:
	def GET(self):
		global banks
		banks = unirest.get("http://46.101.179.35/banco-alimentos").body
		return ""
		
class listaBancos:
	def GET(self):
		global banks
		banks = unirest.get("http://46.101.179.35/banco-alimentos").body
		html = """<HEAD></HEAD>
				<BODY><H1>Lista de Bancos</H1>"""
		for banco in banks:
			html= html +"""
						 <a href="../banco/%s">%s</a> 
						 """%(banco.get("id"),banco.get("nombre"))
			html = html +"""
							</BODY>
						"""
		return html
					
	

if __name__ == '__main__':
	app.run()
