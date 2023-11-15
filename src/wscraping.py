from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
import time

class WebScraping:
    def __init__(self):
        self.end_thread = False
        self.todas_frutas = []
        self.estoque = []
    
    def todasFrutas(self):
        """
        This function is responsible for searching for all the fruits in the game on the website https://blox-fruits.fandom.com/wiki/Blox_Fruits_Wiki and updating the list of all fruits.

        Parameters:
            self: An instance of the class.
        
        Returns:
            None
        """
        frutas = []

        driver = webdriver.Chrome()
        driver.get("https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22")
        driver.implicitly_wait(5)

        linhas = driver.find_element(By.CLASS_NAME, "article-table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            nomeFruta = colunas[1].find_element(By.TAG_NAME, "a").get_attribute("title")
            frutas.append(nomeFruta)
        
        self.todas_frutas = frutas
        driver.quit()

        hora = 0
        min = 0
        while not self.end_thread:
            tempo = time.localtime()
            if tempo.tm_min == min and tempo.tm_hour == hora:
                frutas = []
                driver = webdriver.Chrome()
                driver.get("https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22")
                driver.implicitly_wait(5)
                
                linhas = driver.find_element(By.CLASS_NAME, "article-table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
                for linha in linhas:
                    colunas = linha.find_elements(By.TAG_NAME, "td")
                    nomeFruta = colunas[1].find_element(By.TAG_NAME, "a").get_attribute("title")
                    frutas.append(nomeFruta)
                
                self.todas_frutas = frutas
                driver.quit()
            time.sleep(25)
    
    def buscarFrutas(self):
        """
        This function is responsible for searching for fruits on Blox Fruits Fandom Wiki(https://blox-fruits.fandom.com/wiki/Blox_Fruits_Wiki) website and updating the stock.

        Args:
            self: The instance of the class.

        Returns:
            None
        """
        self.estoque = []

        driver = webdriver.Chrome()
        driver.get("https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22")
        driver.implicitly_wait(5)
        
        figures = driver.find_elements(By.CLASS_NAME, "thumb")
        frutas = []
        for e in figures:
            if e.find_element(By.TAG_NAME, "a").get_attribute("href")[36:] in frutas: break
            else: frutas.append(e.find_element(By.TAG_NAME, "a").get_attribute("href")[36:])
        
        driver.quit()
        self.estoque = frutas

        horas = [[1, 10], [5, 10], [9, 10], [13, 10], [17, 10], [21, 10]]
        while not self.end_thread:
            tempo = time.localtime()
            if [tempo.tm_hour, tempo.tm_min] in horas:
                driver = webdriver.Chrome()
                driver.get("https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22")
                driver.implicitly_wait(5)

                figures = driver.find_elements(By.CLASS_NAME, "thumb")
                frutas = []
                for e in figures:
                    if e.find_element(By.TAG_NAME, "a").get_attribute("href")[36:] in frutas: break
                    else: frutas.append(e.find_element(By.TAG_NAME, "a").get_attribute("href")[36:])
                
                driver.quit()
                self.estoque = frutas
            time.sleep(25)
    
    def setUp(self):
        self.todas = Thread(target=self.todasFrutas)
        self.buscar = Thread(target=self.buscarFrutas)
        self.todas.start()
        self.buscar.start()
    
    def endThreads(self):
        self.end_thread = True
        self.todas.join()
        self.buscar.join()