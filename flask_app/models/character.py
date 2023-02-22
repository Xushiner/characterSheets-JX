from unittest import result
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re

DB = "character-sheet-schema"


class Character:
    def __init__(self, character):
        self.id = character['id']
        self.name = character['name']
        self.ancestry = character['ancestry']
        self.novice_path = character['novice_path']
        self.expert_path = character['expert_path']
        self.master_path = character['master_path']
        self.level = character['level']
        self.insanity = character['insanity']
        self.corruption = character['corruption']
        self.power = character['power']
        self.strength = character['strength']
        self.agility = character['agility']
        self.intellect = character['intellect']
        self.will = character['will']
        self.perception = character['perception']
        self.speed = character['speed']
        self.size = character['size']
        self.health = character['health']
        self.armor = character['armor']
        self.defense = character['defense']
        self.damage = character['damage']
        self.healing_rate = character['healing_rate']
        self.created_at = character['created_at']
        self.updated_at = character['updated_at']
        self.creator = None

    @classmethod
    def create_character(cls, data):
        query = """INSERT INTO 
                    characters (name, ancestry, novice_path, expert_path, master_path, level,insanity,corruption,power,strength,agility, intellect,will, perception, speed, size, health,armor,defense, damage,healing_rate,users_id) 
                    VALUES (%(name)s, %(ancestry)s, %(novice_path)s,%(expert_path)s, %(master_path)s, %(level)s, %(insanity)s, %(corruption)s, %(power)s, %(strength)s, %(agility)s, %(intellect)s, %(will)s, %(perception)s, %(speed)s, %(size)s, %(health)s, %(armor)s, %(defense)s, %(damage)s, %(healing_rate)s, %(users_id)s);
                """
        character = connectToMySQL(DB).query_db(query, data)
        return character

    @classmethod
    def update_character(cls, data):

        query = """UPDATE characters 
                SET name = %(name)s, 
                    ancestry = %(ancestry)s, 
                    novice_path = %(novice_path)s, 
                    expert_path =  %(expert_path)s, 
                    master_path =  %(master_path)s, 
                    level =  %(level)s, 
                    insanity =  %(insanity)s, 
                    corruption =  %(corruption)s, 
                    power =  %(power)s, 
                    strength =  %(strength)s, 
                    agility =  %(agility)s, 
                    intellect =  %(intellect)s, 
                    will=  %(will)s, 
                    perception =  %(perception)s, 
                    speed =  %(speed)s, 
                    size = %(size)s, 
                    health =  %(health)s, 
                    armor = %(armor)s, 
                    defense = %(defense)s, 
                    damage=  %(damage)s, 
                    healing_rate =  %(healing_rate)s 
                WHERE id = %(id)s;
                """
        return connectToMySQL(DB).query_db(query,data)
        

    @classmethod
    def delete_character_by_id(cls, character_id):
        data = {'id': character_id}
        query = "DELETE from characters WHERE id = %(id)s;"
        connectToMySQL(DB).query_db(query, data)
        return character_id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM characters LEFT JOIN users ON characters.users_id = users.id;"
        results = connectToMySQL(DB).query_db(query)
        characters = []
        for character in results:
            one_character = cls(character)
            user_data = {
                "id": character["users.id"],
                "first_name": character["first_name"],
                "last_name": character["last_name"],
                "email": character["email"],
                "password": None,
                "created_at": character["users.created_at"],
                "updated_at": character["users.updated_at"]
            }
            one_character.creator = user.User(user_data)
            characters.append(one_character)
        return characters

    @classmethod
    def get_by_id(cls, character_id):
        data = {'id': character_id}
        query = "SELECT * FROM characters LEFT JOIN users ON users.id = characters.users_id WHERE characters.id = %(id)s; "
        result = connectToMySQL(DB).query_db(query, data)
        result = result[0]
        character = cls(result)
        character.user = user.User(
            {
                "id": result["users.id"],
                "first_name": result["first_name"],
                "last_name": result["last_name"],
                "email": result["email"],
                "password": None,
                "created_at": result["users.created_at"],
                "updated_at": result["users.updated_at"]
            }
        )
        # character.append(cls(character))
        return character
