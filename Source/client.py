from socket import *

def main():
    serverport = 8888
    
    while True:
        # Create a socket and connect to the server
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect(('', serverport))

        # Receive city data
        receivedMessage = clientSocket.recv(1024).decode()
        prediction = input(receivedMessage + ' ')
        
        # Send temperature guess
        clientSocket.send(prediction.encode())
        counter = 0
        while counter < 2:
            if prediction == 'END':
                print('Game is ended, connection is closed')
                clientSocket.close()
                return
            feedBack = clientSocket.recv(1024).decode()
            if feedBack == 'Success!':
                print(feedBack)
                break

            print(feedBack)
            prediction = input('Enter guess:')
            clientSocket.send(prediction.encode())
            counter = counter + 1

        if counter == 2:
            lastMessage = clientSocket.recv(1024).decode()
            print(lastMessage)
        clientSocket.close()
        
    
    

if __name__ == '__main__':
    main()