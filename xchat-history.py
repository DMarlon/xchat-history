 # -*- coding: utf-8 -*-

__module_name__ = "xchat-history"
__module_version__ = "1.0"
__module_description__ = "Python module history"

#Comando será !send diainicial horainicial diafinal horafinal
#Exemplo      !send 02-01-2014 13:57 17-03-2014 17:07

import xchat
import datetime
import smtplib

def message_cb(word, word_eol, userdata):
    #Recupera a mensagem enviada
    comando = word[1]
    #Cria um vetor com cada palavra
    messages = comando.slit(" ")
    #Verifica se ela e igual a !send
    if(messages[0] == "!send"):
        recuperalog(messages[1], messages[2], messages[3], messages[4])

def enviaemail():
    smtp = smtplib.SMTP('smtp.gmail.com:587')
    #ativando o ssl
    #inicia a troca de dados om o servidor
    smtp.ehlo()
    #ativa o tls
    smtp.starttls()
    #reinicia a troca de dados
    smtp.ehlo()
    smtp.login('seuemail@gmail.com', 'senha')
    smtp.sendmail('seuemail@gmail.com','destinatario@server.com',
	'''To: destinatario@server.com
	From: seuemail@server.com
	Subject: Assunto aqui
	Aqui vai o corpo da mensagem''')
    smtp.quit()

def recuperalog(diainicial,horainicial, diafinal, horafinal):
    #Recupera o arquivo de log
    arquivo = open("/home/Marlon/.config/xchat2/scrollback/FreeNode/#oesc-livre.txt")
    #Recupera as linhas do texto
    text = arquivo.readlines()
    #Variaveis para determinar a linha inicial e final
    linhainicio = 0
    linhafinal = 0
    #Loop para recuperar a linha inicial e final de ontem o historico deve ser copiado
    for linha, valor in enumerate(text):
        #Recupera a hora e a data da linha do arquivo de log
        dia = datetime.datetime.fromtimestamp(int(valor[2:13])).strftime('%d-%m-%Y')
        hora = datetime.datetime.fromtimestamp(int(valor[2:13])).strftime('%H:%M')
        #Verifica se são iguais as datas e horas necessarias
        #Se forem marca as variaveis com os valores
        if (hora == horainicial) and (dia == diainicial):
            linhainicio = linha
        elif(hora == horafinal) and (dia == diafinal):
            linhafinal = linha
    #Se ele encontrou logo para a hora especificada
    #Cria uma nova lista com os log da conversa sem as datas e horas
    if(linhainicio != 0 and linhafinal != 0):
        novalista = text[linhainicio:linhafinal]
        for linha in novalista:
            print linha[14:-1]
        enviaemail()
    #Fecha o arquivo para liberalo da memoria.
    arquivo.close()


