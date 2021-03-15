# This project automizes protocols for Outlook.
from time import sleep
from O365 import *
import re
from O365.message import Flag
from protocoles_outlook import *

# Une application de Microsoft Azure est utilisée pour
# définir les portées du programme.
# client ID: 53d1a954-8ab1-4bb0-9c8f-5611c271cb6f
credentials = ('53d1a954-8ab1-4bb0-9c8f-5611c271cb6f', None)
# Scopes: https://o365.github.io/python-o365/latest/usage/account.html?highlight=scopes#setting-scopes
scope = ['basic', 'message_all', 'calendar_all', 'tasks_all', 'onedrive_all']
account = Account(credentials)

# # Utilise ceci pour s'authentifier une seule fois
# if not account.is_authenticated:
#     if account.authenticate(scopes=scope):
#         print('Authenticated!')

# Utilise ceci pour s'authentifier chaque fois (courriels multiples)
if account.authenticate(scopes=scope):
    print('Authenticated!')

# Initialize la boite de courriels
mailbox = account.mailbox()
inbox = mailbox.inbox_folder()

# boucle infinie qui attend des protocoles
while True:
    new_protocol = False
    for message in inbox.get_messages(limit=25):
        """
        Regex: cherche pour des chaines qui commence sont formatée comme ceci:
        [PO#XXXXX] où X est un chiffre. Peut aussi prendre une lettre si il
        faut spécifier des sou-protocoles. Ex: [PO#00000a]. Les protocoles
        nécissite 5 chiffres et des crochets.
        """
        regex_email = re.search("\[PO#[0-9]{5}[a-z]?]", message.subject)
        if regex_email is not None and \
                message.flag.status == Flag.NotFlagged:
            new_protocol = True
            num_protocole = message.subject[regex_email.span()[0] + 4:regex_email.span()[0] + 9]
            try:
                print("protocole " + num_protocole + ":")
                eval("protocole" + num_protocole + "(message)")
                message.flag.set_completed()
                message.save_message()
            except NameError:
                print("protocole " + num_protocole + "non défini.")
    if not new_protocol:
        print("Aucun nouveau protocole trrouvé")
    # attends une minute avant de chercher la boite encore
    sleep(60)
