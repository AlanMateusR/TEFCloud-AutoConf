import os
from html.parser import HTMLParser
import http.client
import json
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import oathtool
import imaplib
import email
import quopri
import re
import requests
import sys
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException
from imap import imap_code
import tkinter
import tkinter.messagebox
import customtkinter
from dotenv import load_dotenv, dotenv_values

# | Configurador automático de pedidos em server cloud |

# Todos os links e senhas foram censuradas no arquivo .env pois são confidenciais da empresa integradora TEF.
# Não é recomendado que tente reproduzir o codigo para qualquer fim, por favor ler o documento README do github.

""" OBTER VARIAVEIS NECESSARIAS """
# Resgatando variaveis .ENV   
load_dotenv()

# Link para requisição portal Gluo
linkGluo = os.getenv("link_crm")

# Link de acesso ao ambiente cloud Software Express
linkSwe = os.getenv("link_swe")

# Usuario e senha de acesso ao ambiente cloud (o script tem seu proprio login e atenticador)
scriptUser = os.getenv("script_user")
scriptPass = os.getenv("script_pass")
# Codigo do gogle authenticator (script tem acesso ao SECRET para efetuar login)
oathtool = os.getenv("oath_secret")

# Link de request para enviar mensagem ao discord da equipe de suporte informando pedido em execução
postDisc = os.getenv("post_discord")
# requisição de envio de mensagem informando termino da execução do pedido
posrtDiscE = os.getenv("post_discond_end")

# Abrir instancia de configuração de numero lógico no ambiente cloud (script tem acesso a todos os modulos)
getConf = os.getenv("get_conf")

# Link de todos os modulos de operadora de cartão no ambiente cloud (para cada operadora de cartão é configurado um numero lógico respectivo ao que contém no pedido de venda do cliente)
get_banrisul = os.getenv("get_banrisul")
get_cielo = os.getenv("get_cielo")
get_rede = os.getenv("get_rede")
get_stone = os.getenv("get_stone")
get_bin = os.getenv("get_bin")
get_sipag = os.getenv("get_sipag")
get_getnetlac = os.getenv("get_getnetlac")
get_pagseguro = os.getenv("get_pagseguro")
get_safra = os.getenv("get_safra")
get_adiq = os.getenv("get_adiq")
get_algorix = os.getenv("get_algorix")
get_comprocard = os.getenv("get_comprocard")
get_tricard = os.getenv("get_tricard")
get_policard = os.getenv("get_policard")
get_valecard = os.getenv("get_valecard")
get_telenet = os.getenv("get_telenet")
get_softnex = os.getenv("get_softnex")
get_vegascard = os.getenv("get_vegascard")
get_conductor = os.getenv("get_conductor")

# Credenciais de acesso IMAP para acessar caixa de entrada do GMAIL (script possui um email proprio onde recebe token de confirmação para as ações efetuadas no ambiente cloud)
imapE = os.getenv("imap_email")
imapP = os.getenv("imap_pass")


# Requisição que envia os logs de execução do codigo para o CRM via API
ApiGluoComent = os.getenv("ApiGluoC")


""" INICIALIZAR PROGRAMA-RPA """

"""VALIDAR SESSAO CRM"""

print("###################### AVISO ####################### \n \n")

print("[ERROS RELATADOS]\n")
print("____PAGSEGURO NAO CONFIGURA BANDEIRA MAESTRO_____\n")

print("########### PROGRAMA EM FASE BETA - POR FAVOR REVISAR OS LOGS ############\n \n")


# Inicializar sessão via API ao CRM para utilizar variavel session em requisições via API 
# Documentação e codigo se encontra em meu github: https://github.com/AlanMateusR/LoginSessaoGluocrm/tree/main

import get_session
get_session.get_session()

# inicia sessão
# armazena variavel em arquivo .txt
with open("session.txt", "r", encoding="utf-8") as arquivo:
    sessions = arquivo.readlines()
    for i, linha in enumerate(sessions):
        if i == 0:
            session = linha

# ##########################________INSERINDO DADOS MANUALMENTE__________######################

# Inicializar instancia de interface grafica CumtomTkinder 
# Resultado do input é armazenado em 'pdvno' refere-se ao numero de pedido de venda do cliente no CRM

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Auto configurar pedido.py")
        self.geometry(f"{400}x{60}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="No. Pedido de Venda:")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Iniciar", command=self.get_entry_value)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def get_entry_value(self):
        global pdvno
        # Obter o valor digitado no CTkEntry
        pdvno = self.entry.get()
        with open("pdvno.txt", "w", encoding="utf-8") as arquivo:
            frases = list()
            frases.append(f"{pdvno}")
            arquivo.writelines(frases)
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()


