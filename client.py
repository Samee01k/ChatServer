import socket
import threading
import datetime
import requests
import psycopg2


user = input("Enter your name: ")

host = socket.gethostname()
ip_address = socket.gethostbyname(host)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, 65005))

#Time
t = datetime.datetime.now().time()

#Location
r = requests.get('https://get.geojs.io/')
ip_r = requests.get('https://get.geojs.io/v1/ip.json')
#ipaddress
ip_add = ip_r.json()['ip']
url = 'https://get.geojs.io/v1/ip/geo/'+ip_add+'.json'
geo_request = requests.get(url)
geo_data = geo_request.json()
city = geo_data['city']
country = geo_data['country']

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'user':
                client.send(user.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break
            
def display():
    while True:
        dbconn = psycopg2.connect("dbname=Chat")
        cursor = dbconn.cursor()
        message = f'IP address: {ip_add} Local Time : {t}  Location: {city}, {country} 	\n {user}: {input("")}'
        cursor.execute("INSERT INTO Chathistory (data) VALUES (%s)",(message,))
        client.send(message.encode('ascii'))
        dbconn.commit()
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

display_thread = threading.Thread(target=display)
display_thread.start()
            
            
