import pyautogui
import keyboard
import time

import pytesseract
from PIL import Image
from PIL import ImageEnhance, ImageFilter

import os

class FindGroup:

    def click_position_screen(x, y):
        
        time.sleep(0.1)
        # Move o mouse para as coordenadas (x, y) e clica
        pyautogui.click(x, y)

    def write_keyboard(text):

        time.sleep(0.1)

        pyautogui.typewrite(text, interval=0.1)

    def press_enter():

        # Pressiona a tecla "Enter"
        keyboard.press("enter")
        time.sleep(0.1)  # Aguarda um pequeno intervalo
        keyboard.release("enter")

    def visualize_mouse_position(self):
        # Loop para imprimir coordenadas enquanto o mouse se move
        while True:
            x, y = pyautogui.position()
            print(f'X: {x}, Y: {y}')

    def recognize_number(self):

        print('RECOGNIZING.....')

        current_folder = os.getcwd()
        # print('\n current_folder: ', current_folder)

        full_desired_path = "C:/Users/win - 10/Documents/financial-applications/k-ri-k-robot/files"
        # print('\n full_desired_path: ', full_desired_path)

        if(current_folder != full_desired_path):
            os.chdir(full_desired_path)

        # Configura o idioma para português e ajusta para reconhecimento de números
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\win - 10\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' # caminho para o executável do Tesseract OCR
        config = r'--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'  # Configura para reconhecimento de números apenas

        # Abrir imagem
        imagem = Image.open("number.png")
        
        imagem = imagem.convert("RGB")
        
        # Aplicar aumento de contraste
        contraste = ImageEnhance.Contrast(imagem)
        imagem = contraste.enhance(2.0)  # Ajuste o fator de contraste conforme necessário

        # Aplicar filtro para remover ruído
        imagem = imagem.filter(ImageFilter.MedianFilter(size=3))

        # Salvar imagem pré-processada
        imagem.save("number.png")

        # Utiliza OCR para extrair texto da imagem (reconhecimento de números)
        numero_texto = pytesseract.image_to_string(Image.open("number.png"), config=config)

        # Verifica se a string não está vazia
        if numero_texto.strip():
            numero = int("".join(filter(str.isdigit, numero_texto)))
            
            # Imprime o número
            print("Número encontrado:", numero)
        else:
            print("Nenhum número foi reconhecido.")

        return numero


    def find_vacancy(self):

        print('FINDING.....')

        #posição do elemento pesquisar do windows
        FindGroup.click_position_screen(x = 139, y = 1057)

        time.sleep(1)
        FindGroup.write_keyboard('chrome')

        time.sleep(3)
        #posição do ícone do chrome
        FindGroup.click_position_screen(x = 168, y = 372)

        time.sleep(1)
        
        pyautogui.hotkey('win', 'up')
        
        FindGroup.write_keyboard('https://www.consorcioservopa.com.br/vendas/login')

        FindGroup.press_enter()

        time.sleep(3)
        #posição do continuar do chrome maximizado
        FindGroup.click_position_screen(x = 958, y = 817)


        time.sleep(5)
        #clicar no acesso Ferramenta Administrativa
        FindGroup.click_position_screen(x = 193, y = 813)

        
        time.sleep(2)
        #clicar no acesso Grupos
        FindGroup.click_position_screen(x = 152, y = 941)

        
        time.sleep(5)
        #clicar no marcador Sem Embutido
        FindGroup.click_position_screen(x = 789, y = 540)

        
        time.sleep(2)
        #clicar no text Numero Grupo
        FindGroup.click_position_screen(x = 1530, y = 526)
        

        FindGroup.write_keyboard('3410')

        time.sleep(1)
        #clicar no acesso Buscar
        FindGroup.click_position_screen(x = 1755, y = 523)
        
        time.sleep(5)
        
    def printing_number(self):

        print('PRINTING.....')

        # Captura uma área da tela onde está o número
        x1, y1, x2, y2 = 1502, 876, 1559, 912  # coordenadas da área de captura
        screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))

        current_folder = os.getcwd()
        # print('\n current_folder: ', current_folder)

        full_desired_path = "C:/Users/win - 10/Documents/financial-applications/k-ri-k-robot/files"
        
        # print('\n full_desired_path: ', full_desired_path)

        if(current_folder != full_desired_path):
            os.chdir(full_desired_path)

        print('SAVING.....')
        screenshot.save("number.png")
        
        pyautogui.hotkey('alt', 'F4')














if __name__ == "__main__":

    print('STARTING.....')

    find_group = FindGroup()

    find_group.find_vacancy()

    time.sleep(5)

    find_group.printing_number()
    
    time.sleep(5)

    find_group.recognize_number()

    # find_group.visualize_mouse_position()
    

