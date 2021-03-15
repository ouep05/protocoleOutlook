# 00001
# print le sujet et le corps du courriel
def protocole00001(message):
    print(message.subject)
    print(message.body_preview)


# 00002
# Si le corps est un int, retourne int + 1
def protocole00002(message):
    try:
        x = int(message.body_preview.partition('\n')[0].strip())
        x = x + 1

        m = message.reply()
        m.body = str(x)
        m.send()
        message.flag.set_completed()
        message.save_message()
        print("valeure " + str(x) + " retournée")
    except ValueError:
        print("Le corps du courriel n'est pas un int")

# 00003
# protocole à plusieurs étapes
