import pandas as pd
from socket import *

def handle_request(client_connection, realTemp):
    # Receive guessed temperature and convert it to float
    receivedTemp = client_connection.recv(1024).decode()
    print('Received ' + receivedTemp)

    # Calculate tolerance values
    tolerance = realTemp / 10
    upperLimit = realTemp + tolerance
    lowerLimit = realTemp - tolerance

    # Receive temperature and send feedback to client
    counter = 0
    while counter < 2:
        if receivedTemp == 'END':
            print('Game is ended, connection is closed')
            client_connection.close()
            exit()
            return
        else:
            receivedTemp = float(receivedTemp)
        
        if receivedTemp <= upperLimit and receivedTemp >= lowerLimit:
            client_connection.send('Success!'.encode())
            print('Success')
            return
        elif receivedTemp < lowerLimit:
            client_connection.send('Higher...'.encode())
            print('Higher')
        elif receivedTemp > upperLimit:
            client_connection.send('Lower...'.encode())
            print('Lower')

        receivedTemp = client_connection.recv(1024).decode()
        print('Received ' + receivedTemp)
        counter = counter + 1

    # Check the last prediction
    if float(receivedTemp) < upperLimit and float(receivedTemp) > lowerLimit:  
        client_connection.send('Success!'.encode())
        print('Success')
        return
    
    client_connection.send(('Correct answer is: ' + str(realTemp)).encode())
    print('Finished')
    return


def serve_forever():
    serverPort = 8888
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)

    # Read data
    weatherData = pd.read_excel("weathers.xlsx")
    print('The server is ready')
    while True:
        
        # Choose a random row
        randomRow = weatherData.sample()
        city = randomRow.iloc[0, 0]
        temp = randomRow.iloc[0, 1]
        
        # Accept the requests and send randomRow data
        print('Waiting for connection...')
        connectionSocket, addr = serverSocket.accept()
        print('Connected.')
        message =  ('Predict the temperature of '  + city).encode()
        connectionSocket.send(message)

        # Handle the guess
        handle_request(connectionSocket, temp)
        

    connectionSocket.close()


if __name__ == '__main__':
    serve_forever()