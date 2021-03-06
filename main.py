# This project automizes protocols for Outlook.
from time import sleep
from O365 import *
import re
from O365.message import Flag
from protocol_classes import *
from protocol_parser import *
import os
from threading import Thread
from queue import Queue

# Une application de Microsoft Azure est utilisée pour
# définir les portées du programme.
# client ID: 53d1a954-8ab1-4bb0-9c8f-5611c271cb6f
credentials = ('53d1a954-8ab1-4bb0-9c8f-5611c271cb6f', None)
# Scopes: https://o365.github.io/python-o365/latest/usage/account.html?highlight=scopes#setting-scopes
scope = ['basic', 'message_all', 'calendar_all', 'tasks_all', 'onedrive_all']
account = Account(credentials)

# Utilise ceci pour s'authentifier une seule fois
if not account.is_authenticated:
    if account.authenticate(scopes=scope):
        print('Authenticated!')

# # Utilise ceci pour s'authentifier chaque fois (addresses multiples)
# if account.authenticate(scopes=scope):
#     print('Authenticated!')

# Initialize la boite de courriels
mailbox = account.mailbox()
inbox = mailbox.inbox_folder()

running_protocols = []


# find and execute a protocol
def trouver_protocole(_protocol_name, _message):
    print(f"Protocole {_protocol_name}:")

    # crée une liste de protocoles existantes pour comparer le protocole reçu
    dir_path = os.path.dirname(os.path.realpath(__file__))
    protocol_list = []
    for file in os.listdir(f"{dir_path}\Protocoles"):
        if file.endswith(".json"):
            protocol_list.append(os.path.join("\\Protocoles", file))
    print(protocol_list)
    if f"\\Protocoles\\{_protocol_name}.json" in protocol_list:
        print(_protocol_name, "in list")

        queue = Queue()
        pthread = threading.Thread(target=protocol_parser, args=(f'Protocoles/{_protocol_name}.json',queue))
        running_protocols.append(MyThread(pthread, queue, _protocol_name, _message.sender))
        queue.put(_message)
        pthread.start()
        print(f"{_protocol_name} started in {pthread.name}")
        # pthread.join()

        _message.flag.set_completed()
        _message.save_message()
    else:
        print(f"protocole {_protocol_name} non défini.")


# boucle infinie qui attend des protocoles
while True:
    has_new_protocol = False
    for message in inbox.get_messages(limit=25):
        """
        Regex: cherche pour des chaines qui commence sont formatée comme ceci:
        [PO#XXXXX] où X est un chiffre. Peut aussi prendre une lettre si il
        faut spécifier des sou-protocoles. Ex: [PO#00000a]. Les protocoles
        nécissite 5 chiffres et des crochets.
        """
        # regex_email = re.search("\[PO#[0-9]{5}[a-z]?]", message.subject)
        regex_email = re.search("\[PO#([1-9]|[a-z]|[A-Z])*]", message.subject)
        if regex_email is not None and \
                message.flag.status == Flag.NotFlagged:
            has_new_protocol = True
            protocol_name = message.subject[regex_email.span()[0] + 4:regex_email.span()[1] - 1]
            trouver_protocole(protocol_name, message)
    if has_new_protocol is False:
        print("Aucun nouveau protocole trrouvé")
    # attends une minute avant de chercher la boite encore
    sleep(60)
