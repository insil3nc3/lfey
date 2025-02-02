import requests
import json



class APIservice:
    def __init__(self, url):
        self.url = url


    def get_user_by_id(self, id):
        try:
            response = requests.get(self.url+"/users/"+str(id))
            content = json.loads(response.content)
            print(content)

            if response.status_code == 200:
                print("User registered successfully!", "Success")
            else:
                print("action failed. Please try again.", "Error")
        except requests.exceptions.RequestException as e:
            # Обработка ошибок при отправке запроса
            print(f"An error occurred: {str(e)}", "Error")


    def get_user_by_name(self, name):
        try:
            response = requests.get(self.url+"/users?username="+name)
            content = json.loads(response.content)
            print(content)
            # Проверяем статус код
            if response.status_code == 200:
                print("User registered successfully!", "Success")
            else:
                print("action failed. Please try again.", "Error")
        except requests.exceptions.RequestException as e:
            # Обработка ошибок при отправке запроса
            print(f"An error occurred: {str(e)}", "Error")


    def send_user_data(self, email, password):
        try:
            # Данные для отправки
            payload = {
                "username": email.split("@")[0],
                "email": email,
                "password": password
            }

            print(f"отправлена дата: {payload} на url: {self.url}")
            # Отправляем POST-запрос
            response = requests.post(self.url+"/users/register", json=payload)

            # Проверяем статус код
            if response.status_code == 201:
                print("User registered successfully!", "Success")
            else:
                print("Registration failed. Please try again.", "Error")
        except requests.exceptions.RequestException as e:
            # Обработка ошибок при отправке запроса
            print(f"An error occurred: {str(e)}", "Error")
