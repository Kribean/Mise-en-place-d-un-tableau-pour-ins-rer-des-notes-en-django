import re
import string
from tinydb import TinyDB, where,table
from pathlib import Path

class User:

    DB=TinyDB(Path(__file__).resolve().parent/ 'db.json',indent=4)

    def __init__(self,first_name:str,last_name:str,phone_number:str="",address:str=""):
        self.first_name=first_name
        self.last_name=last_name
        self.phone_number=phone_number
        self.address=address
    
    def __repr__(self):
        return f"{self.first_name},{self.last_name}"

    def __str__(self):
        return f"{self.first_name}\n{self.last_name}\n{self.phone_number}\n{self.address}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    @property
    def db_instance(self) -> table.Document:
        return User.DB.get((where('first_name') == self.first_name) & (where('last_name') == self.last_name))

    def _check_phone_number(self):

        phone_digits=re.sub(r"[+()\s]*","",self.phone_number)
        if len(phone_digits)<10 or not phone_digits.isdigit():
            raise ValueError(f"Num de tel {self.phone_number} invalide")

    def _check(self):
        self._check_phone_number()
        self._check_names()

    def _check_names(self):
        if not(self.first_name and self.last_name):
            raise ValueError("prenom nom invalide")

        special_characters = string.punctuation+string.digits
        

        for character in self.last_name + self.first_name:
            if character in special_characters:
                raise ValueError(f"Nom invalide {self.full_name}")

    def exists(self):
        return bool(self.db_instance)

    def delete(self):
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []

    def save(self, validate_data=False):
        if validate_data:
            self._check()
        print(self.__dict__)
        User.DB.insert(self.__dict__)

def get_all_user():
    return [User(**user) for user in User.DB.all()]

if __name__=="__main__":
    from faker import Faker
    fake=Faker(locale="fr_FR")
    for _ in range(10):
        user=User(fake.first_name(),fake.last_name(),fake.phone_number(),fake.address())
        user._check()
        user.save(True)
        print(user.phone_number)
        print('*'*10)