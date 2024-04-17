"""_____CONFIGURANDO BANDERIAS_____"""

def band():
    import http.client
    import json
    from selenium import webdriver
    from time import sleep
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    import oathtool
    from html.parser import HTMLParser
    from dotenv import load_dotenv, dotenv_values
    import os

    """ OBTER VARIAVEIS NECESSARIAS """
    # Resgatando variaveis .ENV   
    load_dotenv()

    # Link para requisição portal Gluo
    linkGluo = os.getenv("link_crm")

    # Abrir instancia de parametrização de bandeiras dos cartoes no ambiente cloud (script tem acesso a todos as configurações de banderias)
    getBand = os.getenv("get_band")

    # Credenciais de acesso para script configurar bandeiras de cartões 
    scriptUserB = os.getenv("script_userB")
    scriptPassB = os.getenv("script_passB")
    oathtoolB = os.getenv("oath_secretB")

    # Link de acesso ao ambiente cloud Software Express
    linkSwe = os.getenv("link_swe")

    ###########################################################################################################################

    print("Iniciando configuração de Multibandeiras\n")

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

    pdvno = p1

    conn = http.client.HTTPSConnection(linkGluo)
    payload = ''
    headers = {}
    conn.request("GET",
                 f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20cf_1454,%20cf_1452,%20cf_1464,%20cf_1462,%20cf_1590,%20%20cf_1466,%20cf_2223,%20cf_1468,%20cf_1480,%20cf_2047,%20cf_1472,%20cf_1470,%20%20cf_1556,%20cf_1548,%20cf_1574,%20cf_1504,%20cf_1502,%20cf_1450%20,%20cf_1456,%20cf_1458,%20cf_1460,%20cf_1482,%20cf_1492,%20cf_1494,%20cf_1496,%20cf_1498,%20cf_1500,%20cf_1506,%20cf_1508,%20cf_1510,%20cf_1512,%20cf_1514,%20cf_1516,%20cf_1518,%20cf_1520,%20cf_1522,%20cf_1524,%20cf_1526,%20cf_1528,%20cf_1530,%20cf_1532,%20cf_1534,%20cf_1536,%20cf_1538,%20cf_2225,%20cf_1540,%20cf_1542,%20cf_1544,%20cf_1546,%20cf_1550,%20cf_1552,%20cf_1554,%20cf_1558,%20cf_1560,%20cf_1562,%20cf_1564,%20cf_1566,%20cf_1568,%20cf_1570,%20cf_1572,%20cf_1576,%20cf_1578,%20cf_1580,%20cf_1582,%20cf_1584,%20cf_1586,%20cf_2049,%20cf_2051,%20cf_1588%20FROM%20SalesOrder%20WHERE%20salesorder_no='{pdvno}';&=",
                 payload, headers)
    res = conn.getresponse()
    data = res.read()

    """COMPILAR DADOS DA API [BANDEIRAS"""

    data_dict = json.loads(data)
    Amex = (data_dict["result"][0]["cf_1454"])
    print(f"Amex: {Amex}")

    Alelo = (data_dict["result"][0]["cf_1452"])
    print(f"Alelo: {Alelo}")

    VisaDebito = (data_dict["result"][0]["cf_1464"])
    print(f"Visa Débito: {VisaDebito}")

    VisaCredito = (data_dict["result"][0]["cf_1462"])
    print(f"Visa Crédito: {VisaCredito}")

    VisaVale = (data_dict["result"][0]["cf_1590"])
    print(f"Visa Vale: {VisaVale}")

    MasterCredito = (data_dict["result"][0]["cf_1466"])
    print(f"Master Crédito: {MasterCredito}")

    MasterVoucher = (data_dict["result"][0]["cf_2223"])
    print(f"Master Voucher: {MasterVoucher}")

    MaestroDebito = (data_dict["result"][0]["cf_1468"])
    print(f"Maestro Debito: {MaestroDebito}")

    Hiper = (data_dict["result"][0]["cf_1480"])
    print(f"Hiper: {Hiper}")

    HiperCredito = (data_dict["result"][0]["cf_2047"])
    print(f"Hiper Crédito: {HiperCredito}")

    EloDebito = (data_dict["result"][0]["cf_1472"])
    print(f"Elo Débito: {EloDebito}")

    EloCredito = (data_dict["result"][0]["cf_1470"])
    print(f"Elo Crédito: {EloCredito}")

    Ticket = (data_dict["result"][0]["cf_1556"])
    print(f"Ticket: {Ticket}")

    Sodexo = (data_dict["result"][0]["cf_1548"])
    print(f"Sodexo: {Sodexo}")

    VR = (data_dict["result"][0]["cf_1574"])
    print(f"VR: {VR}")

    CabalDebito = (data_dict["result"][0]["cf_1504"])
    print(f"Cabal Débito: {CabalDebito}")

    CabalCredito = (data_dict["result"][0]["cf_1502"])
    print(f"Cabal Crédito: {CabalCredito}")

    Agiplan = (data_dict["result"][0]["cf_1450"])
    print(f"Agiplan: {Agiplan}")

    AuraCredito = (data_dict["result"][0]["cf_1456"])
    print(f"Aura Crédito: {AuraCredito}")

    Avista = (data_dict["result"][0]["cf_1458"])
    print(f"Avista: {Avista}")

    BanescardCredito = (data_dict["result"][0]["cf_1460"])
    print(f"Banescard Crédito: {BanescardCredito}")

    BanescardDebito = (data_dict["result"][0]["cf_1492"])
    print(f"Banescard Débito: {BanescardDebito}")

    BanrisulCredito = (data_dict["result"][0]["cf_1482"])
    print(f"Banrisul Credito: {BanrisulCredito}")

    Banquet = (data_dict["result"][0]["cf_1494"])
    print(f"Banquet: {Banquet}")

    BanrisulDebito = (data_dict["result"][0]["cf_1496"])
    print(f"Banrisul Debito: {BanrisulDebito}")

    BNBClube = (data_dict["result"][0]["cf_1498"])
    print(f"BNB Clube: {BNBClube}")

    BonusCBA = (data_dict["result"][0]["cf_1500"])
    print(f"Bonus CBA: {BonusCBA}")

    CabalVoucher = (data_dict["result"][0]["cf_1506"])
    print(f"Cabal Voucher: {CabalVoucher}")

    CredsystemMais = (data_dict["result"][0]["cf_1508"])
    print(f"Credsystem - Mais: {CredsystemMais}")

    Credz = (data_dict["result"][0]["cf_1510"])
    print(f"Credz: {Credz}")

    CooperCredCredito = (data_dict["result"][0]["cf_1512"])
    print(f"CooperCred Crédito: {CooperCredCredito}")

    CooperCredDebito = (data_dict["result"][0]["cf_1514"])
    print(f"CooperCred Débito: {CooperCredDebito}")

    DinnersCredito = (data_dict["result"][0]["cf_1516"])
    print(f"Dinners Crédito: {DinnersCredito}")

    Fininvest = (data_dict["result"][0]["cf_1518"])
    print(f"Fininvest: {Fininvest}")

    GoodCardCredito = (data_dict["result"][0]["cf_1520"])
    print(f"GoodCard Crédito: {GoodCardCredito}")

    GoodCardDebito = (data_dict["result"][0]["cf_1522"])
    print(f"GoodCard Débito: {GoodCardDebito}")

    GreenCard = (data_dict["result"][0]["cf_1524"])
    print(f"GreenCard: {GreenCard}")

    JCBCredito = (data_dict["result"][0]["cf_1526"])
    print(f"JCB Crédito: {JCBCredito}")

    Nutricash = (data_dict["result"][0]["cf_1528"])
    print(f"Nutricash: {Nutricash}")

    Planvale = (data_dict["result"][0]["cf_1530"])
    print(f"Planvale: {Planvale}")

    PLVisa = (data_dict["result"][0]["cf_1532"])
    print(f"PLVisa: {PLVisa}")

    PLMaster = (data_dict["result"][0]["cf_1534"])
    print(f"PLMaster: {PLMaster}")

    PolicardDebito = (data_dict["result"][0]["cf_1538"])
    print(f"Policard Débito: {PolicardDebito}")

    PolicardVoucher = (data_dict["result"][0]["cf_2225"])
    print(f"Policard Voucher: {PolicardVoucher}")

    PolicardCredito = (data_dict["result"][0]["cf_1536"])
    print(f"Policard Crédito: {PolicardCredito}")

    BanriCardVoucher = (data_dict["result"][0]["cf_1540"])
    print(f"BanriCard Voucher: {BanriCardVoucher}")

    Sapore = (data_dict["result"][0]["cf_1542"])
    print(f"Sapore: {Sapore}")

    SicrediDebito = (data_dict["result"][0]["cf_1546"])
    print(f"Sicredi Débito: {SicrediDebito}")

    SicrediCredito = (data_dict["result"][0]["cf_1544"])
    print(f"Sicredi Crédito: {SicrediCredito}")

    SorocredDebito = (data_dict["result"][0]["cf_1550"])
    print(f"Sorocred Débito: {SorocredDebito}")

    SorocredCredito = (data_dict["result"][0]["cf_1552"])
    print(f"Sorocred Crédito: {SorocredCredito}")

    SorocredVoucher = (data_dict["result"][0]["cf_1554"])
    print(f"Sorocred Voucher: {SorocredVoucher}")

    Valecard = (data_dict["result"][0]["cf_1558"])
    print(f"Valecard: {Valecard}")

    ValecardDebito = (data_dict["result"][0]["cf_1560"])
    print(f"Valecard Débito: {ValecardDebito}")

    Valefacil = (data_dict["result"][0]["cf_1562"])
    print(f"Valefacil: {Valefacil}")

    Valemulti = (data_dict["result"][0]["cf_1564"])
    print(f"Valemulti: {Valemulti}")

    Valefrota = (data_dict["result"][0]["cf_1566"])
    print(f"Valefrota: {Valefrota}")

    VerdCard = (data_dict["result"][0]["cf_1568"])
    print(f"VerdCard: {VerdCard}")

    VerochequeCredito = (data_dict["result"][0]["cf_1570"])
    print(f"Verocheque Crédito: {VerochequeCredito}")

    VerochequeVoucher = (data_dict["result"][0]["cf_1572"])
    print(f"Verocheque Voucher: {VerochequeVoucher}")

    BanesecardDebito = (data_dict["result"][0]["cf_1578"])
    print(f"Banesecard Debito: {BanesecardDebito}")

    BanesecardCredito = (data_dict["result"][0]["cf_1576"])
    print(f"Banesecard Crédito: {BanesecardCredito}")

    BanesecardVoucher = (data_dict["result"][0]["cf_1580"])
    print(f"Banesecard Voucher: {BanesecardVoucher}")

    BanricardPrivateLabel = (data_dict["result"][0]["cf_1582"])
    print(f"Banricard Private Label: {BanricardPrivateLabel}")

    BENVisaVale = (data_dict["result"][0]["cf_1584"])
    print(f"BEN Visa Vale: {BENVisaVale}")

    Calcard = (data_dict["result"][0]["cf_1586"])
    print(f"Calcard: {Calcard}")

    RedeComprasCredito = (data_dict["result"][0]["cf_2049"])
    print(f"RedeCompras Credito: {RedeComprasCredito}")

    RedeComprasDebito = (data_dict["result"][0]["cf_2051"])
    print(f"RedeCompras Debito: {RedeComprasDebito}")

    Senff = (data_dict["result"][0]["cf_1496"])
    print(f"Senff: {Senff}")

    print()

    # PEGAR ID SITEF COM BASE NO CRM
    conn = http.client.HTTPSConnection(linkGluo)
    payload = ''
    headers = {}
    conn.request("GET",
                 f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20cf_2088%20FROM%20SalesOrder%20WHERE%20salesorder_no='{pdvno}';&=",
                 payload, headers)
    res = conn.getresponse()
    data = res.read()

    data_dict = json.loads(data)
    idsitef = (data_dict["result"][0]["cf_2088"])
    #print(f"Id cliente: {idsitef}")

    """ INICIANDO WEBDRIVER """

    servico = Service(ChromeDriverManager().install())

    browser = webdriver.Chrome(service=servico)
    browser.get(linkSwe)

    # Entra e loga no portal
    search_box_login = browser.find_element(By.NAME, "username")
    search_box_login.send_keys(scriptUserB)

    search_box_passw = browser.find_element(By.NAME, "password")
    search_box_passw.send_keys(scriptPassB)
    search_box_login.submit()

    sleep(2)

    SECRET = oathtoolB
    var = (oathtool.generate_otp(SECRET))

    #print(var)

    #print(f"O codigo adquirido foi: {var}")

    # atribuindo cada caracter de "texto" as devidas variaveis de um a seis
    var_u = var[0]
    var_d = var[1]
    var_t = var[2]
    var_q = var[3]
    var_c = var[4]
    var_s = var[5]

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

    entrar_botao = browser.find_element(By.XPATH, '//*[@id="kc-login"]').click()

    sleep(3)

    # clica aba configuador
    mouse_over = browser.find_element(By.XPATH, '//*[@id="menuConfigurador"]/span').click()
    sleep(1)
    over_click = browser.find_element(By.XPATH, '//*[@id="menuConfiguradorSiTef"]/span/a').click()

    # vai pra aba gerada
    browser.switch_to.window(browser.window_handles[1])

    # aguarda carrgar configurador
    sleep(30)

    # entra roteamento
    # Entrar no configurador sitef
    browser.get(getBand)

    # browser.find_element(By.XPATH, '//*[@id="centro"]/div/ul[1]/li[2]/a').click()

    sleep(11)

    # clica multibandieras
    browser.find_element(By.XPATH, '//*[@id="sd1"]').click()

    sleep(10)

    # clica scrow clientes
    browser.find_element(By.XPATH, '//*[@id="botaoseta"]').click()
    sleep(3)

    """ SELECIONAR CLIENTE COM BASE NO ID SITEF DO CRM """

    browser.find_element(By.XPATH, f'//*[@id="ComboEmp"]/option[@value={idsitef}]').click()
    sleep(5)

    dados_cliente = browser.find_element(By.XPATH, '//*[@id="LabelDadosEmpresa"]').text
    print(dados_cliente)

    ### Click todas banderias nenhum ###

    # clica campo todas bandeiras

    browser.find_element(By.XPATH, '//*[@id="selectAutorizadoresMultiBandeira"]').click()

    # seleciona bin

    browser.find_element(By.XPATH, '//*[@id="selectAutorizadoresMultiBandeira"]/option[2]').click()

    sleep(2)
    
    # confirma 
    browser.switch_to.alert.accept()

    # clica campo todas bandeiras
    browser.find_element(By.XPATH, '//*[@id="selectAutorizadoresMultiBandeira"]').click()

    #seleciona nenhum
    browser.find_element(By.XPATH, '//*[@id="selectAutorizadoresMultiBandeira"]/option[7]').click()

    sleep(2)

    #confirma
    browser.switch_to.alert.accept()

    sleep(1)
    # primeiro click
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[6]').click()

    # AMEX

    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[6]/td[1]').click()

    if Amex == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Amex == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Amex == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Amex == "GetNetLac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Amex == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Amex == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Amex == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Amex == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Amex == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Amex == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Amex == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Amex == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # ALELO

    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[5]/td[1]').click()

    if Alelo == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Alelo == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Alelo == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Alelo == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Alelo == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Alelo == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Alelo == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Alelo == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Alelo == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Alelo == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Alelo == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Alelo == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # visa debito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[107]/td[1]').click()

    if VisaDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif VisaDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif VisaDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif VisaDebito == "GetNetLac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif VisaDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif VisaDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif VisaDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif VisaDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif VisaDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif VisaDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif VisaDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif VisaDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # visa credito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[106]/td[1]').click()

    if VisaCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif VisaCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif VisaCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif VisaCredito == "GetNetLac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif VisaCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif VisaCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif VisaCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif VisaCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif VisaCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif VisaCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif VisaCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif VisaCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # visa vale
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[108]/td[1]').click()

    if VisaVale == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif VisaVale == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif VisaVale == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif VisaVale == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif VisaVale == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif VisaVale == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif VisaVale == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif VisaVale == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif VisaVale == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif VisaVale == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif VisaVale == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif VisaVale == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # MasterCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[63]/td[1]').click()

    if MasterCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif MasterCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif MasterCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif MasterCredito == "GetNetLac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif MasterCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif MasterCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif MasterCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif MasterCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif MasterCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif MasterCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif MasterCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif MasterCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Master voucher
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[62]/td[1]').click()

    if MaestroDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif MaestroDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif MaestroDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif MaestroDebito == "GetNetLac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif MaestroDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif MaestroDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif MaestroDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif MaestroDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif MaestroDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif MaestroDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif MaestroDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif MaestroDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # MaestroDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[61]/td[1]').click()

    if MaestroDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif MaestroDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif MaestroDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif MaestroDebito == "GetNetLac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif MaestroDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif MaestroDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif MaestroDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif MaestroDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif MaestroDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif MaestroDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif MaestroDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif MaestroDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Hiper
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[57]/td[1]').click()

    if Hiper == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Hiper == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Hiper == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Hiper == "GetNetLac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Hiper == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Hiper == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Hiper == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Hiper == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Hiper == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Hiper == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Hiper == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Hiper == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # HiperCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[56]/td[1]').click()

    if HiperCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif HiperCredito == "BIN":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif HiperCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif HiperCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif HiperCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif HiperCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif HiperCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif HiperCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif HiperCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif HiperCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif HiperCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif HiperCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # EloDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[46]/td[1]').click()

    if EloDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif EloDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif EloDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif EloDebito == "GetNetLac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif EloDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif EloDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif EloDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif EloDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif EloDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif EloDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif EloDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif EloDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # EloCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[45]/td[1]').click()

    if EloCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif EloCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif EloCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif EloCredito == "GetNetLac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif EloCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif EloCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif EloCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif EloCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif EloCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif EloCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif EloCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif EloCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Ticket
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[94]/td[1]').click()
    if Ticket == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Ticket == "BIN":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Ticket == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Ticket == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Ticket == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Ticket == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Ticket == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Ticket == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Ticket == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Ticket == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Ticket == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Ticket == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Sodexo
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[90]/td[1]').click()
    if Sodexo == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Sodexo == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Sodexo == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Sodexo == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Sodexo == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Sodexo == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Sodexo == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Sodexo == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Sodexo == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Sodexo == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Sodexo == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Sodexo == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # VR
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[112]/td[1]').click()
    if VR == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif VR == "BIN":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif VR == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif VR == "Getletlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif VR == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif VR == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif VR == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif VR == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif VR == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif VR == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif VR == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif VR == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # CabalDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[31]/td[1]').click()
    if CabalDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif CabalDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif CabalDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif CabalDebito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif CabalDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif CabalDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif CabalDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif CabalDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif CabalDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif CabalDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif CabalDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif CabalDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # CabalCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[30]/td[1]').click()
    if CabalCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif CabalCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif CabalCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif CabalCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif CabalCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif CabalCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif CabalCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif CabalCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif CabalCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif CabalCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif CabalCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif CabalCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Agiplan c
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[3]/td[1]').click()
    if Agiplan == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Agiplan == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Agiplan == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Agiplan == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Agiplan == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Agiplan == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Agiplan == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Agiplan == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Agiplan == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Agiplan == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Agiplan == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Agiplan == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # # Agiplan d
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[4]/td[1]').click()
    if Agiplan == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Agiplan == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Agiplan == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Agiplan == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Agiplan == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Agiplan == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Agiplan == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Agiplan == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Agiplan == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Agiplan == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Agiplan == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Agiplan == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # AuraCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[7]/td[1]').click()
    if AuraCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif AuraCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif AuraCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif AuraCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif AuraCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif AuraCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif AuraCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif AuraCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif AuraCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif AuraCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif AuraCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif AuraCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Avista
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[10]/td[1]').click()
    if Avista == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Avista == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Avista == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Avista == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Avista == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Avista == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Avista == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Avista == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Avista == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Avista == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Avista == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Avista == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # BanescardCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[12]/td[1]').click()
    if BanescardCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif BanescardCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif BanescardCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif BanescardCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif BanescardCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif BanescardCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif BanescardCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif BanescardCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif BanescardCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif BanescardCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif BanescardCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif BanescardCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # BanescardDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[13]/td[1]').click()
    if BanescardDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif BanescardDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif BanescardDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif BanescardDebito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif BanescardDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif BanescardDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif BanescardDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif BanescardDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif BanescardDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif BanescardDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif BanescardDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif BanescardDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # BanrisulDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[21]/td[1]').click()

    if BanrisulDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif BanrisulDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif BanrisulDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif BanrisulDebito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif BanrisulDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif BanrisulDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif BanrisulDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif BanrisulDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif BanrisulDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif BanrisulDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif BanrisulDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif BanrisulDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # BanrisulCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[20]/td[1]').click()

    if BanrisulCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif BanrisulCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif BanrisulCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif BanrisulCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif BanrisulCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif BanrisulCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif BanrisulCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif BanrisulCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif BanrisulCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif BanrisulCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif BanrisulCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif BanrisulCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass


    # Banquet
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[17]/td[1]').click()

    if Banquet == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Banquet == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Banquet == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Banquet == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Banquet == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Banquet == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Banquet == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Banquet == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Banquet == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Banquet == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Banquet == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Banquet == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # BNBClube
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[26]/td[1]').click()

    if BNBClube == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif BNBClube == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif BNBClube == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif BNBClube == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif BNBClube == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif BNBClube == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif BNBClube == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif BNBClube == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif BNBClube == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif BNBClube == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif BNBClube == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif BNBClube == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # BonusCBA
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[27]/td[1]').click()

    if BonusCBA == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif BonusCBA == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif BonusCBA == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif BonusCBA == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif BonusCBA == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif BonusCBA == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif BonusCBA == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif BonusCBA == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif BonusCBA == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif BonusCBA == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif BonusCBA == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif BonusCBA == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # CabalVoucher
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[32]/td[1]').click()

    if CabalVoucher == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif CabalVoucher == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif CabalVoucher == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif CabalVoucher == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif CabalVoucher == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif CabalVoucher == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif CabalVoucher == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif CabalVoucher == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif CabalVoucher == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif CabalVoucher == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif CabalVoucher == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif CabalVoucher == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # CredsystemMais
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[41]/td[1]').click()

    if CredsystemMais == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif CredsystemMais == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif CredsystemMais == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif CredsystemMais == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif CredsystemMais == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif CredsystemMais == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif CredsystemMais == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif CredsystemMais == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif CredsystemMais == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif CredsystemMais == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif CredsystemMais == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif CredsystemMais == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Credz
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[42]/td[1]').click()

    if Credz == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Credz == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Credz == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Credz == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Credz == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Credz == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Credz == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Credz == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Credz == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Credz == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Credz == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Credz == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # CooperCredCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[39]/td[1]').click()

    if CooperCredCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif CooperCredCredito == "BIN":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif CooperCredCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif CooperCredCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif CooperCredCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif CooperCredCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif CooperCredCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif CooperCredCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif CooperCredCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif CooperCredCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif CooperCredCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif CooperCredCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # CooperCredDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[38]/td[1]').click()

    if CooperCredDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif CooperCredDebito == "BIN":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif CooperCredDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif CooperCredDebito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif CooperCredDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif CooperCredDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif CooperCredDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif CooperCredDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif CooperCredDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif CooperCredDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif CooperCredDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif CooperCredDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # DinnersCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[43]/td[1]').click()

    if DinnersCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif DinnersCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif DinnersCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif DinnersCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif DinnersCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif DinnersCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif DinnersCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif DinnersCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif DinnersCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif DinnersCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif DinnersCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif DinnersCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Fininvest
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[50]/td[1]').click()

    if Fininvest == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Fininvest == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Fininvest == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Fininvest == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Fininvest == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Fininvest == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Fininvest == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Fininvest == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Fininvest == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Fininvest == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Fininvest == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Fininvest == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # GoodCardCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[52]/td[1]').click()

    if GoodCardCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif GoodCardCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif GoodCardCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif GoodCardCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif GoodCardCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif GoodCardCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif GoodCardCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif GoodCardCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif GoodCardCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif GoodCardCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif GoodCardCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif GoodCardCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # GoodCardDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[53]/td[1]').click()

    if GoodCardDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif GoodCardDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif GoodCardDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif GoodCardDebito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif GoodCardDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif GoodCardDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif GoodCardDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif GoodCardDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif GoodCardDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif GoodCardDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif GoodCardDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif GoodCardDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # GoodCardvoucher - ativo SE debito habilitado
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[54]/td[1]').click()

    if GoodCardDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif GoodCardDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif GoodCardDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif GoodCardDebito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif GoodCardDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif GoodCardDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif GoodCardDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif GoodCardDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif GoodCardDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif GoodCardDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif GoodCardDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif GoodCardDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # GreenCard
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[55]/td[1]').click()

    if GreenCard == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif GreenCard == "BIN":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif GreenCard == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif GreenCard == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif GreenCard == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif GreenCard == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif GreenCard == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif GreenCard == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif GreenCard == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif GreenCard == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif GreenCard == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif GreenCard == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # JCBCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[58]/td[1]').click()

    if JCBCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif JCBCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif JCBCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif JCBCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif JCBCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif JCBCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif JCBCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif JCBCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif JCBCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif JCBCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif JCBCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif JCBCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Nutricash
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[72]/td[1]').click()

    if Nutricash == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Nutricash == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Nutricash == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Nutricash == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Nutricash == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Nutricash == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Nutricash == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Nutricash == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Nutricash == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Nutricash == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Nutricash == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Nutricash == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Planvale
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[76]/td[1]').click()

    if Planvale == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Planvale == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Planvale == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Planvale == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Planvale == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Planvale == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Planvale == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Planvale == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Planvale == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Planvale == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Planvale == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Planvale == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # PLVisa
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[78]/td[1]').click()

    if PLVisa == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif PLVisa == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif PLVisa == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif PLVisa == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif PLVisa == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif PLVisa == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif PLVisa == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif PLVisa == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif PLVisa == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif PLVisa == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif PLVisa == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif PLVisa == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # PLMaster
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[77]/td[1]').click()

    if PLMaster == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif PLMaster == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif PLMaster == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif PLMaster == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif PLMaster == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif PLMaster == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif PLMaster == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif PLMaster == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif PLMaster == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif PLMaster == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif PLMaster == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif PLMaster == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # PolicardDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[80]/td[1]').click()

    if PolicardDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif PolicardDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif PolicardDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif PolicardDebito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif PolicardDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif PolicardDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif PolicardDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif PolicardDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif PolicardDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif PolicardDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif PolicardDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif PolicardDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # PolicardCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[79]/td[1]').click()

    if PolicardCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif PolicardCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif PolicardCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif PolicardCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif PolicardCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif PolicardCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif PolicardCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif PolicardCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif PolicardCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif PolicardCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif PolicardCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif PolicardCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # PolicardVoucher

    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[81]/td[1]').click()

    if PolicardVoucher == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif PolicardVoucher == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif PolicardVoucher == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif PolicardVoucher == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif PolicardVoucher == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif PolicardVoucher == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif PolicardVoucher == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif PolicardVoucher == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif PolicardVoucher == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif PolicardVoucher == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif PolicardVoucher == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif PolicardVoucher == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # BanriCardVoucher
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[19]/td[1]').click()

    if BanriCardVoucher == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif BanriCardVoucher == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif BanriCardVoucher == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif BanriCardVoucher == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif BanriCardVoucher == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif BanriCardVoucher == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif BanriCardVoucher == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif BanriCardVoucher == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif BanriCardVoucher == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif BanriCardVoucher == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif BanriCardVoucher == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif BanriCardVoucher == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Sapore
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[84]/td[1]').click()

    if Sapore == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Sapore == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Sapore == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Sapore == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Sapore == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Sapore == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Sapore == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Sapore == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Sapore == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Sapore == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Sapore == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Sapore == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # SicrediCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[87]/td[1]').click()

    if SicrediCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif SicrediCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif SicrediCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif SicrediCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif SicrediCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif SicrediCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif SicrediCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif SicrediCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif SicrediCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif SicrediCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif SicrediCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif SicrediCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # SicrediDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[88]/td[1]').click()

    if SicrediDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif SicrediDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif SicrediDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif SicrediDebito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif SicrediDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif SicrediDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif SicrediDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif SicrediDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif SicrediDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif SicrediDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif SicrediDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif SicrediDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # SorocredDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[92]/td[1]').click()

    if SorocredDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif SorocredDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif SorocredDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif SorocredDebito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif SorocredDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif SorocredDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif SorocredDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif SorocredDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif SorocredDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif SorocredDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif SorocredDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif SorocredDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # SorocredCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[91]/td[1]').click()

    if SorocredCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif SorocredCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif SorocredCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif SorocredCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif SorocredCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif SorocredCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif SorocredCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif SorocredCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif SorocredCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif SorocredCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif SorocredCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif SorocredCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # SorocredVoucher
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[93]/td[1]').click()

    if SorocredVoucher == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif SorocredVoucher == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif SorocredVoucher == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif SorocredVoucher == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif SorocredVoucher == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif SorocredVoucher == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif SorocredVoucher == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif SorocredVoucher == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif SorocredVoucher == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif SorocredVoucher == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif SorocredVoucher == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif SorocredVoucher == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Valecard
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[96]/td[1]').click()

    if Valecard == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Valecard == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Valecard == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Valecard == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Valecard == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Valecard == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Valecard == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Valecard == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Valecard == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Valecard == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Valecard == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Valecard == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # ValecardDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[97]/td[1]').click()

    if ValecardDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif ValecardDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif ValecardDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif ValecardDebito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif ValecardDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif ValecardDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif ValecardDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif ValecardDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif ValecardDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif ValecardDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif ValecardDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif ValecardDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Valefacil
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[99]/td[1]').click()

    if Valefacil == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Valefacil == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Valefacil == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Valefacil == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Valefacil == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Valefacil == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Valefacil == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Valefacil == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Valefacil == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Valefacil == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Valefacil == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Valefacil == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Valemulti
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[101]/td[1]').click()

    if Valemulti == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Valemulti == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Valemulti == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Valemulti == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Valemulti == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Valemulti == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Valemulti == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Valemulti == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Valemulti == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Valemulti == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Valemulti == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Valemulti == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Valefrota
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[100]/td[1]').click()

    if Valefrota == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Valefrota == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Valefrota == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Valefrota == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Valefrota == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Valefrota == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Valefrota == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Valefrota == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Valefrota == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Valefrota == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Valefrota == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Valefrota == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # VerdCard
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[102]/td[1]').click()

    if VerdCard == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif VerdCard == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif VerdCard == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif VerdCard == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif VerdCard == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif VerdCard == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif VerdCard == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif VerdCard == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif VerdCard == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif VerdCard == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif VerdCard == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif VerdCard == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # VerochequeCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[104]/td[1]').click()

    if VerochequeCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif VerochequeCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif VerochequeCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif VerochequeCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif VerochequeCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif VerochequeCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif VerochequeCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif VerochequeCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif VerochequeCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif VerochequeCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif VerochequeCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif VerochequeCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # VerochequeVoucher
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[105]/td[1]').click()

    if VerochequeVoucher == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif VerochequeVoucher == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif VerochequeVoucher == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif VerochequeVoucher == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif VerochequeVoucher == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif VerochequeVoucher == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif VerochequeVoucher == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif VerochequeVoucher == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif VerochequeVoucher == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif VerochequeVoucher == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif VerochequeVoucher == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif VerochequeVoucher == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # BanesecardCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[14]/td[1]').click()

    if BanesecardCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif BanesecardCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif BanesecardCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif BanesecardCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif BanesecardCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif BanesecardCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif BanesecardCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif BanesecardCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif BanesecardCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif BanesecardCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif BanesecardCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif BanesecardCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # BanesecardDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[15]/td[1]').click()

    if BanesecardDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif BanesecardDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif BanesecardDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif BanesecardDebito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif BanesecardDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif BanesecardDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif BanesecardDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif BanesecardDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif BanesecardDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif BanesecardDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif BanesecardDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif BanesecardDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # BanesecardVoucher
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[16]/td[1]').click()

    if BanesecardVoucher == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif BanesecardVoucher == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif BanesecardVoucher == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif BanesecardVoucher == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif BanesecardVoucher == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif BanesecardVoucher == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif BanesecardVoucher == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif BanesecardVoucher == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif BanesecardVoucher == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif BanesecardVoucher == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif BanesecardVoucher == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif BanesecardVoucher == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # BanricardPrivateLabel
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[18]/td[1]').click()

    if BanricardPrivateLabel == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif BanricardPrivateLabel == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif BanricardPrivateLabel == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif BanricardPrivateLabel == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif BanricardPrivateLabel == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif BanricardPrivateLabel == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif BanricardPrivateLabel == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif BanricardPrivateLabel == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif BanricardPrivateLabel == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif BanricardPrivateLabel == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif BanricardPrivateLabel == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif BanricardPrivateLabel == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # BENVisaVale
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[22]/td[1]').click()

    if BENVisaVale == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif BENVisaVale == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif BENVisaVale == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif BENVisaVale == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif BENVisaVale == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif BENVisaVale == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif BENVisaVale == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif BENVisaVale == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif BENVisaVale == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif BENVisaVale == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif BENVisaVale == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif BENVisaVale == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Calcard
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[33]/td[1]').click()

    if Calcard == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Calcard == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Calcard == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Calcard == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Calcard == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Calcard == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Calcard == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Calcard == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Calcard == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Calcard == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Calcard == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Calcard == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Senff c
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[83]/td[1]').click()

    if Senff == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Senff == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Senff == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Senff == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Senff == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Senff == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Senff == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Senff == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Senff == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Senff == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Senff == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Senff == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # Senff v
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[84]/td[1]').click()

    if Senff == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif Senff == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif Senff == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif Senff == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif Senff == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif Senff == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif Senff == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif Senff == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif Senff == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif Senff == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif Senff == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif Senff == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # RedeComprasCredito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[82]/td[1]').click()

    if RedeComprasCredito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif RedeComprasCredito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif RedeComprasCredito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif RedeComprasCredito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif RedeComprasCredito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif RedeComprasCredito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif RedeComprasCredito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif RedeComprasCredito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif RedeComprasCredito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif RedeComprasCredito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif RedeComprasCredito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif RedeComprasCredito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    # RedeComprasDebito
    browser.find_element(By.XPATH, '//*[@id="tabMB"]/tbody/tr[83]/td[1]').click()

    if RedeComprasDebito == "Adiq":
        browser.find_element(By.XPATH, '//*[@id="Adiq"]').click()

    elif RedeComprasDebito == "Bin":
        browser.find_element(By.XPATH, '//*[@id="Bin"]').click()

    elif RedeComprasDebito == "Cielo":
        browser.find_element(By.XPATH, '//*[@id="Cielo"]').click()

    elif RedeComprasDebito == "Getnetlac":
        browser.find_element(By.XPATH, '//*[@id="Getnetlac"]').click()

    elif RedeComprasDebito == "GlobalPayments":
        browser.find_element(By.XPATH, '//*[@id="GlobalPayments"]').click()

    elif RedeComprasDebito == "PagSeguro":
        browser.find_element(By.XPATH, '//*[@id="PagSeguro"]').click()

    elif RedeComprasDebito == "Rede":
        browser.find_element(By.XPATH, '//*[@id="Rede"]').click()

    elif RedeComprasDebito == "Safra":
        browser.find_element(By.XPATH, '//*[@id="Safra"]').click()

    elif RedeComprasDebito == "Sipag":
        browser.find_element(By.XPATH, '//*[@id="SiPAG"]').click()

    elif RedeComprasDebito == "Stone":
        browser.find_element(By.XPATH, '//*[@id="Stone"]').click()

    elif RedeComprasDebito == "Tricard":
        browser.find_element(By.XPATH, '//*[@id="Tricard"]').click()

    elif RedeComprasDebito == "Vero":
        browser.find_element(By.XPATH, '//*[@id="Vero"]').click()

    else:
        # print("Bandeira sem roteamento")
        pass

    sleep(3)
    salvar = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[3]/table/tbody/tr/td[2]/input')
    salvar.click()

    print("time sleep... 2seg")
    print()

    sleep(2)

    print("Configuração de bandeiras concluida!")

    browser.quit()

     