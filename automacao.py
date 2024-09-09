import time
from processoModel import Processo
from consts import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def geraHtmlFaseSTJ(driver):
    try:
        elementos = driver.find_elements(By.CLASS_NAME, 'classDivFaseLinha')
        htmlFases1 = [elemento.get_attribute('outerHTML') for elemento in elementos]
        htmlFasesDoDia = ['\n   <div style="background-color:#f1e501;">\n' + fase + '\n   </div>\n' for fase in htmlFases1 if HOJE in fase]
        if len(htmlFasesDoDia) < 5:
            htmlFases = ('\n').join(htmlFasesDoDia) + ('\n').join(htmlFases1[len(htmlFasesDoDia):5])
        else:
            htmlFases = ('\n').join(htmlFasesDoDia)
        return htmlFases
    except NoSuchElementException:
        print("Sistema do STJ está indisponível")
        return ""

def geraHtmlAbasSTJ(driver):
    try:
        elemento = driver.find_element(By.ID, 'idDivAbas')
        return elemento.get_attribute('outerHTML')
    except NoSuchElementException:
        print("Sistema do STJ está indisponível")
        return ""
    
def geraHtmlDescricaoSTJ(driver):
    try:
        elemento = driver.find_element(By.ID, 'idDescricaoProcesso')
        return elemento.get_attribute('outerHTML')
    except NoSuchElementException:
        print("Sistema do STJ está indisponível")
        return ""
    

def geraUltimoHtmlProcessoSTJ(numero_processo, htmlDescricao, htmlAbas, htmlFases):
    '''
    Gera o HTML do processo com as informações do STJ.
    O HTML gerado é uma réplica do site do STJ, mas com as informações 
    atualizadas e sem a necessidade de estar logado no site.
    
    :param numero_processo: Número do processo
    :param htmlDescricao: HTML da descrição do processo
    :param htmlAbas: HTML das abas do processo
    :param htmlFases: HTML das fases do processo
    :return: HTML emulado do processo das últimas 5 movimentações
    '''

    return '''
    <ul style="background-color:#f1e501;">
                    <li>''' + numero_processo + '''</li>
                </ul>
                <div>
                    ''' + htmlDescricao + '''
                </div>
                <div>
                    ''' + htmlAbas + '''
                </div>
                <div>
                    ''' + htmlFases + '''
                </div>
                <style type="text/css"> #idDescricaoProcesso {
                            background-color: #414f55;
                            background-repeat: no-repeat;
                            border-top: 1px solid #FFFFFF;
                            color: #FFFFFF;
                            font-weight: bold;
                            padding: 1em 0.25em 1em 0.25em;
                            text-align: center;
                        }
                        body {
                            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                            font-size: 14px;
                            line-height: 1.42857143;
                            color: #333;
                            background-color: #fff;
                        }
                        .classSpanFaseTexto {
                            vertical-align: top;
                            font-weight: bold;
                            padding: 0 0 0 0.5em;
                            display: inline-block;
                            max-width: 70%;
                            word-wrap: break-word;
                        }
                        .classDivFaseLinha {
                            border-bottom: 1px solid;
                            text-align: left;
                            margin: 0.25em;
                            padding: 0.25em 0;
                        }

                        .classDivConteudoPesquisaProcessual {
                            background-color: #FFFFFF;
                            clear: both;
                            font-size: 1em;
                            padding: 0.5em 0;
                            text-align: justify;
                            border: none;
                            min-height: 4em;
                            overflow: hidden;
                        }
                        #idDivAbas {
                            display: block;
                            background-color: #414f55;
                            font-size: 1.1em;
                            /* height: 1.7em; */
                            overflow: none;
                            padding: 0 0 0 5px;
                            border-style: none;
                            margin-bottom: -1px;
                        }
                </style>
    '''
# Inicializar o WebDriver (usando ChromeDriver como exemplo)
def geraHtmlDosProcessosJuntos():
    html = ''
    for processo in Processo.nao_separados():
        print(processo)
        html += processo[3]
    return HTML_CABECALHO_EMAIL+html+HTML_ASSINATURA_EMAIL

def atualizaHtmlDosProcessosNoBD():
    driver = webdriver.Chrome()
    lista_processos = Processo.list_by('numero_processo')

    for processo_bd in lista_processos:
        numero_processo = processo_bd[0]
        instancia_processo = Processo.find_by_numero_processo(numero_processo)
        try:
            driver.get(instancia_processo.link)
            match instancia_processo.tribunal:
                case Processo.STJ:
                    try:
                        bloco = driver.find_element(By.ID, 'idProcessoDetalhesBloco4')
                        ultimaMovimentacao = bloco.find_element(By.CLASS_NAME, 'classSpanDetalhesTexto')
                        dataUltimaMovimentacao = ultimaMovimentacao.text.split()[0]
                        if dataUltimaMovimentacao == HOJE or instancia_processo.ultimo_html == "":
                            ## procedimento se teve movimentação
                            htmlDescricao = geraHtmlDescricaoSTJ(driver)
                            htmlAbas = geraHtmlAbasSTJ(driver)
                            htmlFases = geraHtmlFaseSTJ(driver)
                            
                            html = geraUltimoHtmlProcessoSTJ(numero_processo, htmlDescricao, htmlAbas, htmlFases)

                            if instancia_processo.separado:
                                Processo.update_by_numero_processo(numero_processo, {'ultimo_html': HTML_CABECALHO_EMAIL+html+HTML_ASSINATURA_EMAIL, 'data_verificacao': HOJE})
                            else:
                                Processo.update_by_numero_processo(numero_processo, {'ultimo_html': html, 'data_verificacao': HOJE})
                            Processo.save()

                        else:
                            ## procedimento se não teve movimentação
                            print("Não teve nenhuma movimentação.")
                            Processo.update_by_numero_processo(numero_processo, {'data_verificacao': HOJE})
                            Processo.save()
                            continue
                    except NoSuchElementException:
                        print("Sistema do STJ está indisponível")
                    time.sleep(1)
                case Processo.STF:
                    print("Sistema não implementado ainda")
        except:
            print("Não conseguiu entrar acessar o link")
    driver.close()
