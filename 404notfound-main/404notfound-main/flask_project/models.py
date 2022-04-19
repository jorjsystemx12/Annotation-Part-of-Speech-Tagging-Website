from flask_project import db, login_manager
from flask_login import UserMixin
import spacy
from xml.etree import ElementTree as ET




nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])
nlp_de = spacy.load('de_core_news_sm')
nlp_el = spacy.load('el_core_news_sm')


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    nationality = db.Column(db.String(60), nullable=False)
    #Added the two extra for linguistic data collection: Language and Background
    language = db.Column(db.String(60), nullable=False)
    background = db.Column(db.String(60), nullable=False)
    #Add level of eduction + TOS + Privacy statement

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}', '{self.gender}', '{self.nationality}', '{self.language}', '{self.background}')"


class ConvertXml:
    def __init__(self, txt_file):
        self.txt_file = txt_file

    def convert_xml(self):
        result_list = []
        for item in self.txt_file:
            doc = nlp(item)
            for token in doc:
                result_list.append((token.text, token.pos_, token.lemma_))
        data = ET.Element("corpus")
        fille = ET.Element("File")
        data.append(fille)
        counter = 1
        for item in result_list:
            token = ET.SubElement(fille, "token")
            token.text = item[0]
            token.set("POS", item[1])
            token.set("lemma", item[2])
            token.set("id", str(counter))
            counter += 1
        tree = ET.ElementTree(data)
        return tree
    def tokens_xml(self):
        result_list = []
        for item in self.txt_file:
            doc = nlp(item)
            for token in doc:
                result_list.append(token.text)
        data = ET.Element("corpus")
        fille = ET.Element("File")
        data.append(fille)
        counter = 1
        for item in result_list:
            token = ET.SubElement(fille, "token")
            token.text = item
            token.set("id", str(counter))
            counter += 1
        tree = ET.ElementTree(data)
        return tree
    def pos_xml(self):
        result_list = []
        for item in self.txt_file:
            doc = nlp(item)
            for token in doc:
                result_list.append((token.text, token.pos_))
        data = ET.Element("corpus")
        fille = ET.Element("File")
        data.append(fille)
        counter = 1
        for item in result_list:
            token = ET.SubElement(fille, "token")
            token.text = item[0]
            token.set("POS", item[1])
            token.set("id", str(counter))
            counter += 1
        tree = ET.ElementTree(data)
        return tree
    def lemma_xml(self):
        result_list = []
        for item in self.txt_file:
            doc = nlp(item)
            for token in doc:
                result_list.append((token.text, token.lemma_))
        data = ET.Element("corpus")
        fille = ET.Element("File")
        data.append(fille)
        counter = 1
        for item in result_list:
            token = ET.SubElement(fille, "token")
            token.text = item[0]
            token.set("lemma", item[1])
            token.set("id", str(counter))
            counter += 1
        tree = ET.ElementTree(data)
        return tree

class ConvertXmlDe:
    def __init__(self, txt_file):
        self.txt_file = txt_file

    def convert_xml(self):
        result_list = []
        for item in self.txt_file:
            doc = nlp_de(item)
            for token in doc:
                result_list.append((token.text, token.pos_, token.lemma_))
        data = ET.Element("corpus")
        fille = ET.Element("File")
        data.append(fille)
        counter = 1
        for item in result_list:
            token = ET.SubElement(fille, "token")
            token.text = item[0]
            token.set("POS", item[1])
            token.set("lemma", item[2])
            token.set("id", str(counter))
            counter += 1
        tree = ET.ElementTree(data)
        return tree
    def tokens_xml(self):
        result_list = []
        for item in self.txt_file:
            doc = nlp_de(item)
            for token in doc:
                result_list.append(token.text)
        data = ET.Element("corpus")
        fille = ET.Element("File")
        data.append(fille)
        counter = 1
        for item in result_list:
            token = ET.SubElement(fille, "token")
            token.text = item
            token.set("id", str(counter))
            counter += 1
        tree = ET.ElementTree(data)
        return tree
    def pos_xml(self):
        result_list = []
        for item in self.txt_file:
            doc = nlp_de(item)
            for token in doc:
                result_list.append((token.text, token.pos_))
        data = ET.Element("corpus")
        fille = ET.Element("File")
        data.append(fille)
        counter = 1
        for item in result_list:
            token = ET.SubElement(fille, "token")
            token.text = item[0]
            token.set("POS", item[1])
            token.set("id", str(counter))
            counter += 1
        tree = ET.ElementTree(data)
        return tree
    def lemma_xml(self):
        result_list = []
        for item in self.txt_file:
            doc = nlp_de(item)
            for token in doc:
                result_list.append((token.text, token.lemma_))
        data = ET.Element("corpus")
        fille = ET.Element("File")
        data.append(fille)
        counter = 1
        for item in result_list:
            token = ET.SubElement(fille, "token")
            token.text = item[0]
            token.set("lemma", item[1])
            token.set("id", str(counter))
            counter += 1
        tree = ET.ElementTree(data)
        return tree

