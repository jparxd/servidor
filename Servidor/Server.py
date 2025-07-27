import http.server
import socketserver
import urllib.parse
import os

ARQUIVOS_DIR = os.path.abspath('/arquivos')

os.makedirs(ARQUIVOS_DIR, exist_ok=True)
print(f"Diretório de arquivos configurado: {ARQUIVOS_DIR}")

class SimpleHTTPCheckHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)


        if 'arquivo' not in query_params or not query_params['arquivo']:
            self.send_response(400)
            self.send_header('Content-type ','text/plain; charset = utf-8')
            self.end_headers()
            self.wfile.write("Erro: Parâmetro 'arquivo' não fornecido na URL. Use o formato: /?arquivo=nome_do_arquivo.txt".encode('utf-8'))
            return
        
        filename = query_params['arquivo'][0]

        requested_path = os.path.normpath(os.path.join(ARQUIVOS_DIR, filename))


        if not requested_path.startswith(ARQUIVOS_DIR + os.sep):
            self.send_response(403)
            self.send_header('Content-type', 'text/plain;charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Acesso negado: Tentativa de acessar '{filename}' fora do diretório permitido.".encode('utf-8'))
            return
        
        if os.path.exists(requested_path) and os.path.isfile(requested_path):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Sucesso! O arquivo '{filename}' existe na pasta '{ARQUIVOS_DIR}'.".encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Erro: O arquivo '{filename}' NÃO existe na pasta '{ARQUIVOS_DIR}'.".encode('utf-8'))
    
PORT=8000
Handler = SimpleHTTPCheckHandler


if __name__ == '__main__':
    with socketserver.TCPServer(("",PORT),Handler) as httpd:
        print(f"Servidor HTTP pronto e ouvindo na porta{PORT}...")
        print(f"Para testar, acesse em seu navegador ou use o 'Curl':")
        print(f"- Arquivo existente: http://localhost:{PORT}/?arquivo=documento.txt")
        print(f" - Arquivo inexistente: http://localhost:{PORT}/?arquivo=nao_existe.pdf")
        print(f" - Parâmetro ausente: http://localhost:{PORT}/")
        print(f"Pressione Ctrl+C para parar o servidor a qualquer momento.")
        try:

            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n Servidor parado.')
            httpd.shutdown()

