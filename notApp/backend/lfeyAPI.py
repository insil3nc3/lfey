import logging

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

    def confirm_password(self, email, code):
        try:
            # Формируем URL для подтверждения кода
            url = f"{self.url}/users/confirm/{email}/{code}"
            logging.debug(f"Sending request to: {url}")  # Логируем URL

            # Отправляем POST-запрос
            response = requests.post(url)
            logging.debug(f"Response status code: {response.status_code}")  # Логируем статус код

            # Обрабатываем ответ
            if response.status_code == 200:
                # Если ответ успешный, возвращаем строку (например, JWT-токен)
                jwt_token = response.text  # Получаем текстовый ответ
                logging.debug("Code confirmed successfully! JWT token received.")
                return jwt_token
            elif response.status_code == 400:
                # Обрабатываем ошибку (например, неверный код)
                error_message = response.text  # Получаем текстовое сообщение об ошибке
                logging.error(f"Failed to confirm code: {error_message}")
                print(f"Error: {error_message}")  # Выводим сообщение об ошибке
                return None
            else:
                # Обрабатываем другие ошибки
                logging.error(f"Unexpected status code: {response.status_code}")
                print(f"Unexpected error: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            # Обработка ошибок при отправке запроса
            logging.error(f"An error occurred: {str(e)}")
            print(f"An error occurred: {str(e)}")
            return None

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
                print(response.status_code,"\n",response.text)
        except requests.exceptions.RequestException as e:
            # Обработка ошибок при отправке запроса
            print(f"An error occurred: {str(e)}", "Error")


    def login(self, email, password):
        try:
            # Данные для отправки
            payload = {
                "email": email,
                "password": password
            }

            print(f"отправлена дата: {payload} на url: {self.url}")
            # Отправляем POST-запрос
            response = requests.post(self.url+"/users/login", json=payload)

            # Проверяем статус код
            if response.status_code == 200:
                print("User logined successfully!", "Success")
                return response.text
            else:
                print(response.status_code,"\n",response.text)
                return None
        except requests.exceptions.RequestException as e:
            # Обработка ошибок при отправке запроса
            print(f"An error occurred: {str(e)}", "Error")