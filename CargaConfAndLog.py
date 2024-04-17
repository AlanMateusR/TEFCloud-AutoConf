"""_____APLICANDO CARGA_____"""

def carga():
    
    import http.client
    import json
    from selenium import webdriver
    from time import sleep
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    import oathtool
    from html.parser import HTMLParser
    import requests
    import os
    from dotenv import load_dotenv, dotenv_values
    """ OBTER VARIAVEIS NECESSARIAS """
    # Resgatando variaveis .ENV   
    load_dotenv()

    # Link para requisição portal Gluo
    linkGluo = os.getenv("link_crm")

    # Link de acesso ao ambiente cloud Software Express
    linkSwe = os.getenv("link_swe")

    # Abrir instancia de aplicação de carga de tabelas no ambiente cloud
    getCarga = os.getenv("get_carga")

    # Usuario e senha de acesso ao ambiente cloud (o script tem seu proprio login e atenticador)
    scriptUser = os.getenv("script_user")
    scriptPass = os.getenv("script_pass")
    # Codigo do gogle authenticator (script tem acesso ao SECRET para efetuar login)
    oathtool = os.getenv("oath_secret")

    # É buscado pelo script os logs das açoes efetuadas no server (as informações serão enviada para o CRM)
    LinkLogSWE = os.getenv("LinkLogSWE")
    
    # Requisição que envia os logs de execução do codigo para o CRM via API
    ApiGluoComent = os.getenv("ApiGluoC")

    #######################################################################################################

    print("Iniciando aplicação de carga de tabelas SITEF\n")

    # valida sessao CRM
    with open("session.txt", "r", encoding="utf-8") as arquivo:
        cnpjs = arquivo.readlines()
        for i, linha in enumerate(cnpjs):
            if i == 0:
                session = linha

    # le num pdv escrito no txt
    with open("pdvno.txt", "r", encoding="utf-8") as arquivo:
        cnpjs = arquivo.readlines()
        for i, linha in enumerate(cnpjs):
            if i == 0:
                p1 = linha

    # ARMAZENA VARIAVEL DA PRIMEIRA LINHA DO TXT
    pdvno = p1

    # le num pdv escrito no txt
    with open("cnpjs.txt", "r", encoding="utf-8") as arquivo:
        id = arquivo.readlines()
        for i, linha in enumerate(id):
            if i == 1:
                idsitef = linha

    """INICIANDO WEBDRIVER"""

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

    sleep(3)

    # clica aba configuador
    mouse_over = browser.find_element(By.XPATH, '//*[@id="menuConfigurador"]/span').click()
    sleep(1)
    over_click = browser.find_element(By.XPATH, '//*[@id="menuConfiguradorSiTef"]/span/a').click()

    # vai pra aba gerada
    browser.switch_to.window(browser.window_handles[1])

    # aguarda carregar configurador sitef
    print("aguardando Sitef carregar configurador, 25 segundos...")
    sleep(25)

    print("Iniciando aplicação de carga de tabelas no modulos do pedido, time sleep de 14 segundos...")
    sleep(14)

    # abre carga
    browser.get(getCarga)

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

    # resultado da req vai estar nesse [data]

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

    # print(AutorizadoraPos, CodEstabelecimento, NumLogico)

    lista = list()
    adqPorNome = dict()

    for row in data:
        """print('Nome autorizadora: ', row[AutorizadoraPos], '; Cod estabelecimento: ', row[CodEstabelecimento],
                '; Num logico: ', row[NumLogico])"""

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
    #print()
    #print(adqPorNome)

    # CARGA APLICADA 0
    var = 0
    print(f'Fixado valor a VAR: {var}')

    for adqobj in lista:
        adq = adqobj["nomeadq"]
        numl = adqobj["numllog"]
        cod = adqobj["codestab"]
            

        if adq == 'Cielo':
            print("Aplicando carga de tabelas CIELO")
            # clica Cielo
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[21]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd22"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # dar ok no alert msg
                sleep(5)
                browser.switch_to.alert.accept()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print("Esta é a primeira carga")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga 
            else:
                print("Esta é uma carga consecutiva")
                pass


            ### segue ###

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada
            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")
            
            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')
                              
            pass

        elif adq == 'Rede':
            print("Aplicando carga de tabelas REDE")
            # clica Rede
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[57]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd58"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print("Esta é a primeira carga")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga 
            else:
                print("Esta é uma carga consecutiva")
                pass

            ### segue ###

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada
            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")
            
            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')

            pass

        elif adq == 'Stone':
            print("Aplicando carga de tabelas STONE")
            # clica Stone
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[79]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd80"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print("Esta é a primeira carga")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga 
            else:
                print("Esta é uma carga consecutiva")
                pass

            ### segue ###

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada
            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")
            
            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')

            pass

        elif adq == 'BIN':
            print("Aplicando carga de tabelas BIN")
            # clica BIN
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[9]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd10"]').click()

            # espera carregar
            sleep(7)
            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print("Esta é a primeira carga")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga 
            else:
                print("Esta é uma carga consecutiva")
                pass

            ### segue ###

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")

            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')

            pass

        elif adq == 'Sipag':
            print("Aplicando carga de tabelas Sipag")
            # clica Sipag
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[67]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd68"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print("Esta é a primeira carga")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga 
            else:
                print("Esta é uma carga consecutiva")
                pass

            ### segue ###

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")
            
            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')

            pass
            
        elif adq == 'PagSeguro':

            print("Aplicando carga de tabelas PagSeguro")

            # clica PagSeguro
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[53]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd54"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print(f"Esta é a primeira cargan\nVar: {var}")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga 
            else:
                print(f"Esta é uma carga consecutiva\nVar: {var}")
                pass

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")

            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.

            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')
            print(f"Adicionado valor a VAR: {var}")
            pass

        elif adq == 'GetNetLac':
            print("Aplicando carga de tabelas GetNetLac")
            # clica getnetlac
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[35]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd36"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print("Esta é a primeira carga")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga 
            else:
                print("Esta é uma carga consecutiva")
                pass

            ### segue ###

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")
            
            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')

            pass

        elif adq == 'Safra':
            print("Aplicando carga de tabelas safra")
            # clica safra
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[63]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd64"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print("Esta é a primeira carga")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga 
            else:
                print("Esta é uma carga consecutiva")
                pass

            ### segue ###

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")
            
            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')

            pass

        elif adq == 'ADIQ':
            print("Aplicando carga de tabelas ADIQ")
            # clica ADIQ
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[1]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd2"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print("Esta é a primeira carga")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga 
            else:
                print("Esta é uma carga consecutiva")
                pass

            ### segue ###

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")
            
            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')

            pass    

        elif adq == 'Algorix':
            print("Aplicando carga de tabelas Algorix")
            # clica Algorix
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[3]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd4"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print("Esta é a primeira carga")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga 
            else:
                print("Esta é uma carga consecutiva")
                pass

            ### segue ###

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")
            
            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')

            pass    

        elif adq == 'Tricard':
            print("Aplicando carga de tabelas Tricard")
            # clica Tricard
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[85]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd86"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print("Esta é a primeira carga")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga 
            else:
                print("Esta é uma carga consecutiva")
                pass

            ### segue ###

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")
            
            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')

            pass    

        elif adq == 'Policard':
            print("Aplicando carga de tabelas Policard")
            # clica Policard
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[55]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd56"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print(f"Esta é a primeira carga\nVar: {var}")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga
            else:
                print(f"Esta é uma carga consecutiva\nVar: {var}")
                pass
            # marca carga de tabelas para o idsitef em questão
            elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")

            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')
            print(f'Adicionado valor a Var: {var}')
            pass

        elif adq == 'Valecard':
            print("Aplicando carga de tabelas Valecard")
            # clica Policard
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[89]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd90"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print(f"Esta é a primeira carga\nVar: {var}")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga
            else:
                print(f"Esta é uma carga consecutiva\nVar: {var}")
                pass
            # marca carga de tabelas para o idsitef em questão
            elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")

            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')
            print(f'Adicionado valor a Var: {var}')
            pass

        elif adq == 'Telenet':
            print("Aplicando carga de tabelas Telenet")
            # clica Policard
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[83]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd84"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print(f"Esta é a primeira carga\nVar: {var}")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga
            else:
                print(f"Esta é uma carga consecutiva\nVar: {var}")
                pass
            # marca carga de tabelas para o idsitef em questão
            elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")

            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')
            print(f'Adicionado valor a Var: {var}')
            pass

        elif adq == 'Softnex':
            print("Aplicando carga de tabelas Softnex")
            # clica Policard
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[71]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd72"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print(f"Esta é a primeira carga\nVar: {var}")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga
            else:
                print(f"Esta é uma carga consecutiva\nVar: {var}")
                pass
            # marca carga de tabelas para o idsitef em questão
            elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")

            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')
            print(f'Adicionado valor a Var: {var}')
            pass

        elif adq == 'Vegascard':
            print("Aplicando carga de tabelas Vegascard")
            # clica Policard
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[91]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd92"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print(f"Esta é a primeira carga\nVar: {var}")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga
            else:
                print(f"Esta é uma carga consecutiva\nVar: {var}")
                pass
            # marca carga de tabelas para o idsitef em questão
            elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")

            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')
            print(f'Adicionado valor a Var: {var}')
            pass

        elif adq == 'Conductor':
            print("Aplicando carga de tabelas Conductor")
            # clica Conductor
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[23]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd24"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print(f"Esta é a primeira carga\nVar: {var}")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga
            else:
                print(f"Esta é uma carga consecutiva\nVar: {var}")
                pass
            # marca carga de tabelas para o idsitef em questão
            elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")

            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')
            print(f'Adicionado valor a Var: {var}')
            pass

        elif adq == 'Banrisul':
            # clica Banrisul
            browser.find_element(By.XPATH, '//*[@id="dd0"]/div[93]/a[2]').click()

            # clica carga
            browser.find_element(By.XPATH, '//*[@id="sd94"]').click()

            # espera carregar
            sleep(7)

            # Subprocess para caso não tenha sido aplicado carga ainda (var = 0)
            def primeiracarga():
                # DESMARCAR PRIMEIRA LOJA   
                browser.find_element(By.XPATH, '//*[@id="TImagem_00000282"]').click()

                # marca carga de tabelas para o idsitef em questão
                elemento_idsitef = '//*[@id="TDImagem_{}"]'.format(idsitef)

                browser.find_element(By.XPATH, f"{elemento_idsitef}").click()

            # Primeira carga, deve-se desmarcar id padrao e marcar o id sitef do pedido.
            if var == 0:
                print("Esta é a primeira carga")
                primeiracarga()
                pass

            # Carga consecutiva, deve-se considerar que já foi aplicado carga 
            else:
                print("Esta é uma carga consecutiva")
                pass

            ### segue ###

            # enviar

            browser.find_element(By.XPATH, '//*[@id="btnenviar"]/div').click()

            # aguarda carga ser enviada

            print("Aguardando carregamento da carga, 20 segundos...")
            sleep(20)

            # pegar resposta (tem que ser especificamente o elemento com o idsitef)

            elemento_status = '//*[@id="EmprResposta_{}"]'.format(idsitef)

            resposta = browser.find_element(By.XPATH, f"{elemento_status}").text

            print(f"Status da carga: {resposta}")
            
            # Ao final de toda execução de carga será acrescentado +1 valor a variavel var para garantir que ao passar para o proximo modulo apenas deverá clicar em enviar.
            if resposta == 'OK.':
                sleep(5)
                var += 1
                print(f'Novo valor fixado valor a VAR: {var}')
            elif resposta == '???Ha carga de tabelas em andamento.???': 
                print("???Ha carga de tabelas em andamento.???")
                sleep(3)
                
            elif resposta == '???Transacao em andamento???': 
                print("\n??????Transacao em andamento???\n")
                sleep(3)
            else:
                var = 0
                print(f'Novo valor fixado valor a VAR: {var}')
            pass

    #browser.quit()
    print("\nCarga de tabelas concluidas.")

    # time sleep
    sleep(5)

    # abre eventos
    browser.get(LinkLogSWE)

    sleep(6)

    # clica Log
    browser.find_element(By.XPATH, '//*[@id="sd1"]').click()

    sleep(4)

    # clica scrow
    browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()

    browser.find_element(By.XPATH, '//*[@id="ComboEmp"]/option[@value=\'' + idsitef + '\']').click()
    sleep(4)

    # clica em pesquisar
    browser.find_element(By.XPATH, '//*[@id="Listar"]/div').click()
    sleep(8)

    # grava elemento body dos logs
    log = browser.find_element(By.XPATH, '//*[@id="TabelaLog"]/tbody').text

    with open("log.txt", "w", encoding="utf-8") as arquivo:
        frases = list()
        frases.append(f"{log}")
        arquivo.writelines(frases)

    # declarando subprocesso para enviar log
    def Log():
        print("Enviando logs")
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
                   'element': json.dumps({"assigned_user_id": "19x31", "related_to": id, "commentcontent": log})
                   }
        files = [

        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print("Requisição enviada")
        # print(response.text)

    # Enviando Log antes de validar condições de alteração de status
    Log()

     # declarando subprocesso para alterar status do pedido sendo executado para implantação.
    def req_status():

        conn = http.client.HTTPSConnection(linkGluo)

        conn.request("GET",
                     f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20id%20FROM"
                     f"%20SalesOrder%20WHERE%20salesorder_no%3D'{pdvno}'%3B")

        res = conn.getresponse()
        data = res.read()

        # print(data.decode("utf-8"))

        # # organiza dados json
        data_dict_1 = json.loads(data)
        # declara id a partir do json
        id_element = (data_dict_1["result"][0]["id"])

        # print(id_element)

        # print()

        operation_1 = "revise"
        session_1 = f"{session}"
        element_type_1 = "SalesOrder"
        ajx_1 = "DETAILVIEW"
        sostatus_1 = "Implantação"

        url = ApiGluoComent

        payload = {'operation': operation_1,
                   'sessionName': session_1,
                   'elementType': element_type_1,
                   'ajxaction': ajx_1,
                   'element': json.dumps({"salesorder_no": pdvno, "sostatus": sostatus_1, "id": id_element})
                   }

        files = [

        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        # print(response.text)

    # declarando subprocesso para envio de comentario no pedido informando que carga foi aplicada com sucesso e pedido sera liberado
    def Cargaok():
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
                                          "commentcontent": "<strong>Pedido configurado por meio de RPA (Robot Programing Automation)</strong>\n- Lógicos foram configurados com êxito\n- Multibandeiras configuradas com êxito\n- Carga de tabelas aplicada com sucesso\n \n <strong>- Pedido liberado para implantação</strong>"})
                   }
        files = [

        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print("Requisição enviada")
        # print(response.text)

    # declarando subprocesso para envio de comentario no pedido informando que carga NAO FOI aplicada com sucesso e NAO SERA pedido sera liberado
    def CargaErro():
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
                                          "commentcontent": f"<strong>Pedido configurado por meio de RPA (Robot Programing Automation)</strong>\n- Lógicos foram configurados com êxito\n- Multibandeiras configuradas com êxito\n<strong>- CARGA DE TABELAS NÃO FORAM APLICADAS COM SUCESSO</strong>\n \n - Pedido NÃO pode ser liberado para implantação, status da carga: {resposta}\nPor favor revisar o Log e contatar o suporte."})
                   }
        files = [

        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print("Requisição enviada")
        # print(response.text)

    # Avaliando se pedido terá o status alterado para implantação ou não, qualquer coisa diferente de OK. ou enviando não vai dispara o comando.
    if resposta == "OK.":
        print(
            f"Resultado da carga de tabelas foi igual a OK/Enviando \nPedido {pdvno} terá o status alterado para implantação\n")
        Cargaok()
        req_status()
    elif resposta == "Enviando..." or "???Ha carga de tabelas em andamento.???" or "???Transacao em andamento???":
        print("\nIdentificado demora na aplicação de carga, iniciando time sleep de mais 21 segundos...")
        sleep(25)
    else:
        print(
            f"O resultado da carga de tabelas de algum modulo não foi OK.\nResultado: {resposta}\nStatus do pedido {pdvno} não será alterado para implantação automaticamente\nNecessita verificação!.")
        CargaErro()

