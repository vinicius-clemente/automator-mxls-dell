# automator-mxls-dell

Automated Python tool to clear duplicate/stuck dynamic MAC addresses on Dell MXL switches and validate host connectivity via ICMP ping.



\# Automator MXLs Dell (MAC Table Cleaner \& Connectivity Validator)



Ferramenta de automacao desenvolvida em Python para resolucao rapida de problemas de conectividade causados por MAC addresses duplicados ou travados na tabela CAM de switches Dell MXL, executando a limpeza remota e validando automaticamente o retorno do servidor via ping.



\## Como Funciona



1\. \*\*Conexao SSH em Lote:\*\* Autentica-se sequencialmente nos switches Dell MXL listados no arquivo de inventario.

2\. \*\*Limpeza da Tabela MAC:\*\* Executa o comando `clear mac-add dyn add <MAC>` para remover entradas dinamicas travadas ou duplicadas.

3\. \*\*Desconexao Segura:\*\* Encerra a sessao SSH (`disconnect`) imediatamente apos o comando para liberar as linhas VTY do equipamento.

4\. \*\*Validacao de Conectividade:\*\* Dispara pacotes ICMP (`ping -c 10`) diretamente a partir do Jump Host Linux para confirmar que o IP do servidor voltou a responder.



\## Tecnologias Utilizadas



\- \*\*Python 3.x\*\*

\- \*\*Netmiko / Paramiko:\*\* Automacao de sessoes SSH e tratamento de excecoes de rede (timeouts, falhas de autenticacao e erros de protocolo).

\- \*\*OS / ICMP:\*\* Validacao de conectividade ponta a ponta apos a intervencao.



\## Como Utilizar



1\. Clone o repositorio:

&#x20;  ```bash

&#x20;  git clone \[https://github.com/vinicius-master/automator-mxls-dell.git](https://github.com/vinicius-master/automator-mxls-dell.git)

&#x20;  cd automator-mxls-dell

