def get_session():
   import hashlib
   import json
   import http.client
   import os
   from dotenv import load_dotenv, dotenv_values
   import mimetypes
   from codecs import encode

   # Carregando ENV
   # por favor preencha os dados do .env com as proprias credenciais ou altere as variaveis do codigo (linkGluo/user/KeySession).
   
   # Documentação e codigo se encontra em meu github: https://github.com/AlanMateusR/LoginSessaoGluocrm/tree/main

   load_dotenv()

   """AUTENTICAÇÃO PARTE 1 """

   # METODO GET/ GETCHALLENGE
   
   """ OBTER VARIAVEIS NECESSARIAS """
   # Resgatando variaveis .ENV   

   # linkGluo para requisição portal Gluo (concedido pelo suporte Gluo)
   linkGluo = os.getenv("linkGluo_crm")
   
   # Nome de usuario para login (consultar perfil do gluo)
   UserSession = os.getenv("UserSession")

   # Chave de acesso Gluo (concedido pelo suporte Gluo)
   KeySession = os.getenv("KeySession")

   # GET / CHALLENGE - obter token de acesso

   conn = http.client.HTTPSConnection(linkGluo)
   payload = ''
   headers = {}
   conn.request("GET", f"/webservice.php?operation=getchallenge&username={UserSession}", payload, headers)
   res = conn.getresponse()
   data = res.read()

   # Resgatando dados (TOKEN) obtido do resultado da requisição (data dict)

   data_dict_1 = json.loads(data)
   tokena = (data_dict_1["result"]["token"])

   # Somando TOKEN obtido com ACCESKeySession -> token + acess KeySession --> md5 encode
   two = (tokena + KeySession)

   # gerando codigo e passando para md5
   str2hash = f"{two}"

   # obtendo MD5 
   result = hashlib.md5(str2hash.encode())

   # montando chave final
   KeySession = (result.hexdigest())

   """Enviar Chave final com metodo / POST e obter sessão"""

   # enviando chaves de requisição + metodo post

   conn = http.client.HTTPSConnection(linkGluo)
   dataList = []
   boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
   dataList.append(encode('--' + boundary))
   dataList.append(encode('Content-Disposition: form-data; name=operation;'))

   dataList.append(encode('Content-Type: {}'.format('text/plain')))
   dataList.append(encode(''))

   dataList.append(encode("login"))
   dataList.append(encode('--' + boundary))
   dataList.append(encode('Content-Disposition: form-data; name=username;'))

   dataList.append(encode('Content-Type: {}'.format('text/plain')))
   dataList.append(encode(''))

   dataList.append(encode("portal"))
   dataList.append(encode('--' + boundary))
   dataList.append(encode('Content-Disposition: form-data; name=accessKeySession;'))

   dataList.append(encode('Content-Type: {}'.format('text/plain')))
   dataList.append(encode(''))

   dataList.append(encode(f"{KeySession}"))
   dataList.append(encode('--' + boundary + '--'))
   dataList.append(encode(''))
   body = b'\r\n'.join(dataList)
   payload = body
   headers = {
      'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
   }
   conn.request("POST", "/webservice.php", payload, headers)
   res = conn.getresponse()
   data_s = res.read()

   # Resgatando dado para variavel (str)

   data_dict_2 = json.loads(data_s)
   session = (data_dict_2["result"]["sessionName"])
   print(f"sessão iniciada: {session}")

   # salvando .txt com sessao inicializada

   with open("session.txt", "w", encoding="utf-8") as arquivo:
      frases = list()
      frases.append(f"{session}")
      arquivo.writelines(frases)
