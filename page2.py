import smtplib
import requests
import hashlib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# URL do site que você deseja monitorar
url = 'https://time.is/Fortaleza'

# Configuração do e-mail (Outlook)
smtp_server = 'smtp-mail.outlook.com'
smtp_port = 587
smtp_login = 'suzanadirra@hotmail.com'  # Seu e-mail do Outlook
smtp_password = 'ThisIsSuzy24'  # Sua senha de login ou senha de aplicativo se a 2FA estiver ativada
email_sender = 'suzanadirra@hotmail.com'  # O remetente é o seu login SMTP
email_receiver = 'rfl.brc@gmail.com'  # Destinatário do e-mail

# Função para calcular o hash do HTML da página
def get_page_hash():
    # Enviar requisição para o site
    response = requests.get(url)
    page_html = response.text
    
    # Gerar um hash do conteúdo HTML para comparações
    return hashlib.md5(page_html.encode('utf-8')).hexdigest()

# Função para enviar e-mail
def send_email(subject, body):
    try:
        # Configurar o servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Iniciar uma conexão segura TLS
        
        # Fazer login na conta de e-mail
        server.login(smtp_login, smtp_password)
        
        # Configurar o e-mail
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject
        
        # Corpo do e-mail
        msg.attach(MIMEText(body, 'plain'))
        
        # Enviar o e-mail
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()
        
        print('E-mail enviado com sucesso!')
    except Exception as e:
        print(f'Erro ao enviar o e-mail: {e}')

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
            send_email(
                subject=f'Alteração no site: {url}', 
                body=f'O conteúdo do site {url} foi alterado.')
            
            # Atualizar o hash armazenado
            with open("previous_hash.txt", "w") as file:
                file.write(current_hash)
        
        else:
            print("Nenhuma alteração detectada.")

        # Aguardar 30 segundos antes de verificar novamente
        time.sleep(60)

# Rodando o monitoramento
if __name__ == "__main__":
    monitor()
