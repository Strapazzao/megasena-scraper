from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

def separa_ganhadores(lista_premi):
    dicionario_ganhadores = {'seis_dezenas_qtd':'',
                              'seis_dezenas_valor':0,

                              'cinco_dezenas_qtd':'',
                              'cinco_dezenas_valor':0,

                              'quatro_dezenas_qtd':'',
                              'quatro_dezenas_valor':0,
                              }

    seis_dezenas = lista_premi[0].split(',')
    cinco_dezenas = lista_premi[1].split(',')
    quatro_dezenas = lista_premi[2].split(',')
    
    dicionario_ganhadores['seis_dezenas_qtd'] = seis_dezenas[0].split(' ')[0]
    dicionario_ganhadores['cinco_dezenas_qtd'] = cinco_dezenas[0].split(' ')[0]
    dicionario_ganhadores['quatro_dezenas_qtd'] = quatro_dezenas[0].split(' ')[0]


    if len(seis_dezenas) > 1:
        dicionario_ganhadores['seis_dezenas_valor'] = int(''.join(seis_dezenas[1:]).replace("R$ ","").replace(".",""))/10
    if len(cinco_dezenas) > 1:
        dicionario_ganhadores['cinco_dezenas_valor'] = int(''.join(cinco_dezenas[1:]).replace("R$ ","").replace(".",""))/10
    if len(quatro_dezenas) > 1:
        dicionario_ganhadores['quatro_dezenas_valor'] = int(''.join(quatro_dezenas[1:]).replace("R$ ","").replace(".",""))/10

    return dicionario_ganhadores

options = Options()
options.add_argument("-headless")
navegador = Firefox(options= options)


url = 'https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx'

navegador.get(url)

concurso_atual = int(navegador.find_element(By.CSS_SELECTOR, "div.title-bar.clearfix span").text.split(' ')[1])

d = []
concurso = concurso_atual

navegador.switch_to.new_window('tab')
all_windows = navegador.window_handles

while True:
    

    navegador.switch_to.window(all_windows[0])

    WebDriverWait(navegador,timeout=20).until(
        lambda d: d.find_element(By.ID, "loading").value_of_css_property("display") == "none")

    cabecalho = navegador.find_element(By.CSS_SELECTOR, "div.title-bar.clearfix span")
    concurso = int(cabecalho.text.split(' ')[1])
    
    dezenas = navegador.find_elements(By.CSS_SELECTOR, "ul.numbers.megasena li")

    lista_dezena = [int(dezena.text) for dezena in dezenas]

    concurso = int(cabecalho.text.split(' ')[1])

    data_resultado = datetime.strptime(cabecalho.text.split(' ')[2]
                                       .replace("(","")
                                       .replace(")",""),"%d/%m/%Y")

    acumulou = navegador.find_element(By.CSS_SELECTOR, 'h3.epsilon[ng-show="resultado.acumulado"]').get_attribute("class") == 'epsilon'

    ganhadores = navegador.find_elements(By.CSS_SELECTOR,'span[ng-show*="faixaPremiacao.numeroDeGanhadores"]')
    lista_premi = [elem.text for elem in ganhadores if elem.text.strip()]

    ganhadores_separados = separa_ganhadores(lista_premi)
 
    
    
    infos_concurso = {'concurso':concurso,'data_resultado':data_resultado,
                      'numeros_sorteados':lista_dezena,'acumulou':acumulou,
                      }
    infos_concurso.update(ganhadores_separados)

    d.append(infos_concurso)

    print(concurso)

    if concurso == 1:
            break
    else:
        concurso -= 1 
        
    buscador_consurso = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID,'buscaConcurso')))
    buscador_consurso.clear()
    buscador_consurso.send_keys(concurso)
    buscador_consurso.send_keys(Keys.ENTER)


df = pd.DataFrame(d)
df.to_parquet('./data/sorteios.parquet')