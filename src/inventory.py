import pickle

class Inventory:
    group_inv = []
    group_file = 'inv.bot'

    def __init__(self):
        self.user = None
        self.inv = []
        self.user_file = 'usr_inv.bot'

    def load_data(self, group=True):
        if group:
            temp = pickle.load()
            for x in temp:
                group_inv.append(x)
        else:
            temp = pickle.load()
            for x in temp:
                self.inv.append(x)

    def save_data(self, group=True):
        if group:
            pickle.dump(group_inv, group_file)
        else:
            pickle.dump(self.inv, self.file) # BUG: fix this so it actually works ecks dee

    def add_item(self, item, group=True):
        if group:
            group_inv.append(item)
        else:
            self.inv.append(item)

    def remove_item(self, item, group=True): # might need to do this better, potentional BUG
        if group:
            group_inv.remove(item)
        else:
            self.inv.remove(item)

    def display_data(self, group=True):
        return group_inv if group else self.inv
