# Automator MXLs Dell (MAC Table Cleaner & Connectivity Validator)

Ferramenta de automação desenvolvida em Python para resolução rápida de problemas de conectividade causados por MAC addresses duplicados ou travados na tabela CAM de switches Dell MXL, executando a limpeza remota e validando automaticamente o retorno do servidor via ping.

## Como Funciona

1. **Conexão SSH em Lote:** Autentica-se sequencialmente nos switches Dell MXL listados no arquivo de inventário.
2. **Limpeza da Tabela MAC:** Executa o comando `clear mac-add dyn add <MAC>` para remover entradas dinâmicas travadas ou duplicadas.
3. **Desconexão Segura:** Encerra a sessão SSH (`disconnect`) imediatamente após o comando para liberar as linhas VTY do equipamento.
4. **Validação de Conectividade:** Dispara pacotes ICMP (`ping -c 10`) diretamente a partir do Jump Host Linux para confirmar que o IP do servidor voltou a responder.

## Tecnologias Utilizadas

- **Python 3.x**
- **Netmiko / Paramiko:** Automação de sessões SSH e tratamento de exceções de rede (timeouts, falhas de autenticação e erros de protocolo).
- **OS / ICMP:** Validação de conectividade ponta a ponta após a intervenção.

## Como Utilizar

1. Clone o repositório:

       git clone https://github.com/vinicius-clemente/automator-mxls-dell.git
       cd automator-mxls-dell

2. Instale as dependências:

       pip install -r requirements.txt

3. Adicione os endereços IP dos switches Dell MXL no arquivo `devices.txt`.

4. Execute o script e informe os dados solicitados (usuário, senha, MAC address no formato `XX:XX:XX:XX:XX:XX` e o IP do servidor para validação):

       python clear-mac-mxl.py

   *(Ajuste o nome do arquivo `.py` conforme o script principal da pasta).*

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
