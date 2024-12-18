import requests
import hashlib
import time
import subprocess

# URL do site que você deseja monitorar
url = 'https://time.is/Fortaleza'

# Função para calcular o hash do HTML da página
def get_page_hash():
    # Enviar requisição para o site
    response = requests.get(url)
    page_html = response.text
    
    # Gerar um hash do conteúdo HTML para comparações
    return hashlib.md5(page_html.encode('utf-8')).hexdigest()

# Função para enviar notificação para o Termux (telefone)
def send_notification(message):
    # Usando o comando 'termux-notification' para exibir a notificação no Termux
    subprocess.run(['termux-notification', '--title', 'Alerta de Mudança no Site', '--content', message, '--priority', 'high'])

# Função principal para monitorar periodicamente
def monitor():
    try:
        # Tentar ler o hash armazenado da página
        with open("previous_hash.txt", "r") as file:
            previous_hash = file.read().strip()
    except FileNotFoundError:
        previous_hash = None

    while True:
        current_hash = get_page_hash()  # Obter o hash atual da página
        
        # Comparar o hash atual com o anterior
        if current_hash != previous_hash:
            print("Alteração detectada no site!")
            send_notification(f'O conteúdo do site {url} foi alterado.')  # Enviar notificação para o telefone
            
            # Atualizar o hash armazenado
            with open("previous_hash.txt", "w") as file:
                file.write(current_hash)
        
        else:
            print("Nenhuma alteração detectada.")

        # Aguardar 10 minutos antes de verificar novamente
        time.sleep(30)

# Rodando o monitoramento
if __name__ == "__main__":
    monitor()
