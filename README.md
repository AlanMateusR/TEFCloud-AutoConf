# TEF-Cloud-AutoConf

## Projeto composto por software RPA & Web-Scraping que tem por objetivo automatizar configurações diversas em um servidor dedicado com base em dados de um CRM.

 * **Projeto:** Automatização de longas tarefas complexas e manuais em um ambiente com servidor nuvem dedicado, tudo com base em dados de um CRM comunicando-se por meio de API.
 * **Arquivos:** LogicoConf.py | BandeiraCargaConf.py | CargaConfAndLog.py | get_session.py | imap.py | credentials.env 
 * **Status do projeto:** Entregue

 
 * **Escopo:** Empresa disponibiliza serviços de suporte para integração no escopo de TEF (Transferencia eletronica de fundos) e vende a propria VPN e TLS para este fim. Cabe também ao integrador TEF do cliente a responsabilidade de preparar o ambiente TEF dos mesmos para possibilitar as devidas comunicações entre PDV (Ponto de venda/ERP) e Adquirente (operadora de cartão), seja por parametrização para padrão em vendas via TEF ou configurações diversas no escopo meio de pagamento.

 * **Problematica:** Colaboradores do setor técnico designado da empresa necessitam diariamente verificar uma lista de clientes no CRM da organização com status do pedido de venda em APROVADO, cujo significado é a necessidade de efetuar uma serie de configurações, parametrizações e testes em um ambiente nuvem dedicado afim de possibilitar uma integração cruzada entre servidores, tudo com base em um formulario que foi devidamente licenciado pelo setor comercial/financeiro, no CRM se encontram todos os dados que devem ser configurados MANUALMENTE um por um no ambiente reservado, no caso de conformidade entre todas as informações e se a integração for bem sucedida (comunicação online) o pedido de venda TEF do cliente deve passar a ter o status alterado para IMPLANTAÇÃO.
 * **Solução:** Software de teste automatizado foi programado para automatizar todo o procedimento de . Para o projeto foram concedidos acesso ao ambiente Fiserv (Sitef - integração TEF) para verificar relatorio de vendas e ainda as chaves de acesso para integração via API ao portal de CRM Gluo (baseado em Vtiger CRM).

  
 * **Autor:** Alan Mateus Rodrigues
 * **Data de Criação:** 25/02/2024
 * **Ramo da empresa:** Tecnologia em meios de pagamento

<br>

 ## !!! Adendo !!!
 * **Este código é disponibilizado no GitHub exclusivamente como parte do portfólio de programação do autor.**
* **O objetivo é demonstrar experiência e habilidades na área de programação.** 
* **Não é recomendada a reprodução, distribuição ou utilização deste código para qualquer finalidade.**

 >* Links, nomes e dados confidenciais foram censurados e a explicação tecnica do funcionamento do codigo foi resumida.
 >* Para mais informações, entre em contato com o autor em: alanmateusr@gmail.com
 >* www.linkedin.com/in/alan-rodrigues-983822218 

<br>

# || Resumo do Fluxo de funcionamento do script ||

* **1.** Primeiramente script efetua login no portal Fiserv e exporta uma planilha contendo dados de diversos clientes e seus respectivos dados de venda (quantidade de venda, valores etc) a informação essencial é o valor total de venda efetuados.
* **2.** Da planilha gerada é efetuada uma separação pra obter somente os clientes que venderam um valor diferente de R$ 0,00 para então resultar clientes que já venderam em algum momento (se já tiverem vendido qualquer valor então o produto de integração TEF já foi implantado).
* **3.** Script integra via API com CRM (Gluo) para efetuar requisições GET e registrar pelo menos 20 clientes que estão com pedido de vendas com status igual a "IMPLANTAÇÃO" (serão armazenados em .txt)
* **4.** Será efetuado merge para cruzamento de dados entre clientes que venderam um valor diferente de R$ 0,00 X Cliente com status em implantação, o resultado do cruzamento será a lista de clientes que não devem mais estar em implantação pois ja efetivaram pelo menos uma venda (será gerado outra lista em txt).
* **5.** Uma vez que for obtido a lista de clientes (Identificados com CNPJ) será enviado requisição novamente via API para alterar o status do pedido de venda de todos os cliente da lista para FINALIZADO.

<br>
<br>

