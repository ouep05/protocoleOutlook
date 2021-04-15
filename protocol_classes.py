# Un Protocole est un dictionnaire d'acteurs (acteur = role)
# un acteur a un dictionnaire avec plusieurs états
#   les états crée une machine à état pour chaque acteur
# un état individuel


class MyThread(object):
    def __init__(self, thread, queue, protocol_name, sender):
        self.thread = thread
        self.queue = queue
        self.protocol_name = protocol_name
        self.sender = sender
        # self.id ?


class Transition(object):
    def __init__(self, data):
        self.data = data
        self.condition = list(self.data.values())[0]
        self.actions = list(self.data.values())[1]
        self.next_state = list(self.data.values())[2]


class State(object):
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.initial = list(self.data.values())[0]
        self.final = list(self.data.values())[1]
        self.transitions_data = list(self.data.values())[2]
        self.transitions = list()
        if self.transitions_data is not None:
            for i in range(0, len(self.transitions_data)):
                self.transitions.append(Transition(self.transitions_data[i]))


class Actor(object):
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.initiates = list(self.data.values())[0]
        self.in_transition = list(self.data.values())[1]
        self.states_data = list(self.data.values())[2]
        self.state_names = []
        # current_state used as an index in the program
        self.current_state = -1
        self.states = list()
        for key in self.states_data.keys():
            self.state_names.append(key)
            self.states.append(State(key, self.states_data[key]))


# ** named Protocole since Protocol (no e) is in O365.connections
class Protocole(object):
    def __init__(self, name: str, data, queue):
        self.data = data
        self.name = name
        self.queue = queue
        self.variables = {}
        # list of all the actor names
        self.actors_names = list(data.keys())
        # populate a list of actors with the dictionary within each actor
        self.actors = list()
        for key in self.actors_names:
            self.actors.append(Actor(key, data[key]))

    # checks if any given variable is in the dictionary
    # if yes, return that value, if no, send the variable back
    def key(self, var):
        if var in self.variables.keys():
            return self.variables[var]
        else:
            return var

    def input_number(self, var, value=None):
        if value is None:
            value = int(input('Entrer un nombre: '))
        self.variables[var] = value

    def input_var(self, var, value=None):
        if value is None:
            input('Entrer une valeure: ')
        self.variables[var] = value

    def send(self, recipient, value):
        sending = ""
        if type(value) is tuple:
            for t in value:
                sending = f"{sending} {t},"
            sending = sending[0:len(sending) - 1]
        else:
            sending = f"{sending} {value}"
        print(f"Sending{sending} to {recipient}")

    # change return to whether or not we got an email
    def receive(self, recipient_var, recipient, var_dict):
        # add recipient to vars if it does not exist (is the if needed?)
        if recipient_var not in self.variables.keys():
            self.variables[recipient_var] = recipient
        for var in var_dict:
            self.variables[var] = var_dict[var]
        return True

    def equal(self, var, comparer):
        return True if var == comparer else False
