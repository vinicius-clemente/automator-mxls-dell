#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################################
#                                                                          #
# NOME - AUTOMATOR CLEAR MAC MXLS DELL                                     #
# AUTOR - VINICIUS CLEMENTE                                                #
# DATA - 03/03/21                                                          #
# DESCRIPTION - ESSE ROBO TEM COMO FACILITAR AS TAREFAS COMO DAR UM CLEAR  #
# MAC NAS MXLS DELL, AUTOMATIZANDO O PROCESSO DEPOIS ELE DESLOGA DAS MXLS  #
# E FAZ A VALIDAÇÃO PINGANDO O IP PARA VERIFICAR SE ESTÁ RESPONDENDO E FOI #
# EFETIVO O CLEAR NO MAC                                                   #
#                                                                          #
############################################################################

# ==============================================================================
# IMPORTAÇÃO DE BIBLIOTECAS
# ==============================================================================
from getpass import getpass  # Permite digitar a senha no terminal de forma oculta (sem exibir caracteres)
from netmiko import ConnectHandler  # Módulo principal para gerenciar conexões SSH com ativos de rede
from netmiko.ssh_exception import NetMikoTimeoutException, AuthenticationException  # Exceções específicas de rede/login
from paramiko.ssh_exception import SSHException  # Exceções de protocolo SSH subjacente
import os  # Permite executar comandos diretamente no sistema operacional (Jump Host Linux)

# ==============================================================================
# ENTRADA DE DADOS (INPUTS DO OPERADOR)
# ==============================================================================
username = input('Enter your SSH username: ')  # Solicita o usuário de acesso aos switches
password = getpass()  # Solicita a senha de forma segura e oculta
mac = input('Enter mac-address (format XX:XX:XX:XX:XX:XX): ')  # MAC address a ser limpo da tabela CAM
IPSET = input('IP do servidor: ')  # IP de destino para validar a conectividade após a limpeza

# ==============================================================================
# LEITURA DO INVENTÁRIO DE EQUIPAMENTOS
# ==============================================================================
# Abre o arquivo de texto com a lista de IPs dos switches MXL e carrega cada linha em uma lista
with open('devices_file_MXL-SWs.txt') as f:
    devices_list = f.read().splitlines()

# ==============================================================================
# LOOP DE EXECUÇÃO POR EQUIPAMENTO
# ==============================================================================
for devices in devices_list:
    # Ignora linhas em branco ou linhas comentadas com '#' no arquivo de inventário
    if not devices.strip() or devices.startswith('#'):
        continue

    print('\nConnecting to device: ' + devices)
    ip_address_of_device = devices

    # Dicionário com os parâmetros de conexão exigidos pelo Netmiko
    ios_device = {
        'device_type': 'cisco_ios',  # Driver utilizado para interpretar o CLI do equipamento
        'ip': ip_address_of_device,
        'username': username,
        'password': password
    }

    # ==========================================================================
    # ESTABELECIMENTO DA SESSÃO SSH E TRATAMENTO DE ERROS
    # ==========================================================================
    try:
        net_connect = ConnectHandler(**ios_device)  # Inicia a conexão SSH desempacotando o dicionário
    except AuthenticationException:
        print('Authentication failure: ' + ip_address_of_device)  # Erro de usuário ou senha incorretos
        continue
    except NetMikoTimeoutException:
        print('Timeout to device: ' + ip_address_of_device)  # Equipamento inacessível ou porta SSH filtrada
        continue
    except EOFError:
        print(
            'End of file while attempting device ' + ip_address_of_device)  # Conexão encerrada abruptamente pelo equipamento
        continue
    except SSHException:
        print(
            'SSH Issue. Are you sure SSH is enabled? ' + ip_address_of_device)  # Falha na negociação SSH (ex: algoritmo incompatível)
        continue
    except Exception as unknown_error:
        print('Some other error: ' + str(unknown_error))  # Captura qualquer outro erro imprevisto sem parar o loop
        continue

    # ==========================================================================
    # EXECUÇÃO DOS COMANDOS E VALIDAÇÃO DE CONECTIVIDADE
    # ==========================================================================
    # 1. Envia o comando para limpar o MAC address dinâmico específico na tabela do switch
    output = net_connect.send_command('clear mac-add dyn add ' + mac)
    print(output)
    print('MAC limpo com sucesso no switch:', ip_address_of_device)

    # 2. Encerra a sessão SSH com o switch para liberar recursos (VTY lines)
    net_connect.disconnect()

    # 3. Dispara 10 pacotes ICMP (ping) a partir do Jump Host Linux para validar o retorno do servidor
    print(f'Testando conectividade a partir do Jump Host para o servidor {IPSET}...')
    os.system('ping ' + IPSET + ' -c 10')
    print('-' * 40)  # Linha divisória visual no terminal entre um equipamento e outro