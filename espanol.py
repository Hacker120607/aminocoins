import string, random, requests, secmail, pyshorteners
from aminofix import Client
from bs4 import BeautifulSoup
from time import sleep
from aminofix.lib.util.exceptions import ActionNotAllowed, IncorrectVerificationCode
from aminofix.lib.util import deviceId as device


def captcha(url):
    return requests.post("https://captcha-do-mega.herokuapp.com/", data={"text": url}).json()['captcha']


def gerar_email():
    def gerar_aleatorio(size=16, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    email = "xmega-" + gerar_aleatorio() + "@wwjmp.com"
    return email


def deviceId():
    return device()


def get_link(email):
    try:
        mail = secmail.SecMail()
        sleep(2.5)
        inbox = mail.get_messages(email)
        for Id in inbox.id:
            msg = mail.read_message(email=email, id=Id).htmlBody
            bs = BeautifulSoup(msg, 'html.parser')
            images = bs.find_all('a')[0]
            url = (images['href'])
            if url is not None:
                return url
    except:
        pass


def encurtar_link(link):
    ps = pyshorteners.Shortener()
    return ps.tinyurl.short(fr"{link}")


def log(cli: Client, email, password, device):
    try:
        cli.login(email, password)
        SID = f"{cli.sid}"
        with open("accounts.json", 'a') as x:
            acc = f'\n{{\n"email": "{email}",\n"password": "{password}",\n"device": "{device}",\n"SID": "{SID}"\n}},'
            x.write(acc)
            print(">> Cuenta guardada! <<")

    except Exception as b:
        print(b)


def reset_dj():
    with open("device.json", 'w') as x:
        x.close()


def threadit(password):
    print("\n[ADVERTENCIA] Puedes crear 5 cuentas por VPN")
    contador = 0
    while True:
        reset_dj()
        try:
            if contador == 5:
                print("¡Cambia la VPN para seguir creando cuentas!")
                break

            email = gerar_email()
            device = deviceId()
            print(f"\nGerando email {email}...")
            client = Client(device)
            client.request_verify_code(email)
            link = get_link(email)
            print(link)
            codigo = captcha(link)
            print(codigo)
            client.register(nickname="XMEGABOTS", email=email, password=password, verificationCode=codigo, deviceId=device)

            log(client, email, password, device)
            contador += 1

        except IncorrectVerificationCode:
            print("Código incorrecto")

        except ActionNotAllowed:
            print("¡Cambia la VPN para seguir creando cuentas!")
            break

        except Exception as g:
            print(g)
