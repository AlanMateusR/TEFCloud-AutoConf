def imap_code():
    import imaplib
    import email
    import re
    import quopri
    from dotenv import load_dotenv, dotenv_values
    import os

    """ OBTER VARIAVEIS NECESSARIAS """
    # Resgatando variaveis .ENV  

    # Credenciais de acesso IMAP para acessar caixa de entrada do GMAIL (script possui um email proprio onde recebe token de confirmação para as ações efetuadas no ambiente cloud)
    imapE = os.getenv("imap_email")
    imapP = os.getenv("imap_pass")

    load_dotenv()

    # conectar ao servidor do gmail imap
    objCon = imaplib.IMAP4_SSL("imap.gmail.com")

    # logar no email
    login = imapE

    senha = imapP
    objCon.login(login, senha)

    codigo = None

    #procura no email recebido o token de confirmação para efetuar COMITTI no ambiente cloud
    def find_code(txt):
        global codigo
        pattern = r"Código:\s*(\d+)"

        matches = re.findall(pattern, txt)

        if matches:
            codigo = matches[0]
            #print("Found code:", codigo)
            with open("imap.txt", "w", encoding="utf-8") as arquivo:
                frases = list()
                frases.append(f"{codigo}")
                arquivo.writelines(frases)
        else:
            print("Code not found")


    def analyze_msg(mail_msg):
        msgtxt = quopri.decodestring(mail_msg.get_payload(decode=True)).decode('UTF-8')
        # no_html_tags = re.sub('<[^<]+?>', '', msgtxt)
        # find_code(no_html_tags)
        find_code(msgtxt)
        # print(msgtxt)


    print(objCon.select(mailbox='inbox', readonly=True))
    # filtro
    resposta, idDosEmails = objCon.search(None, 'All')

    for num in idDosEmails[0].split():
        resultado, dados = objCon.fetch(num, '(RFC822)')
        texto_do_email = dados[0][1]
        texto_do_email = texto_do_email.decode('UTF-8')
        texto_do_email = email.message_from_string(texto_do_email)
        # print(texto_do_email)
        msg = texto_do_email

        if msg.is_multipart():
            # print("is multipart")
            for part in msg.get_payload():
                # print(part.get_payload())
                forwarded = email.message_from_string(part.get_payload())
                # print(forwarded.get_payload())
                if forwarded.is_multipart():
                    for fpart in forwarded.get_payload(decode=True):
                        analyze_msg(fpart)
                else:
                    analyze_msg(forwarded)
        else:
            analyze_msg(msg)

    # print("Código encontrado:  ", codigo)

    #print(f"Token adquirido: {codigo}")

    