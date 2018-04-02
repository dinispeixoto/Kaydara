import IBMWatsonAPI

if __name__ == '__main__':
    cont = None
    #Necessary to send a empty message to connect to the assistant
    print("Press Enter!")
    while True:
        msg = input("Me: ")
        (intent, entities, context, output) = IBMWatsonAPI.send_message(msg,cont)
        cont = context
        for m in output:
            print(m)
