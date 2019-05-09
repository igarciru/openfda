import http.server
import http.client
import socketserver
import json

IP = "localhost"
PORT = 8000
headers = {'User-Agent': 'http-client'}
direccion_openfda="api.fda.gov"
busquedamedicamentos="/drug/label.json?search=active_ingredient:"
busquedaempresas="/drug/label.json?search=openfda.manufacturer_name:"
parametrolistas="/drug/label.json?limit="

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def principal(self):
        html_principal="busqueda.html"
        with open(html_principal) as f:
            pagina_busqueda=f.read()
        return pagina_busqueda

    def do_GET(self):
        if self.path=="/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(self.principal(), "utf-8"))

        elif "searchDrug" in self.path:
            solicitud=self.path.split("=")
            try:
                if solicitud[2]!="":
                    componente=solicitud[1]+"="+solicitud[2]
                else:
                    componente=solicitud[1]+"="+"10"
            except IndexError:
                componente=solicitud[1]+"&limit=10"
            conn = http.client.HTTPSConnection(direccion_openfda)
            conn.request("GET",busquedamedicamentos+componente,None,headers)
            coderespuesta=conn.getresponse()
            print(coderespuesta.status,coderespuesta.reason)
            respuesta_en_json=coderespuesta.read().decode("utf-8")
            conn.close()
            respuesta=json.loads(respuesta_en_json)
            lista=["<ul>A continuacion aparece una lista de los medicamentos con el componente solicitado:</ul>"]
            try:
                respuesta=respuesta["results"]
                for elemento in respuesta:
                    try:
                        lista.append("<li>"+elemento["openfda"]["generic_name"][0]+"</li>")
                    except KeyError:
                        lista.append("<li>Medicamento no encontrado</li>")
            except KeyError:
                lista.append("<li>No se ha podido obtener ningun resultado</li>")
            datos="".join(lista)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(datos,"utf-8"))

        elif "searchCompany" in self.path:
            solicitud=self.path.split("=")
            try:
                if solicitud[2]!="":
                    empresa=solicitud[1]+"="+solicitud[2]
                else:
                    empresa=solicitud[1]+"="+"10"
            except IndexError:
                empresa=solicitud[1]+"&limit=10"
            conn = http.client.HTTPSConnection(direccion_openfda)
            conn.request("GET",busquedaempresas+empresa,None,headers)
            coderespuesta=conn.getresponse()
            print(coderespuesta.status,coderespuesta.reason)
            respuesta_en_json=coderespuesta.read().decode("utf-8")
            conn.close()

            respuesta=json.loads(respuesta_en_json)
            lista=["<ul>A continuacion aparece una lista de los medicamentos de la empresa solicitada:</ul>"]
            try:
                respuesta=respuesta["results"]
                for elemento in respuesta:
                    try:
                        lista.append("<li>"+elemento["openfda"]["generic_name"][0]+"</li>")
                    except KeyError:
                        lista.append("<li>Medicamento no encontrado</li>")
            except KeyError:
                lista.append("<li>No se ha podido obtener ningun resultado</li>")
            datos="".join(lista)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(datos,"utf-8"))

        elif "listDrugs" in self.path:
            solicitud=self.path.split("=")
            limite=solicitud[1]
            conn = http.client.HTTPSConnection(direccion_openfda)
            conn.request("GET",parametrolistas+limite,None,headers)
            coderespuesta=conn.getresponse()
            print(coderespuesta.status,coderespuesta.reason)
            respuesta_en_json=coderespuesta.read().decode("utf-8")
            conn.close()
            respuesta=json.loads(respuesta_en_json)
            lista=["<ul>A continuacion aparece una lista de los medicamentos solicitados:</ul>"]
            try:
                respuesta=respuesta["results"]
                for elemento in respuesta:
                    try:
                        lista.append("<li>"+elemento["openfda"]["generic_name"][0]+"</li>")
                    except KeyError:
                        lista.append("<li>Medicamento no encontrado</li>")
            except KeyError:
                lista.append("<li>Introduzca un limite correcto</li>")
            datos="".join(lista)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(datos,"utf-8"))

        elif "listCompanies" in self.path:
            solicitud=self.path.split("=")
            limite=solicitud[1]
            conn = http.client.HTTPSConnection(direccion_openfda)
            conn.request("GET",parametrolistas+limite,None,headers)
            coderespuesta=conn.getresponse()
            print(coderespuesta.status,coderespuesta.reason)
            respuesta_en_json=coderespuesta.read().decode("utf-8")
            conn.close()
            respuesta=json.loads(respuesta_en_json)
            lista=["<ul>A continuacion aparece una lista de las empresas solicitadas:</ul>"]
            try:
                respuesta=respuesta["results"]
                for elemento in respuesta:
                    try:
                        lista.append("<li>"+elemento["openfda"]["generic_name"][0]+"</li>")
                    except KeyError:
                        lista.append("<li>Empresa no encontrada</li>")
            except KeyError:
                lista.append("<li>Introduzca un limite correcto</li>")
            datos="".join(lista)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(datos,"utf-8"))

        elif "secret" in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', "Basic realm=Acceso no permitido")
            self.end_headers()

        elif "redirect"  in self.path:
            self.send_response(301)
            self.send_header("Location","http://localhost:8000")
            self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("No se ha encontrado el recurso solicitado")
        return ""
socketserver.TCPServer.allow_reuse_address= True
Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer((IP, PORT), Handler)
print("Servidor ejecutándose en el puerto", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass

httpd.server_close()
print("")
print("Server stopped!")

