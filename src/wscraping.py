from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class WebScraping:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.todas_frutas = []
        self.estoque = []
    
    def todasFrutas(self):
        frutas = []

        self.driver.get("https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22")
        linhas = self.driver.find_element(By.CLASS_NAME, "article-table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            nomeFruta = colunas[1].find_element(By.TAG_NAME, "a").get_attribute("title")
            frutas.append(nomeFruta)
        
        self.todas_frutas = frutas
        
        self.driver.quit()

        hora = 0
        min = 0
        
        while True:
            tempo = time.localtime()
            if tempo.tm_min == min and tempo.tm_hour == hora:
                frutas = []
                self.driver.get("https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22")
                linhas = self.driver.find_element(By.CLASS_NAME, "article-table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
                
                for linha in linhas:
                    colunas = linha.find_elements(By.TAG_NAME, "td")
                    nomeFruta = colunas[1].find_element(By.TAG_NAME, "a").get_attribute("title")
                    frutas.append(nomeFruta)
                
                self.todas_frutas = frutas
                
                self.driver.quit()
            time.sleep(25)
    
    def buscarFrutas(self):
        self.estoque = []

        self.driver.get("https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22")
        figures = self.driver.find_elements(By.CLASS_NAME, "thumb")
        
        frutas = []
        
        for e in figures:
            if e.find_element(By.TAG_NAME, "a").get_attribute("href")[36:] in frutas: break
            else: frutas.append(e.find_element(By.TAG_NAME, "a").get_attribute("href")[36:])
        
        self.driver.quit()
        
        self.estoque = frutas

        horas = [[1, 10], [5, 10], [9, 10], [13, 10], [17, 10], [21, 10]]
        while True:
            tempo = time.localtime()
            if [tempo.tm_hour, tempo.tm_min] in horas:
                self.driver.get("https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22")
                figures = self.driver.find_elements(By.CLASS_NAME, "thumb")
                
                frutas = []
                
                for e in figures:
                    if e.find_element(By.TAG_NAME, "a").get_attribute("href")[36:] in frutas: break
                    else: frutas.append(e.find_element(By.TAG_NAME, "a").get_attribute("href")[36:])
                
                self.driver.quit()
                
                self.estoque = frutas
            time.sleep(25)