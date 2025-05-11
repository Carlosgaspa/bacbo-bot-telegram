
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import telegram

# Configurações do Telegram
TOKEN = "8176352743:AAFrr_sx9yjv9e2HuTfdrwDi8Oba37MfqEA"
CHAT_ID = "1002328051434"
bot = telegram.Bot(token=TOKEN)

# Função para enviar sinal formatado
def enviar_sinal(cor):
    cor_emoji = {"azul": "🔵", "vermelho": "🔴", "verde": "🟢"}.get(cor, "🎲")
    mensagem = (
        "🧠 *Analisando próxima jogada...*\n\n"
        "👮‍♂️ *ENTRADA CONFIRMADA*\n"
        f"🎲 apostar na cor {cor_emoji}\n"
        "🟠 proteger o empate\n"
        "💬 fazer até 2 gales"
    )
    bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode=telegram.ParseMode.MARKDOWN)

# Configuração do navegador
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

# Acessa o site da Rokubet e começa o monitoramento
driver.get("https://www.rokubet.com/casino/game/bacbo")

def obter_resultado():
    try:
        elementos = driver.find_elements(By.CLASS_NAME, "recent-numbers__number")
        if len(elementos) >= 2:
            dados = [int(el.text.strip()) for el in elementos[:2]]
            return dados
    except:
        return None

ultimos = []

while True:
    resultado = obter_resultado()
    if resultado and resultado != ultimos:
        ultimos = resultado
        print("Novo resultado:", resultado)
        if resultado[0] > resultado[1]:
            enviar_sinal("azul")
        elif resultado[0] < resultado[1]:
            enviar_sinal("vermelho")
        else:
            enviar_sinal("verde")
    time.sleep(10)