#Greek class for XML
class ConvertXmlEl:
    def __init__(self, txt_file):
        self.txt_file = txt_file

    def convert_xml(self):
        result_list = []
        for item in self.txt_file:
            doc = nlp_el(item)
            for token in doc:
                result_list.append((token.text, token.pos_, token.lemma_))
        data = ET.Element("corpus")
        fille = ET.Element("File")
        data.append(fille)
        counter = 1
        for item in result_list:
            token = ET.SubElement(fille, "token")
            token.text = item[0]
            token.set("POS", item[1])
            token.set("lemma", item[2])
            token.set("id", str(counter))
            counter += 1
        tree = ET.ElementTree(data)
        return tree
    def tokens_xml(self):
        result_list = []
        for item in self.txt_file:
            doc = nlp_el(item)
            for token in doc:
                result_list.append(token.text)
        data = ET.Element("corpus")
        fille = ET.Element("File")
        data.append(fille)
        counter = 1
        for item in result_list:
            token = ET.SubElement(fille, "token")
            token.text = item
            token.set("id", str(counter))
            counter += 1
        tree = ET.ElementTree(data)
        return tree
    def pos_xml(self):
        result_list = []
        for item in self.txt_file:
            doc = nlp_el(item)
            for token in doc:
                result_list.append((token.text, token.pos_))
        data = ET.Element("corpus")
        fille = ET.Element("File")
        data.append(fille)
        counter = 1
        for item in result_list:
            token = ET.SubElement(fille, "token")
            token.text = item[0]
            token.set("POS", item[1])
            token.set("id", str(counter))
            counter +=1
        tree = ET.ElementTree(data)
        return tree
    def lemma_xml(self):
        result_list = []
        for item in self.txt_file:
            doc = nlp_el(item)
            for token in doc:
                result_list.append((token.text, token.lemma_))
        data = ET.Element("corpus")
        fille = ET.Element("File")
        data.append(fille)
        counter = 1
        for item in result_list:
            token = ET.SubElement(fille, "token")
            token.text = item[0]
            token.set("lemma", item[1])
            token.set("id", str(counter))
            counter += 1
        tree = ET.ElementTree(data)
        return tree


class ConvertJson:
    def __init__(self, txt_file):
        self.txt_file = txt_file

    def convert_to_json(self):
        result_list = []
        counter = 1
        for item in self.txt_file:
            doc = nlp(item)
            for token in doc:
                result_list.append({"Lemma":token.lemma_, "POS": token.pos_, "token_id": counter, "token": token.text})
                counter += 1
        return result_list

    def token_json(self):
        result_list = []
        counter = 1
        for item in self.txt_file:
            doc = nlp(item)
            for token in doc:
                result_list.append({"token_id": counter, "token": token.text})
                counter += 1
        return result_list

    def lemma_json(self):
        result_list = []
        counter = 1
        for item in self.txt_file:
            doc = nlp(item)
            for token in doc:
                result_list.append({"token_id": counter, "token": token.text, "Lemma": token.lemma_})
                counter += 1
        return result_list

    def pos_json(self):
        result_list = []
        counter = 1
        for item in self.txt_file:
            doc = nlp(item)
            for token in doc:
                result_list.append({"token_id": counter, "token": token.text, "POS": token.pos_})
                counter += 1
        return result_list





class ConvertJsonDe:
    def __init__(self, txt_file):
        self.txt_file = txt_file

    def convert_to_json(self):
        result_list = []
        counter = 1
        for item in self.txt_file:
            doc = nlp_de(item)
            for token in doc:
                result_list.append({"Lemma": token.lemma_, "POS": token.pos_, "token_id": counter, "token": token.text})
                counter += 1
        return result_list


    def token_json(self):
        result_list = []
        counter = 1
        for item in self.txt_file:
            doc = nlp_de(item)
            for token in doc:
                result_list.append({"token_id": counter, "token": token.text})
                counter += 1
        return result_list

    def lemma_json(self):
        result_list = []
        counter = 1
        for item in self.txt_file:
            doc = nlp_de(item)
            for token in doc:
                result_list.append({"token_id": counter, "token": token.text, "Lemma": token.lemma_})
                counter += 1
        return result_list

    def pos_json(self):
        result_list = []
        counter = 1
        for item in self.txt_file:
            doc = nlp_de(item)
            for token in doc:
                result_list.append({"token_id": counter, "token": token.text, "POS": token.pos_})
                counter += 1
        return result_list

# Greek Class for JSON
class ConvertJsonEl:
    def __init__(self, txt_file):
        self.txt_file = txt_file

    def convert_to_json(self):
        result_list = []
        counter = 1
        for item in self.txt_file:
            doc = nlp_el(item)
            for token in doc:
                result_list.append({"Lemma": token.lemma_, "POS": token.pos_, "token_id": counter, "token": token.text})
                counter += 1
        return result_list

    def token_json(self):
        result_list = []
        counter = 1
        for item in self.txt_file:
            doc = nlp_el(item)
            for token in doc:
                result_list.append({"token_id": counter, "token": token.text})
                counter += 1
        return result_list

    def lemma_json(self):
        result_list = []
        counter = 1
        for item in self.txt_file:
            doc = nlp_el(item)
            for token in doc:
                result_list.append({"token_id": counter, "token": token.text, "Lemma": token.lemma_})
                counter += 1
        return result_list

    def pos_json(self):
        result_list = []
        counter = 1
        for item in self.txt_file:
            doc = nlp_el(item)
            for token in doc:
                result_list.append({"token_id": counter, "token": token.text, "POS": token.pos_})
                counter += 1
        return result_list
