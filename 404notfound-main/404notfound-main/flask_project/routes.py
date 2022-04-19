import os
from os.path import join, dirname, realpath
from flask import Flask, request, render_template, url_for, flash, redirect, send_file, send_from_directory, jsonify, json
from flask_project.forms import Registration, LogIn
from flask_project import app, db, bcrypt
from flask_project.models import User, ConvertXml, ConvertJson, ConvertXmlDe, ConvertJsonDe, ConvertXmlEl, ConvertJsonEl
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import secure_filename
import re
import random


basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = './static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DOWNLOAD_FOLDER = './static/download'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home Page - MUCA")


@app.route("/about")
def about():
    return render_template("about.html", title="about - MUCA")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LogIn()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home"))
        else:
            flash("Incorrect email or password")
    return render_template("login.html", title="login - MUCA", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = Registration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                    password=hashed_password, gender=form.gender.data, nationality=form.nationality.data, 
                    language=form.language.data, background=form.background.data)
        db.session.add(user)
        db.session.commit()
        flash(f"{form.first_name.data}! your account was created successfully. you can now log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="register - MUCA", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


# This function is taken from the following site: https://www.programmersought.com/article/10663049555/
# author is unknown
def pretty_xml(element, indent, newline, level=0):  # Elemnt is passed in Elment class parameters for indentation indent, for wrapping NEWLINE
    if element:  # Determine whether the element has child elements
        if (element.text is None) or element.text.isspace():  # If there is no element of text content
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # Else: # here two lines if the Notes removed, Element will start a new line of text
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # Element will turn into a list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # If it is not the last element of the list, indicating that the next line is the starting level of the same elements, indentation should be consistent
            subelement.tail = newline + indent * (level + 1)
        else:  # If it is the last element of the list, indicating that the next line is the end of the parent element, a small indentation should
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)



