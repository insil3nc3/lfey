from shop_bd import ModulesManager


db_manager = ModulesManager()

def get_all_modules():
    return db_manager.get_all_modules()

