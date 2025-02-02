from backend.lfeyAPI import APIservice

api = APIservice("http://bore.pub:63156")

api.get_user_by_name("test1")

api.get_user_by_id("52")