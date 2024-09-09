import schedule
import time
from automacao_email import enviaEmail
from automacao import geraHtmlDosProcessosJuntos
from automacao import atualizaHtmlDosProcessosNoBD
from processoModel import Processo

def adicionarNovoProcesso():
    Processo.new(
        input("Digite o número do processo: "), 
        input("Digite o link do processo: "),
        tribunal=input("Digite o tribunal: "),
        separado=bool(input("Digite se a movimentação é separada ou não: "))
    )
    Processo.save()
def consultarProcessos():
    print("-=" * 30)
    print("Os processos incluídos no banco de dados são:")
    for processo in Processo.list_by('numero_processo'):
        print(processo[0])
    print("-=" * 30)

def excluirProcesso():
    Processo.delete_by_numero_processo(input("Digite o número do processo: "))
    Processo.save()

def continuar():
    while True:
        resposta = input("Deseja continuar? [S/N] ")
        if resposta.upper() == "S":
            return True
        elif resposta.upper() == "N":
            return False
        else:
            print("Digite uma opção válida!")

def rotinaEmails():
    print("Verificando os processos...")
    atualizaHtmlDosProcessosNoBD()
    enviaEmail(geraHtmlDosProcessosJuntos(), "Acompanhamento Diário STJ")
    for processo in Processo.separados():
        enviaEmail(processo[3], f"Acompanhamento Diário STJ - Processo {processo[0]}")

schedule.every().day.at("14:49").do(rotinaEmails)
while True:
    schedule.run_pending()
    time.sleep(60)

    # print("-=" * 30)
    
    # print('''
    # Bem vindo ao HUB da automação de Acompanhamento Processual
    # Digite o número da opção desejada:
    # [ 1 ] Adicionar novo processo
    # [ 2 ] Enviar e-mail de acompanhamento diário
    # [ 3 ] Consultar processos já incluídos
    # [ 4 ] Excluir processo da nossa Base de dados
    # [ 5 ] Sair
    #       ''')
    # print("-=" * 30)
    # resposta = input()
    # match resposta:
    #     case '1': 
    #         adicionarNovoProcesso()
    #         if not continuar():
    #             break
    #     case '2': 
    #         rotinaEmails()
    #         if not continuar():
    #             break
    #     case '3': 
    #         consultarProcessos()
    #         if not continuar():
    #             break
    #     case '4': 
    #         excluirProcesso()
    #         if not continuar():
    #             break
    #     case '5': break
    #     case _: print("Digite uma opção válida!")