@app.route("/xmlconvert", methods=["GET", "POST"])
def xmlconvert():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        select_language = request.form.get('language')
        select_annotation = request.form.get('annotation')
        if file and select_language == "English" and select_annotation == "all":
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)),'r', encoding = 'utf-8')
            try_1 = ConvertXml(documentation)
            xml_tree = try_1.convert_xml()
            root = xml_tree.getroot()
            pretty_xml(root, '\t', '\n')
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".xml"
            tokenoutfile = open(path_download + result_file, "wb")
            xml_tree.write(tokenoutfile, encoding='utf-8', xml_declaration=True)
        if file and select_language == "English" and select_annotation == "Tok":
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)),'r', encoding = 'utf-8')
            try_1 = ConvertXml(documentation)
            xml_tree = try_1.tokens_xml()
            root = xml_tree.getroot()
            pretty_xml(root, '\t', '\n')
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".xml"
            tokenoutfile = open(path_download + result_file, "wb")
            xml_tree.write(tokenoutfile, encoding='utf-8', xml_declaration=True)
        if file and select_language == "English" and select_annotation == "Tokpos":
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)),'r', encoding = 'utf-8')
            try_1 = ConvertXml(documentation)
            xml_tree = try_1.pos_xml()
            root = xml_tree.getroot()
            pretty_xml(root, '\t', '\n')
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".xml"
            tokenoutfile = open(path_download + result_file, "wb")
            xml_tree.write(tokenoutfile, encoding='utf-8', xml_declaration=True)
        if file and select_language == "English" and select_annotation == "Toklemma":
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)),'r', encoding = 'utf-8')
            try_1 = ConvertXml(documentation)
            xml_tree = try_1.lemma_xml()
            root = xml_tree.getroot()
            pretty_xml(root, '\t', '\n')
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".xml"
            tokenoutfile = open(path_download + result_file, "wb")
            xml_tree.write(tokenoutfile, encoding='utf-8', xml_declaration=True)
        if file and select_language == "German" and select_annotation == "all":
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)),'r', encoding = 'utf-8')
            try_1 = ConvertXmlDe(documentation)
            xml_tree = try_1.convert_xml()
            root = xml_tree.getroot()
            pretty_xml(root, '\t', '\n')
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".xml"
            tokenoutfile = open(path_download + result_file, "wb")
            xml_tree.write(tokenoutfile, encoding='utf-8', xml_declaration=True)
        if file and select_language == "German" and select_annotation == "Tok":
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)),'r', encoding = 'utf-8')
            try_1 = ConvertXmlDe(documentation)
            xml_tree = try_1.tokens_xml()
            root = xml_tree.getroot()
            pretty_xml(root, '\t', '\n')
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".xml"
            tokenoutfile = open(path_download + result_file, "wb")
            xml_tree.write(tokenoutfile, encoding='utf-8', xml_declaration=True)
        if file and select_language == "German" and select_annotation == "Tokpos":
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)),'r', encoding = 'utf-8')
            try_1 = ConvertXmlDe(documentation)
            xml_tree = try_1.pos_xml()
            root = xml_tree.getroot()
            pretty_xml(root, '\t', '\n')
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".xml"
            tokenoutfile = open(path_download + result_file, "wb")
            xml_tree.write(tokenoutfile, encoding='utf-8', xml_declaration=True)
        if file and select_language == "German" and select_annotation == "Toklemma":
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)),'r', encoding = 'utf-8')
            try_1 = ConvertXmlDe(documentation)
            xml_tree = try_1.lemma_xml()
            root = xml_tree.getroot()
            pretty_xml(root, '\t', '\n')
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".xml"
            tokenoutfile = open(path_download + result_file, "wb")
            xml_tree.write(tokenoutfile, encoding='utf-8', xml_declaration=True)
        #Greek Set
        if file and select_language == "Greek" and select_annotation == "all":
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)),'r', encoding = 'utf-8')
            try_1 = ConvertXmlEl(documentation)
            xml_tree = try_1.convert_xml()
            root = xml_tree.getroot()
            pretty_xml(root, '\t', '\n')
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".xml"
            tokenoutfile = open(path_download + result_file, "wb")
            xml_tree.write(tokenoutfile, encoding='utf-8', xml_declaration=True)
        if file and select_language == "Greek" and select_annotation == "Tok":
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)),'r', encoding = 'utf-8')
            try_1 = ConvertXmlEl(documentation)
            xml_tree = try_1.tokens_xml()
            root = xml_tree.getroot()
            pretty_xml(root, '\t', '\n')
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".xml"
            tokenoutfile = open(path_download + result_file, "wb")
            xml_tree.write(tokenoutfile, encoding='utf-8', xml_declaration=True)
        if file and select_language == "Greek" and select_annotation == "Tokpos":
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)),'r', encoding = 'utf-8')
            try_1 = ConvertXmlEl(documentation)
            xml_tree = try_1.pos_xml()
            root = xml_tree.getroot()
            pretty_xml(root, '\t', '\n')
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".xml"
            tokenoutfile = open(path_download + result_file, "wb")
            xml_tree.write(tokenoutfile, encoding='utf-8', xml_declaration=True)
        if file and select_language == "Greek" and select_annotation == "Toklemma":
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)),'r', encoding = 'utf-8')
            try_1 = ConvertXmlEl(documentation)
            xml_tree = try_1.lemma_xml()
            root = xml_tree.getroot()
            pretty_xml(root, '\t', '\n')
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".xml"
            tokenoutfile = open(path_download + result_file, "wb")
            xml_tree.write(tokenoutfile, encoding='utf-8', xml_declaration=True)

        with open(tokenoutfile.name, "rb") as f:
            file_url = url_for('download_file', name=result_file)
            return render_template('xmlconvert.html', output=f.read().decode('utf8'), fileurl=file_url)
    return render_template("xmlconvert.html", title="XML Converter - MUCA")


