# TEF-Cloud-AutoConf

## Projeto composto por software RPA & Web-Scraping que tem por objetivo automatizar configurações diversas em um servidor dedicado com base em dados de um CRM.

 * **Projeto:** Automatização de longas tarefas complexas e manuais em um ambiente com servidor nuvem dedicado, tudo com base em dados de um CRM comunicando-se por meio de API.
 * **Arquivos:** LogicoConf.py | BandeiraCargaConf.py | CargaConfAndLog.py | get_session.py | imap.py | credentials.env 
 * **Status do projeto:** Entregue

 
 * **Escopo:** Empresa disponibiliza serviços de suporte para integração no escopo de TEF (Transferencia eletronica de fundos) e vende a propria VPN e TLS para este fim. Cabe também ao integrador TEF do cliente a responsabilidade de preparar o ambiente TEF dos mesmos para possibilitar as devidas comunicações entre PDV (Ponto de venda/ERP) e Adquirente (operadora de cartão), seja por parametrização para padrão em vendas via TEF ou configurações diversas no escopo meio de pagamento.

 * **Problematica:** Colaboradores do setor técnico designado da empresa necessitam diariamente verificar uma lista de clientes no CRM da organização com status do pedido de venda em APROVADO, cujo significado é a necessidade de efetuar uma serie de configurações, parametrizações e testes em um ambiente nuvem dedicado afim de possibilitar uma integração cruzada entre servidores, tudo com base em um formulario que foi devidamente licenciado pelo setor comercial/financeiro, no CRM se encontram todos os dados que devem ser configurados MANUALMENTE um por um no ambiente reservado, no caso de conformidade entre todas as informações e se a integração for bem sucedida (comunicação online) o pedido de venda TEF do cliente deve passar a ter o status alterado para IMPLANTAÇÃO.
 * **Solução:** Software de teste automatizado foi programado para efetivar todo o procedimento de configuração, verificação, teste e parametrização da demanda de forma automatizada, agilizada e simplificada. Para o projeto foram concedidos acesso ao ambiente de configuração de modulos da Fiserv, e ainda as chaves de acesso para integração via API ao portal de CRM Gluo (baseado em Vtiger CRM).

  
 * **Autor:** Alan Mateus Rodrigues
 * **Data de Criação:** 25/02/2024
 * **Ramo da empresa:** Tecnologia em meios de pagamento

<br>

 ## !!! Adendo !!!
 * **Este código é disponibilizado no GitHub exclusivamente como parte do portfólio de programação do autor.**
* **O objetivo é demonstrar experiência e habilidades na área de programação.** 
* **Não é recomendada a reprodução, distribuição ou utilização deste código para qualquer finalidade.**

 >* Links, nomes e dados confidenciais foram censurados e a explicação tecnica do funcionamento do codigo foi resumida.
 >* Para mais informações, entre em contato com o autor em: www.linkedin.com/in/alan-rodrigues-983822218 
 

<br>

|| IMPLEMENTAÇÃO ||

[Breve explicação do fluxo de funcionamento]

* 1. Primeiramente é configurado no servidor um numero lógico repassado pelo autorizador, o numero lógico TEF visa integrar o PDV (PONTO DE VENDA) do cliente final a operadora de cartão (exemplo: REDE, CIELO, STONE) por meio do servidor cloud alocado nas dependencias da FISERV.
* 2. Verificar se o numero lógico esta dentro do padrão do autorizador (cada autorizador tem seu padrão, por exemplo para CIELO o padrão de lógico é sempre começar com digito 4)
* 3. Após ser inserido o numero lógico, é enviado token de confirmação de configuração para caixa de entrada do analista poder fazer COMMIT no servidor.
*4. Buscar todos os dados de relação de multibandeiras TEF do CRM para efetuar configuração de bandeiras no servidor (a relação de bandeiras visa parametrizar qual operadora de cartão vai autorizar cada bandeira, exemplo; Mastercard Credito será autorizado pela Cielo)
* 5. Após parametrizar as bandeiras, deve-se efetuar uma "carga de tabelas" que em suma faz um "ping" no servidor da operadora de cartão utilizando o numero lógico que foi configurado (se numero lógico não for valido a carga de tabelas resultará em erro)
* 6. Deve ser revisado se as configurações foram aplicadas corretamente e a carga de tabelas resultou em sucesso, caso tudo esteja em conformidade deve-se alterar o status da licença do cliente para IMPLANTAÇÃO e comentado os Logs no CRM.

<br>
<br>

[Script - resumo]

  Configurar numero lógico da operadora de cartão fixado no pedido de venda TEF 
 > Script vai colher os dados do pedido de venda selecionado via API do CRM, Numero do pedido de venda, Cnpj e Id Sitef 

| Regra de inicialização |
* deve haver pelo menos uma adquirente no pedido <<<
* pedido deve ter o campo "id sitef" preenchido <<<
* pedido deve estar com status de aprovado <<<


>> Com os dados já em cache no programa, driver de simulação do navegador google-chrome (Webdriver-manager) vai inicializar na pagina de login do Sitef e começar as devidas configurações, validações e autenticações.
>> Uma nova instancia do selenium será inicializada para efetuar nova integração e coleta de dados do CRM via API para então parametrizar toda a relação de bandeiras nos server.
>> Mais uma vez outra instancia é criada para fazer carga de tabelas (ping) utilizando por chave o numero lógico ja configurado, se o resultado for OK o pedido de venda no CRM terá o status alterado e Log anexado.
