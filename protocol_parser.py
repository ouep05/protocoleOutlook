import json
import random
from time import sleep
from protocol_classes import *
import threading
from queue import Queue


def execute_state(p, user):
    print()
    print(p.variables)
    print("Commencement de l'état " + p.actors[user].states[p.actors[user].current_state].name)

    acceptable_transitions = []
    i = 0
    # for each transition that exists in the current state
    for transition in p.actors[user].states[p.actors[user].current_state].transitions:
        # if condition is true, add that transition to acceptable transitions list
        # only the transition index is saved
        if transition.condition == "true" or eval(transition.condition):
            acceptable_transitions.append(i)
        i = i + 1

    print("possible states:", acceptable_transitions)

    # if acceptable transitions list exists
    if len(acceptable_transitions) > 0:
        # select a random index from the transition index list
        selected_transition_index = random.choice(acceptable_transitions)

        # retrieve the Transition object that was selected above
        selected_transition = p.actors[user].states[p.actors[user].current_state].transitions[selected_transition_index]
        # execute each action in the transition
        for action in selected_transition.actions:
            print(action)
            eval(action)

        # save the index of the next state
        p.actors[user].current_state = p.actors[user].state_names.index(selected_transition.next_state)
        print("next state: " + selected_transition.next_state)
        sleep(10)


def protocol_parser(filename, queue):
    with open(filename) as json_file:
        p = Protocole(filename, json.load(json_file), queue)
        user = 0

        message = p.queue.get()

        print()
        print(message.sender)
        print(threading.current_thread())
        print("user is", p.actors[user].name)
        print("user initiates the protocol") if p.actors[user].initiates \
            else print("user does not initiate the protocol")
        if p.actors[user].in_transition is not None:
            print("transitions:")
            for transition in p.actors[user].in_transition:
                print("  " + transition)
                eval(transition)

        print()
        print(p.variables)
        print()

        print("states:")
        i = 0

        for state in p.actors[user].states:
            if state.initial:
                p.actors[user].current_state = i
                print(" >" + state.name)
            else:
                print("  " + state.name)
            i = i + 1

        # while current state is not final state
        while p.actors[user].states[p.actors[user].current_state].final is False:
            execute_state(p, user)
            sleep(2)

        print()
        print("Commencement de l'état " + p.actors[user].states[p.actors[user].current_state].name)
        print("état final atteint")
        print("closing {0}".format(threading.current_thread().name))


# protocol_parser('Protocoles/NumPing.json')