@app.route("/jsonconvert", methods=["GET", "POST"])
def jsonconvert():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        select = request.form.get('language')
        select_annotation = request.form.get('annotation')
        files = request.files.getlist("file")
        results_list = []
        if len(files) > 0 and select == "English" and select_annotation == "all":
            for f in files:
                filename = secure_filename(f.filename)
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)), 'r',
                                     encoding='utf-8')
                try_2 = ConvertJson(documentation)
                json_pack = try_2.convert_to_json()
                results_list.append(json_pack)
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".json"
            outputfile = open(path_download + result_file, "wb")
            json.dump(results_list, outputfile)
        if len(files) > 0 and select == "English" and select_annotation == "Tok":
            for f in files:
                filename = secure_filename(f.filename)
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)), 'r',
                                     encoding='utf-8')
                try_2 = ConvertJson(documentation)
                json_pack = try_2.token_json()
                results_list.append(json_pack)
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".json"
            outputfile = open(path_download + result_file, "wb")
            json.dump(results_list, outputfile)
        if len(files) > 0 and select == "English" and select_annotation == "Tokpos":
            for f in files:
                filename = secure_filename(f.filename)
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)), 'r',
                                     encoding='utf-8')
                try_2 = ConvertJson(documentation)
                json_pack = try_2.pos_json()
                results_list.append(json_pack)
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".json"
            outputfile = open(path_download + result_file, "wb")
            json.dump(results_list, outputfile)
        if len(files) > 0 and select == "English" and select_annotation == "Toklemma":
            for f in files:
                filename = secure_filename(f.filename)
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)), 'r',
                                     encoding='utf-8')
                try_2 = ConvertJson(documentation)
                json_pack = try_2.lemma_json()
                results_list.append(json_pack)
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".json"
            outputfile = open(path_download + result_file, "wb")
            json.dump(results_list, outputfile)
        if len(files) > 0 and select == "German" and select_annotation == "all":
            for f in files:
                filename = secure_filename(f.filename)
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)), 'r',
                                     encoding='utf-8')
                try_2 = ConvertJsonDe(documentation)
                json_pack = try_2.convert_to_json()
                results_list.append(json_pack)
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".json"
            outputfile = open(path_download + result_file, "wb")
            json.dump(results_list, outputfile)
        if len(files) > 0 and select == "German" and select_annotation == "Tok":
            for f in files:
                filename = secure_filename(f.filename)
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)), 'r',
                                     encoding='utf-8')
                try_2 = ConvertJsonDe(documentation)
                json_pack = try_2.token_json()
                results_list.append(json_pack)
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".json"
            outputfile = open(path_download + result_file, "wb")
            json.dump(results_list, outputfile)
        if len(files) > 0 and select == "German" and select_annotation == "Tokpos":
            for f in files:
                filename = secure_filename(f.filename)
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)), 'r',
                                     encoding='utf-8')
                try_2 = ConvertJsonDe(documentation)
                json_pack = try_2.pos_json()
                results_list.append(json_pack)
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".json"
            outputfile = open(path_download + result_file, "wb")
            json.dump(results_list, outputfile)
        if len(files) > 0 and select == "German" and select_annotation == "Toklemma":
            for f in files:
                filename = secure_filename(f.filename)
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)), 'r',
                                     encoding='utf-8')
                try_2 = ConvertJsonDe(documentation)
                json_pack = try_2.lemma_json()
                results_list.append(json_pack)
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".json"
            outputfile = open(path_download + result_file, "wb")
            json.dump(results_list, outputfile)

        #Greek set for JSON
        if len(files) > 0 and select == "Greek" and select_annotation == "all":
            for f in files:
                filename = secure_filename(f.filename)
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)), 'r',
                                     encoding='utf-8')
                try_2 = ConvertJsonEl(documentation)
                json_pack = try_2.convert_to_json()
                results_list.append(json_pack)
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".json"
            outputfile = open(path_download + result_file, "wb")
            json.dump(results_list, outputfile, ensure_ascii=False)
        if len(files) > 0 and select == "Greek" and select_annotation == "Tok":
            for f in files:
                filename = secure_filename(f.filename)
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)), 'r',
                                     encoding='utf-8')
                try_2 = ConvertJsonEl(documentation)
                json_pack = try_2.token_json()
                results_list.append(json_pack)
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".json"
            outputfile = open(path_download + result_file, "wb")
            json.dump(results_list, outputfile, ensure_ascii=False)
        if len(files) > 0 and select == "Greek" and select_annotation == "Tokpos":
            for f in files:
                filename = secure_filename(f.filename)
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)), 'r',
                                     encoding='utf-8')
                try_2 = ConvertJsonEl(documentation)
                json_pack = try_2.pos_json()
                results_list.append(json_pack)
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".json"
            outputfile = open(path_download + result_file, "wb")
            json.dump(results_list, outputfile, ensure_ascii=False)
        if len(files) > 0 and select == "Greek" and select_annotation == "Toklemma":
            for f in files:
                filename = secure_filename(f.filename)
                f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                documentation = open((os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)), 'r',
                                     encoding='utf-8')
                try_2 = ConvertJsonEl(documentation)
                json_pack = try_2.lemma_json()
                results_list.append(json_pack)
            path_download = "flask_project/static/download/"
            result_file = "result_" + str(random.randint(1000, 9999)) + ".json"
            outputfile = open(path_download + result_file, "wb")
            json.dump(results_list, outputfile, ensure_ascii=False)

        with open(outputfile.name, "rb") as f:
            file_url = url_for('download_file', name=result_file)
            return render_template('jsonconvert.html', output=f.read().decode('utf-8'), fileurl=file_url)
    return render_template("jsonconvert.html", title="JSON Converter - MUCA")

@app.route('/upload/<name>')
def download_file(name):
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], name), as_attachment=True)



    