"""___PEGAR ID SITEF COM BASE NO CRM___"""

conn = http.client.HTTPSConnection(linkGluo)
payload = ''
headers = {}
conn.request("GET",
             f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20cf_2088%20FROM%20SalesOrder%20WHERE%20salesorder_no='{pdvno}';&=",
             payload, headers)
res = conn.getresponse()
data = res.read()

# atribuindo variavel com base no resultado
# obtendo idsitef do pedido (se id sitef nao estiver preenchido no CRM o script deve encerrar)

data_dict = json.loads(data)
idsitef = (data_dict["result"][0]["cf_2088"])

# Não prosseguir se campo IDSITEF no pedido não estiver preenchido.

tam = len(idsitef)

if tam > 1:
    pass
else:
    print("ID SITEF NÃO ESTA PREENCHIDO, ENCERRANDO APLICAÇÃO!!!")
    sys.exit()


""" COLETANDO CNPJ CLIENTE """

# requisição PDVNO
# coletar account_id e armazenar em variavel

#Função para coletar info PEDIDO
def ReqPed(info):
    conn = http.client.HTTPSConnection(linkGluo)
    payload = ''
    headers = {}
    conn.request("GET", f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20*%20FROM%20SalesOrder%20WHERE%20salesorder_no='{pdvno}';", payload, headers)
    res = conn.getresponse()
    data = res.read()

    data_dict = json.loads(data)
    return (data_dict["result"][0][f"{info}"])


#Subprocess coleta de dados ORG
# ORG seria um modulo do CRM chamado "organizações" este modulo resgata dados do estabelecimento do cliente final.
def GetCnpj():
    global cnpj
    #### RETRIEVE ###

    conn = http.client.HTTPSConnection(linkGluo)
    payload = ''
    headers = {}
    conn.request("GET", f"/webservice.php?sessionName={session}&id={id}&operation=retrieve", payload, headers)
    res = conn.getresponse()
    data = res.read()

    data_dict = json.loads(data)
    cnpj = (data_dict["result"]["cpfcnpj"])

# Processando dados coletados via API para efetuar novas requisições
# Utilizar Id do pedido >> retrieve >> org >> cnpj >> var
id = ReqPed("account_id") 
# Chamar subprocesso (cnpj esta em uma global) 
GetCnpj()

# Print CNPJ para teste de variavel
# exibir codigo no terminal para confirmação de cliente.
print(f"CNPJ Pedido: {cnpj}")
print()

# SALVANDO TXT COM CNPJ PRIMEIRA LINHA E ID SITEF SEGUNDA LINHA
# salvar em cache txt

with open("cnpjs.txt", "w", encoding="utf-8") as arquivo:
    frases = list()
    frases.append(f"{cnpj} \n")
    frases.append(idsitef)
    arquivo.writelines(frases)

# ENVIANDO MENSAGEM AO DISCORD de que o pedido em questão foi inicializado
# envia uma mensagem (POST REQUEST) para um servidor da plataforma discord contendo informações a respeito do pedido que será configurado.

r = requests.post(
    postDisc,
    json={
        "username": "EMPRESA",
        "avatar_url": "https://imgur.com/IMAGE.jpg",
        "content": "",
        "embeds": [
            {
                "title": f"Configuração em andamento",
                "color": 65297,
                "description": f"Configuração em andamento, pedido Sitef Nuvem  {cnpj}",
                "timestamp": "",
                "author": {
                    "name": "",
                    "icon_url": ""
                },
                "image": {},
                "thumbnail": {},
                "footer": {
                    "text": f"{pdvno}, Id Sitef: {idsitef}"
                },
                "fields": []
            }
        ],
        "components": []
    })

"""INICIANDO WEBDRIVER"""
# será utilizado biblioteca selenium para efetivar automação e WEBDRIVER MANAGER para controle das instancias de driver do navegador GOOGLE CHROME

servico = Service(ChromeDriverManager().install())

browser = webdriver.Chrome(service=servico)
browser.get(linkSwe)

# Entra e loga no portal
search_box_login = browser.find_element(By.NAME, "username")
search_box_login.send_keys(scriptUser)

search_box_passw = browser.find_element(By.NAME, "password")
search_box_passw.send_keys(scriptPass)
search_box_login.submit()

sleep(2)

# token - OJ4E42BQONJE6NTPJU3TARCFHBHGUVCT

# Validando codigo de login google atenticator

SECRET = oathtool
var = (oathtool.generate_otp(SECRET))

# separando os elementos

var_u = var[0]
var_d = var[1]
var_t = var[2]
var_q = var[3]
var_c = var[4]
var_s = var[5]

# iniciando login
# inserindo dados nos campos para atenticar login

click_primeiro_campo = browser.find_element(By.ID, "camp1")
click_primeiro_campo.send_keys(f'{var_u}')

click_segundo_campo = browser.find_element(By.ID, "camp2")
click_segundo_campo.send_keys(f'{var_d}')

click_terceiro_campo = browser.find_element(By.ID, "camp3")
click_terceiro_campo.send_keys(f'{var_t}')

click_quarto_campo = browser.find_element(By.ID, "camp4")
click_quarto_campo.send_keys(f'{var_q}')

click_quinto_campo = browser.find_element(By.ID, "camp5")
click_quinto_campo.send_keys(f'{var_c}')

click_sexto_campo = browser.find_element(By.ID, "camp6")
click_sexto_campo.send_keys(f'{var_s}')

# clicar no botão login

browser.find_element(By.XPATH, '//*[@id="kc-login"]').click()

sleep(2)

# clica aba configuador
browser.find_element(By.XPATH, '//*[@id="menuConfigurador"]/span').click()
sleep(1)
browser.find_element(By.XPATH, '//*[@id="menuConfiguradorSiTef"]/span/a').click()

# vai pra aba gerada
browser.switch_to.window(browser.window_handles[1])

# aguarda carregar configurador sitef
print("aguardando Sitef carregar configurador, 25 segundos...")
sleep(19)

# Entrar no configurador sitef
browser.get(getConf)
#browser.find_element(By.XPATH, '//*[@id="centro"]/div/ul[1]/li[1]/a').click()

sleep(6)

"""_____VALIDANDO/CONFIGURANDO LÓGICOS_______"""

# INICIALIZANDO COLETA DE DADOS VIA API DO CRM COM BASE NO PDV_NO

conn = http.client.HTTPSConnection(linkGluo)
payload = ''
headers = {}
conn.request("GET",
             f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20adquirentes_html%20FROM%20SalesOrder%20WHERE%20salesorder_no='{pdvno}';&=",
             payload, headers)

res = conn.getresponse()
data = res.read()

data_dict = json.loads(data)
data = (data_dict["result"][0]["adquirentes_html"])

# resultado da requisição vai estar nesse [data]

""" First row is the header, all other rows are data """

# logico com base do pdv_no

class TableParser(HTMLParser):
    header = []
    data = []
    current_data = []
    first_row = True

    def handle_starttag(self, tag, attrs):
        if self.first_row:
            return

        if tag == "tr":
            current_data = []

    def handle_endtag(self, tag):
        if self.first_row and tag == "tr":
            self.first_row = False
            return

        if self.first_row:
            return

        if tag == "tr":
            self.data.append(self.current_data)
            self.current_data = []

    def handle_data(self, data):
        data = data.strip()

        if len(data) == 0:
            return

        if self.first_row:
            self.header.append(data)
        else:
            self.current_data.append(data)


def parse_table(html):
    parser = TableParser()
    parser.feed(html)
    return (parser.header, parser.data)


header, data = parse_table(data)

AutorizadoraPos = header.index('Autorizadora')
CodEstabelecimento = header.index('Código Estabelecimento')
NumLogico = header.index('Número Lógico')

#print(AutorizadoraPos, CodEstabelecimento, NumLogico)

lista = list()
adqPorNome = dict()

for row in data:
    print('Nome autorizadora: ', row[AutorizadoraPos], '; Cod estabelecimento: ', row[CodEstabelecimento],
          '; Num logico: ', row[NumLogico])

    adq = row[AutorizadoraPos]
    numl = row[NumLogico]
    cod = row[CodEstabelecimento]

    lista.append({
        "nomeadq": adq,
        "numllog": numl,
        "codestab": cod
    })

    adqPorNome[adq] = {
        "numllog": numl,
        "codestab": cod
    }

#print(lista)
print()
#print(adqPorNome)

for adqobj in lista:
    adq = adqobj["nomeadq"]
    numl = adqobj["numllog"]
    cod = adqobj["codestab"]

    """DEFINICNDO SUBPROCESS MODULOS SEPARADOS"""

    #ATENCAO TEM QUE VER SE VAI FUNCIONA MAIS DE UM LOGICO E AJUSTAR O PASS

    def Banrisul():
        sleep(5)

        # entra Banrisul
        browser.get(get_banrisul)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(3)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(2)

        # insere cod estabelecimento
        browser.find_element(By.XPATH, '//*[@id="codigorede"]').send_keys(f"{cod}")

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(15)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(3)

        browser.switch_to.alert.accept()

        sleep(5)

        # confirmar alert do navegador
        try:
            browser.switch_to.alert.accept()
            sleep(3)
            pass
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Cielo():
        sleep(6)

        with open("cielo_logico.txt", "r", encoding="utf-8") as arquivo:
            logico = arquivo.readlines()
            for i, linha in enumerate(logico):
                if i == 0:
                    logico = linha

        # avaliando numero lógico Cielo
        primDigito = logico[0]

        #declarando subprocesso para envio de comentario no pedido CASO lógico não comece com 4
        def PrimDigiNotFor():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nNumero lógico da Cielo informado no pedido ({numl}) não começa com 4, provalmente está incorreto\nEncerrando fluxo...É necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)

        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nEncerrando fluxo...É necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)

        if primDigito != '4':
            print(
                f"Numero lógico da Cielo informado no pedido ({numl}) não começa com 4, provalmente está incorreto\nEncerrando fluxo...Será enviado aviso no comentario do pedido.")
            PrimDigiNotFor()
            quit()

        qtd_digitos_numl = len(logico)

        if qtd_digitos_numl == 8:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass

        elif qtd_digitos_numl == 10:
            print(
                f"Verificado que lógico Cielo contém {qtd_digitos_numl} digitos, considera-se que os dois ultimos caracteres são o codigo verificador...\n"
                f"Será providenciado uma nova variavel para ser configurado somente os 8 primeiros digitos do lógico...")

            logico = logico[0] + logico[1] + logico[2] + logico[3] + logico[4] + logico[5] + logico[6] + logico[7]

        else:
            print(
                f"O numero lógico {logico} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Numero lógico tem menos de 8 digitos!!!")
            InvalidDigit()
            quit()

        # Abre configurador cielo
        browser.get(get_cielo)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(4)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="TermLogico"]').send_keys(f"{logico}")
        sleep(4)

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
            pass
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Rede():
        sleep(7)
        print("Módulo REDE será configurado... Verificando se pedido é PROMO REDE...")
        print("ATENÇÃO!!! VERIFICAÇÃO DA FLAG PROMO REDE ADM AINDA NÃO FOI IMPLEMENTADA!!!")
        print()
        # VERIFICANDO SE CLIENTE É PROMO REDE
        conn = http.client.HTTPSConnection(linkGluo)
        payload = ''
        headers = {}
        conn.request("GET",
                     f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20produto_pdv%20FROM%20SalesOrder%20WHERE%20salesorder_no='{pdvno}';",
                     payload, headers)
        res = conn.getresponse()
        data = res.read()
        # print(data.decode("utf-8"))

        print()

        data_dict = json.loads(data)
        produto = (data_dict["result"][0]["produto_pdv"])

        # print(produto)

        # Conferindo se cliente é promo rede

        # print("Conferindo se cliente utiliza PROMO REDE...")

        if produto == "Sitef Nuvem":
            print(f"Cliente não é promo rede, {produto}")
        elif produto == "Sitef Nuvem – Promo REDE":
            print(f"Cliente é promo rede, {produto}")

        # avaliando numero lógico REDE
        qtd_digitos_numl = len(numl)


        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nÉ necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)


        if qtd_digitos_numl == 15:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass
        else:
            print(
                f"O numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Lógico lógico não contém 15 digitos")
            InvalidDigit()
            print("\nAdquirente de grande porte identificada, fluxo será encerrado")
            quit()

                # Abre configurador REDE
        browser.get(get_rede)
        sleep(3)

        # clica Rede
        # browser.find_element(By.XPATH, '//*[@id="dd0"]/div[143]/a[2]').click()

        # clica estabelecimento
        # browser.find_element(By.XPATH, '//*[@id="sd229"]').click()

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(4)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(4)

        """SE PROMO REDE > HABILITAR CHECKBOX"""

        if produto == "Sitef Nuvem – Promo REDE":
            # Checkbox SITEF PROMO REDE
            mouse_over = browser.find_element(By.XPATH, '//*[@id="PromoRede"]').click()
            
            sleep(2)
            
            # clica em salvar
            browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()

            # espera aparecer alert
            sleep(3)

            # vai para alert e confirma + aguarda 4 seg
            browser.switch_to.alert.accept()
            sleep(7)

            # pegar token
            imap_code()
            sleep(5)

            with open("imap.txt", "r", encoding="utf-8") as arquivo:
                emails = arquivo.readlines()
                for i, linha in enumerate(emails):
                    if i == 0:
                        codigo = linha

            # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
            browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

            # CLICA CONFIRMAR
            browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

            sleep(3)
            browser.switch_to.alert.accept()
            sleep(5)

            try:
                browser.switch_to.alert.accept()
                sleep(3)
                pass
            except:
                pass

            pass

        elif produto == "Sitef Nuvem":
            #clica em salvar

            browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()

            sleep(7)
            # pegar token
            imap_code()
            sleep(6)

            with open("imap.txt", "r", encoding="utf-8") as arquivo:
                emails = arquivo.readlines()
                for i, linha in enumerate(emails):
                    if i == 0:
                        codigo = linha

            # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
            browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

            # CLICA CONFIRMAR
            browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

            sleep(3)
            
            browser.switch_to.alert.accept()
            sleep(5)

            try:
                browser.switch_to.alert.accept()
                sleep(3)
                pass
            except:
                pass
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Stone():

        sleep(7)
        # entra stone
        browser.get(get_stone)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(3)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(2)

        # insere cod estabelecimento
        browser.find_element(By.XPATH, '//*[@id="EditCodStone"]').send_keys(f"{cod}")

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
            pass
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass
    
    def BIN():
        sleep(7)

        # entra bin
        browser.get(get_bin)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(3)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="terminalvirtual"]').send_keys(f"{numl}")
        sleep(2)

        # insere cod estabelecimento
        # CONFIRMAR PARAMETRIZAÇÂO
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{cod}")

        # CONFIRMAR PARAMETRIZAÇÂO
        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
            pass
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Sipag():
        # entra Sipag
        browser.get(get_sipag)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(3)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="terminalvirtual"]').send_keys(f"{numl}")
        sleep(2)

        # insere cod estabelecimento
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{cod}")

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
            pass
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def GetNetLac():
        # entra GetNetLac

        with open("getnetlac_logico.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    logico = linha

        # verificando padrao logico getnetlac

        # (1) CODIGO DE ESTAB
        qtd = len(logico)
        print(f'quantidade de digitos do logico: {logico}')

        if qtd == 15:
            print('Código Estabelecimento Getnetlac contém 15 digitos, está no padrão Sitef!')
            pass

        elif qtd == 8:
            print(f'Identificado que logico Getnetlac contém {qtd} digitos, será considerado que faltam 7 zeros á esquerda para lógico ser ajustado...')
            # processar nova variavel para logico Getnetlac
            nova = '0000000' + logico
            print(f'Nova variavel gerada: {nova}\n')
            cod = nova

            

            pass

        else:
            print(f'Lógico Getnetlac contém {qtd} digitos, está fora do padrão Sitef conhecido!!!')   

        """qtdt = len(adq)
        if qtdt == 8:
            print('Logico contem 8 digitos, está no padrão Sitef!!!')
            pass

        else:
            print(f'Lógico Getnetlac contém {qtd} digitos, está fora do padrão Sitef conhecido!!!')  """


        browser.get(get_getnetlac)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(3)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="terminallogico"]').send_keys(f"{numl}")
        sleep(2)

        # insere cod estabelecimento
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{cod}")

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
            pass
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def PagSeguro():
        # avaliando numero lógico pagseguro
        qtd_digitos_numl = len(numl)

        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nÉ necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)


        if qtd_digitos_numl == 15:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass
        else:
            print(
                f"O numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Lógico lógico não contém 15 digitos")
            InvalidDigit()
            print("\nNão é adquirente de grande porte, fluxo não será encerrado")
            pass

        # entra PagSeguro
        browser.get(get_pagseguro)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(4)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(4)

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
        except:
            pass 

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Safra():
        sleep(7)
        
        # entra safra
        browser.get(get_safra)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(3)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="terminallogico"]').send_keys(f"{numl}")
        sleep(2)

        # insere cod estabelecimento
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{cod}")

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
            pass
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def ADIQ():
        sleep(7)

        qtd_digitos_numl = len(numl)

        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nÉ necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)

        if qtd_digitos_numl == 15:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass
        else:
            print(
                f"O numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Lógico lógico não contém 15 digitos")
            InvalidDigit()
            print("\nNão é adquirente de grande porte, fluxo não será encerrado")
            pass

        # entra ADIQ
        browser.get(get_adiq)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(3)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(2)

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
            pass
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Algorix():
        sleep(7)
        
        # avaliando numero lógico Algorix
        qtd_digitos_numl = len(numl)

        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nÉ necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)


        if qtd_digitos_numl == 7:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass
        else:
            print(
                f"O numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Lógico lógico não contém 7 digitos")
            InvalidDigit()
            print("\nNão é adquirente de grande porte, fluxo não será encerrado")
            pass

        # entra Algorix
        browser.get(get_algorix)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(3)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(2)

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
            pass
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Comprocard():
        sleep(7)
        
        # avaliando numero lógico Comprocard
        qtd_digitos_numl = len(numl)

        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nÉ necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)


        if qtd_digitos_numl == 15:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass
        else:
            print(
                f"O numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Lógico lógico não contém 15 digitos")
            InvalidDigit()
            print("\nNão é adquirente de grande porte, fluxo não será encerrado")
            pass

        # entra Comprocard
        browser.get(get_comprocard)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(5)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(2)

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
            pass
        except:
            pass


        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Tricard():
        sleep(7)
        
        # avaliando numero lógico Tricard
        qtd_digitos_numl = len(numl)


        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nÉ necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)


        if qtd_digitos_numl == 15:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass
        else:
            print(
                f"O numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Lógico lógico não contém 15 digitos")
            InvalidDigit()
            print("\nNão é adquirente de grande porte, fluxo não será encerrado")
            pass

        # entra Tricard
        browser.get(get_tricard)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(3)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(2)

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
            pass
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Policard():
        sleep(7)

        # avaliando numero lógico Policard
        qtd_digitos_numl = len(numl)

        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nÉ necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)

        if qtd_digitos_numl == 15:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass
        else:
            print(
                f"O numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Lógico lógico não contém 15 digitos")
            InvalidDigit()
            print("\nNão é adquirente de grande porte, fluxo não será encerrado")
            pass

        # entra Policard
        browser.get(get_policard)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(3)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(2)

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        
        browser.switch_to.alert.accept()
        sleep(3)
        try:
            browser.switch_to.alert.accept()
            sleep(3)
            pass
        except:
            pass


        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Valecard():
        sleep(7)
        # avaliando numero lógico Valecard
        qtd_digitos_numl = len(numl)

        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nÉ necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)

        if qtd_digitos_numl == 8:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass
        else:
            print(
                f"O numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Lógico lógico não contém 8 digitos")
            InvalidDigit()
            print("\nNão é adquirente de grande porte, fluxo não será encerrado")
            pass


        # entra Valecard
        browser.get(get_valecard)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(4)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(4)

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        print("Obs, script ainda não é capaz de integrar com configuração de associação de combustiveis")
        pass

    def Telenet():
        sleep(7)
        # avaliando numero lógico Telenet
        qtd_digitos_numl = len(numl)

        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nÉ necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)

        if qtd_digitos_numl == 15:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass
        else:
            print(
                f"O numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Lógico lógico não contém 15 digitos")
            InvalidDigit()
            print("\nNão é adquirente de grande porte, fluxo não será encerrado")
            pass

        # entra Telenet
        browser.get(get_telenet)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(4)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(4)

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Softnex():
        sleep(7)
        # avaliando numero lógico Softnex
        qtd_digitos_numl = len(numl)
        qtd_digitos_cod = len(cod)

        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nÉ necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)


        if qtd_digitos_numl == 15:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass
        else:
            print(
                f"O numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Lógico lógico não contém 15 digitos")
            InvalidDigit()
            print("\nNão é adquirente de grande porte, fluxo não será encerrado")
            pass

        # entra Softnex
        browser.get(get_softnex)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(4)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(4)

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Vegascard():
        sleep(7)
        # avaliando numero lógico Vegascard
        qtd_digitos_numl = len(numl)

        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nÉ necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)

        if qtd_digitos_numl == 15:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass
        else:
            print(
                f"O numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Lógico lógico não contém 15 digitos")
            InvalidDigit()
            print("\nNão é adquirente de grande porte, fluxo não será encerrado")
            pass

        # entra Vegascard
        browser.get(get_vegascard)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(4)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(4)

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
        except:
            pass

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    def Conductor():
        # avaliando numero lógico Conductor
        qtd_digitos_numl = len(numl)

        def InvalidDigit():
            import http.client
            import json

            ################################### [Pegar id] #######################################3

            conn = http.client.HTTPSConnection(linkGluo)
            payload = ''
            headers = {}
            conn.request("GET",
                         f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM%20SalesOrder%20WHERE%20salesorder_no%20=%20'{pdvno}'%20LIMIT%201;",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()

            # teste retorno da req
            # print(data.decode("utf-8"))

            # criando dicionario
            data_dict = json.loads(data)
            id = (data_dict["result"][0]["id"])

            # Print CNPJ para teste de variavel
            # print(f"ID: {id}\n")

            ################################### [Usar id para req comment] #######################################

            import requests

            url = ApiGluoComent

            payload = {'operation': 'create',
                       'sessionName': session,
                       'elementType': 'ModComments',
                       'element': json.dumps({"assigned_user_id": "19x31", "related_to": id,
                                              "commentcontent": f"<strong>Pedido esta sendo gerenciado por meio de RPA (Robot Programing Automation)</strong>\nO numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.\nÉ necessario revisão."})
                       }
            files = [

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print("Requisição enviada")
            # print(response.text)


        if qtd_digitos_numl == 8:
            print(
                f"O numero lógico solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. ESTÁ DENTRO DO PADRÃO SITEF.")
            pass
        else:
            print(
                f"O numero lógico {numl} solicitado para adquirente {adq} contém {qtd_digitos_numl} digitos. NÃO ESTÁ DENTRO DO PADRÃO SITEF.")
            print(f"Lógico lógico não contém 8 digitos")
            InvalidDigit()
            print("\nNão é adquirente de grande porte, fluxo não será encerrado")
            pass

        # entra conductorp
        browser.get(get_conductor)
        sleep(3)

        # clica scrow
        browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

        # idsitef = input("Digite ID Sitef: ")

        browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
        sleep(4)

        # insere num logico
        browser.find_element(By.XPATH, '//*[@id="EditCodEstab"]').send_keys(f"{numl}")
        sleep(4)

        # clica em salvar
        browser.find_element(By.XPATH, '//*[@id="Salvar"]').click()
        sleep(14)

        # pegar token
        imap_code()
        sleep(4)

        with open("imap.txt", "r", encoding="utf-8") as arquivo:
            emails = arquivo.readlines()
            for i, linha in enumerate(emails):
                if i == 0:
                    codigo = linha

        # INSERE TOKEN PARA CONFIRMAÇÃO DE CONFIGURAÇÃO
        browser.find_element(By.XPATH, '//*[@id="inputToken"]').send_keys(f"{codigo}")

        # CLICA CONFIRMAR
        browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/button[1]/span').click()

        sleep(7)

        browser.switch_to.alert.accept()

        sleep(5)

        try:
            browser.switch_to.alert.accept()
            sleep(3)
        except:
            pass 

        print(f"Inclusão lógico {adq} enfetuado\n")
        pass

    if adq == 'Cielo':
        print("Inicializando configuração CIELO")

        with open("cielo_logico.txt", "w", encoding="utf-8") as arquivo:
                frases = list()
                frases.append(f"{numl}")
                arquivo.writelines(frases)

        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Cielo()

            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break 
  
    elif adq == 'Rede':
        print("Inicializando configuração rede")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Rede()

            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break 
        
    elif adq == 'Stone':
        print("Inicializando configuração stone")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Stone()

            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break 
        
    elif adq == 'BIN':
        print("Inicializando configuração BIN")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                BIN()

            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break 

    elif adq == 'Sipag':
        print("Inicializando configuração Sipag")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Sipag()

            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break 
        
    elif adq == 'Banrisul':
        print("Inicializando configuração Banrisul")

        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                
                Banrisul()

            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break 
    
    elif adq == 'GetNetLac':
        print("Inicializando configuração GetNetLac")

        with open("getnetlac_logico.txt", "w", encoding="utf-8") as arquivo:
                frases = list()
                frases.append(f"{cod}")
                arquivo.writelines(frases)

        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                GetNetLac()

            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                os.remove('getnetlac_logico.txt')
                sleep(1)
                break 
        
    elif adq == 'PagSeguro':
        print("Inicializando configuração PagSeguro")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                PagSeguro()

            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break 

    elif adq == 'Safra':
        print("Inicializando configuração Safra")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Safra()
                
            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break
        
    elif adq == 'ADIQ':
        print("Inicializando configuração ADIQ")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                ADIQ()
                
            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break
        
    elif adq == 'Algorix':
        print("Inicializando configuração Algorix")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Algorix()
                
            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break

    elif adq == 'Comprocard':
        print("Inicializando configuração Comprocard")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Comprocard()
                
            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break

    elif adq == 'Tricard':
        print("Inicializando configuração Tricard")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Tricard()
                
            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break

    elif adq == 'Policard':
        print("Inicializando configuração Policard")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Policard()
                
            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break

    elif adq == 'Valecard':
        print("Inicializando configuração Valecard")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Valecard()
                
            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break

    elif adq == 'Telenet':
        print("Inicializando configuração Telenet")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Telenet()
                
            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break

    elif adq == 'Softnex':
        print("Inicializando configuração Softnex")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Softnex()
                
            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break

    elif adq == 'Vegascard':
        print("Inicializando configuração Vegascard")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Vegascard()
                
            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break

    elif adq == 'Conductor':
        print("Inicializando configuração Conductor")
        while True:
            """SUBPROCESS"""
            # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

            try:
                # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
                #print("Executando módulo lógicos...")
                Conductor()
                
            except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
                print(f"Ocorreu um erro: {e}")
                print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
                sleep(5)  # Aguarda 5 segundos antes de reiniciar
            else:
                # Este bloco é executado se nenhum erro ocorrer
                #print("Código executado com sucesso.")
                 # Sai do loop se não houver erro
                break

browser.quit()

"""_____CONFIGURANDO BANDERIAS_____"""

import BandeiraCargaConf
import time

while True:
    """SUBPROCESS BANDEIRAS E CARGA"""
    # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

    try:
        # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
        #print("Executando módulo lógicos...")
        BandeiraCargaConf.band()

    except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
        print(f"Ocorreu um erro: {e}")
        print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
        time.sleep(5)  # Aguarda 5 segundos antes de reiniciar
    else:
        # Este bloco é executado se nenhum erro ocorrer
        #print("Código executado com sucesso.")
        break  # Sai do loop se não houver erro


"""_____APLICANDO CARGA_____"""

import CargaConfAndLog
#CargaConf.carga()

while True:
    """SUBPROCESS BANDEIRAS E CARGA"""
    # REINICIAR EM CASO DE ERRO (OSB: setar limite de tentativas posteriormente)

    try:
        # executando subprocesso para configuração automatica de BANDEIRAS E LÓGICOS
        #print("Executando módulo lógicos...")
        CargaConfAndLog.carga()

    except (ElementClickInterceptedException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException) as e:
        print(f"Ocorreu um erro: {e}")
        print("Houve erro interno na rotina. Reiniciando o script em 5 segundos...")
        time.sleep(5)  # Aguarda 5 segundos antes de reiniciar
    else:
        # Este bloco é executado se nenhum erro ocorrer
        #print("Código executado com sucesso.")
        break  # Sai do loop se não houver erro

"""limpeza de dados"""
# limpar todos os arquivos locais gerados 

print("Inicializando limpeza do cache...")

os.remove('session.txt')
os.remove('cnpjs.txt')
os.remove('pdvno.txt')
os.remove('imap.txt')

#limpa a caixa de entrada do gmail que o script utiliza para atenticar cada ação no server.

def limpeza_imap():
    # Your email credentials
    email = imapE
    password = imapP
    # Connect to Gmail's IMAP server
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login to your email account
    imap_server.login(email, password)

    # Select the mailbox you want to work with (e.g., "inbox")
    mailbox = "inbox"
    imap_server.select(mailbox)

    # Search for emails you want to delete (you can modify the search criteria)
    # For example, to delete all emails from a specific sender:
    # search_criteria = '(FROM "sender@example.com")'
    search_criteria = 'ALL'
    result, data = imap_server.search(None, search_criteria)

    # Get a list of email IDs to delete
    email_ids = data[0].split()

    # Delete each email by marking it for deletion
    for email_id in email_ids:
        imap_server.store(email_id, '+FLAGS', '\\Deleted')

    # Permanently remove the emails marked for deletion
    imap_server.expunge()

    # Logout and close the connection
    imap_server.logout()

    print("Emails deleted successfully.")

limpeza_imap()

print("limpeza concluida")

"""alterar pedido para implantação"""
# insira o codigo aqui

print("\nFINALIZADO")

r = requests.post(
    posrtDiscE,
    json={
        "username": "empresa",
        "avatar_url": "https://imgur.com/fwwTk2z.jpg",
        "content": "",
        "embeds": [
            {
                "title": f"Configuração concluída {cnpj}",
                "color": 65297,
                "description": f"Adquirente incluída: {adq}",
                "timestamp": "",
                "author": {
                    "name": "",
                    "icon_url": ""
                },
                "image": {},
                "thumbnail": {},
                "footer": {
                    "text": f"Configuração concluida, pedido liberado."
                },
                "fields": []
            }
        ],
        "components": []
    })

