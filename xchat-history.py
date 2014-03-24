 # -*- coding: utf-8 -*-

__module_name__ = "xchat-history"
__module_version__ = "1.0"
__module_description__ = "Python module history"

#Comando será !send diainicial horainicial diafinal horafinal
#Exemplo      !send 02-01-2014 13:57 17-03-2014 17:07

import xchat
import datetime
import smtplib
from email.MIMEText import MIMEText


def message_cb(word, word_eol, userdata):
    #Recupera a mensagem enviada 
    comando = word[1]
    #Cria um vetor com cada palavra
    messages = comando.split(" ")
    #Verifica se ela e igual a !send
    if(messages[0] == "!send"):
        recuperalog(messages[1], messages[2], messages[3], messages[4])

def enviaemail(mensagem):
    #Usado os site abaixo como referencia
    #http://www.vivaolinux.com.br/dica/Enviando-email-com-Python-e-autenticacao-no-SMTP-pelo-Linux
    #http://rafapinheiro.wordpress.com/2009/02/22/enviando-e-mail-com-python-pelo-gmail/

    #Cria a mensagem a ser enviada
    msg1 = MIMEText("%s"% mensagem)
    #Titulo da mensagem
    msg1['Subject']='Aqui vai o titulo do e-mail Ex. Conversa no canal #OeSC-Livre'
    #Destino e destinatario    
    msg1['From']="seuemail@servidor.com"
    msg1['To']="destinatario@servidor.com"
    #ativando o ssl
    #O caminho SMTP é do gmail(Mas pode ser alterado para o de sua preferencia)
    smtp = smtplib.SMTP('smtp.gmail.com:587')
    #inicia a troca de dados om o servidor
    smtp.ehlo()
    #ativa o tls
    smtp.starttls()
    #reinicia a troca de dados
    smtp.ehlo()
    #Efetua o login
    smtp.login('seuemail@server.com', 'senha')
    #Envia o e-mail
    smtp.sendmail('seuemail@server.com','destinatario@server.com',msg1.as_string())
    #Fecha a conexao
    smtp.quit()

def recuperalog(diainicial,horainicial, diafinal, horafinal):
    #Recupera o arquivo de log
    #Deve ser alterado o caminho em open para o seu arquivo de backup do xchat
    arquivo = open("/home/Marlon/.config/xchat2/scrollback/FreeNode/#oesc-livre.txt")
    #Recupera as linhas do texto
    text = arquivo.readlines()
    #Variaveis para determinar a linha inicial e final
    linhainicio = 0
    linhafinal = 0
    #Loop para recuperar a linha inicial e final de onde o historico deve ser copiado
    for linha, valor in enumerate(text):
        #Recupera a hora e a data de uma linha do arquivo de log
        dia = datetime.datetime.fromtimestamp(int(valor[2:13])).strftime('%d-%m-%Y')
        hora = datetime.datetime.fromtimestamp(int(valor[2:13])).strftime('%H:%M')	
        #Verifica se as datas e horas solicitadas para serem enviadas existem no log
        #Se existirem marca a linha aonde comeca e onde termina
        if (hora == horainicial and dia == diainicial):
            linhainicio = linha
        elif(hora == horafinal and dia == diafinal):
            linhafinal = linha
    #Se ele encontrou log para a hora e data solicitada
    #Cria uma nova lista com os log da conversa sem as datas e horas
    if(linhainicio != 0 and linhafinal != 0):
        novalista = text[linhainicio:linhafinal]
	#inicia a varial que vai ser passada para o e-mail
	mensagemfinal = ""
	#O for vai montar uma string com todo o log da conversa
	for linha in novalista:
            mensagemfinal += linha[14:-1] + '\n'
	#Apos montar a string passa a mensagem de log como parametro para o email
        enviaemail(mensagemfinal)   
    #Fecha o arquivo de log.
    arquivo.close()

xchat.prnt("Plugin carregado com sucesso");
xchat.hook_print("Channel Message", message_cb)
xchat.hook_print("Your Message", message_cb)
xchat.hook_print("Private Message to Dialog", message_cb)





