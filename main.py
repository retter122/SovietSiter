from flask import *
import json

app = Flask(__name__)

Users = dict()

with open('static/Users.json') as Usrs:
    Users = json.load(Usrs)

User = dict()
nextId = 0
if Users:
    nextId = int(max(list(Users.keys())))
Magazins = dict()
memSize = 12

SovietRespulics = [
    "Росcийская СФСР",
    "Белорусская ССР",
    "Украинская ССР",
    "Узбекская ССР",
    "Казахская ССР"
    "Туркменская ССР"
    "Кыгызская ССР"
    "Таджикская CCР"
    "Армянская ССР",
    "Грузинская ССР",
    "Азейрбайджанская ССР",
    "Молдавская ССР",
    "Эстонская ССР",
    "Латвийская ССР",
    "Литовская CCР",
    "Германская ДР",
    "Корейская НДР",
    "Китайская НР",
    "Польская ДР",
    "Венгерская ДР",
    "Румынская ДР",
    "Чехо-словатская ДР",
    "Болгарская ДР",
    "СФР Югославия",
    "Албанская ДР",
]

@app.route('/')
@app.route('/Capital')
def MainMenu():
    m = [f"static/Design/Magazine/{str(i + 1)}.jpg" for i in range(6)]
    return render_template("main.html", User=User, magaz=m, news=[])

@app.route("/Work")
def Work():
    m = [f"static/Design/Work/{str(i)}.jpg" for i in range(11)]
    return render_template("work.html", User=User, Sld=m)

@app.route('/Voice')
def VoiceProlate():
    Blgs = []
    for i in Users.keys():
        for j in Users[i].get("Blogs"):
            Blog = j
            Blog["UserName"] = Users[i]["Name"]
            Blgs.append(Blog)

    return render_template("voice.html", User=User, Blogs=Blgs)

@app.route('/Memory')
def Memory():
    m = [f"static/Design/Memory/{str(i + 1)}.jpg" for i in range(memSize)]
    return render_template("mem.html", mems=m, User=User)

@app.route('/Pioner')
def Pioner():
    return render_template("pioner.html", User=User)

@app.route('/Regist', methods=['GET', 'POST'])
def Regist():
    global nextId, User, Users
    Err = ""
    f = True
    if request.method == 'POST':
        if request.form['submit_button'] == 'Назад':
            return MainMenu()

        elif request.form['submit_button'] == 'Регистрация':
            for i in Users.keys():
                if (request.form['userSurname'] == Users[i]["Surname"] and request.form['userName'] == Users[i]["Name"] and request.form['userFather'] == Users[i]["Fathername"] and
                request.form['userPassword'] == Users[i]["Password"]):
                    Err = "Товарищ, вы уже зарегистрированны!"
                    f = False
                    break
            if not (request.form['userSurname']) and f:
                Err = "Товарищ, вы не указали свою фамилию"
            elif not (request.form['userName']) and f:
                Err = "Товарищ, вы не указали свою имя"
            elif not (request.form['userCountry']) and f:
                Err = "Товарищ, вы не указали свою страну"
            elif not (request.form['userCity']) and f:
                Err = "Товарищ, вы не указали свой город"
            elif not (request.form['userAdress']) and f:
                Err = "Товарищ, вы не указали свой адрес"
            elif not (request.form['userPassword']) and f:
                Err = "Товарищ, вы не указали свой пароль, помините капитализм никогда не дремлет!"
            elif f:
                User["Name"] = request.form['userName']
                User["Surname"] = request.form['userSurname']
                User["Fathername"] = request.form['userFather']
                User["Country"] = request.form['userCountry']
                User["City"] = request.form['userCity']
                User["Adress"] = request.form['userAdress']
                User["Password"] = request.form['userPassword']
                User["Avatar"] = 'static/Design/UserAvatars/0.jpg'
                User["Id"] = nextId
                Users[nextId] = User
                nextId += 1
                with open('static/Users.json', 'w') as Usrs:
                    json.dump(Users, Usrs)
                    return MainMenu()

        elif request.form['submit_button'] == 'Вход':
            f = 0
            idu = 0
            for i in Users.keys():
                if (request.form['userSurname'] == Users[i]["Surname"] and request.form['userName'] == Users[i]["Name"] and request.form['userFather'] == Users[i]["Fathername"] and
                request.form['userPassword'] == Users[i]["Password"]):
                    f = 2
                    idu = i
                    break

                elif (request.form['userSurname'] == Users[i]["Surname"] and request.form['userName'] == Users[i]["Name"] and request.form['userFather'] == Users[i]["Fathername"] and
                request.form['userPassword'] != Users[i]["Password"]):
                    f = 1
                    break

            if f == 2:
                User["Name"] = request.form['userName']
                User["Surname"] = request.form['userSurname']
                User["Fathername"] = request.form['userFather']
                User["Country"] = request.form['userCountry']
                User["City"] = request.form['userCity']
                User["Adress"] = request.form['userAdress']
                User["Password"] = request.form['userPassword']
                User["Avatar"] = Users[idu]["Avatar"]
                User["Blogs"] = Users[idu]["Blogs"]
                User["Id"] = idu
                return MainMenu()

            elif f == 1:
                Err = "Товарищ, вы ввели не правильный пароль!"

            else:
                Err = "Товарищ, вы еще не зарегистрированы!"


    return render_template("registration.html", Error=Err, resp=SovietRespulics)


@app.route('/User', methods=['GET', 'POST'])
def UserPage():
    Err = ""
    CrBl = False
    if request.method == 'POST':
        if request.form['submit_button'] == 'Назад':
            return MainMenu()

        if request.form['submit_button'] == 'Применить':
            f = True
            for i in Users.keys():
                if (request.form['userSurname'] == Users[i]["Surname"] and request.form['userName'] == Users[i]["Name"] and request.form['userFather'] == Users[i]["Fathername"]):
                    f = False
                    break

            if f or (User["Name"] == request.form['userName'] and User["Surname"] == request.form['userSurname'] and User["Fathername"] == request.form['userFather']):
                User["Name"] = request.form['userName']
                User["Surname"] = request.form['userSurname']
                User["Fathername"] = request.form['userFather']
                User["Country"] = request.form['userCountry']
                User["City"] = request.form['userCity']
                User["Adress"] = request.form['userAdress']
                if request.files['userAvatar']:
                    request.files['userAvatar'].save(f'static/Design/UserAvatars/{int(User["Id"]) + 1}.jpg')
                    User["Avatar"] = f'static/Design/UserAvatars/{int(User["Id"]) + 1}.jpg'
                Users[User["Id"]] = User
                with open('static/Users.json', 'w') as Usrs:
                    json.dump(Users, Usrs)
                    return MainMenu()

            else:
                Err = "Товарищ, такие данные пользователя уже заняты!"

        if request.form['submit_button'] == 'Создать запись':
            CrBl = True

        if request.form['submit_button'] == 'Сохранить запись':
            CrBl = False
            if "Blogs" in User.keys():
                Blog = dict()
                Blog["Name"] = request.form['H1']
                Blog["Text"] = request.form['TextData']
                User["Blogs"].append(Blog)

            else:
                User["Blogs"] = []
                Blog = dict()
                Blog["Name"] = request.form['H1']
                Blog["Text"] = request.form['TextData']
                User["Blogs"].append(Blog)

            Users[User["Id"]] = User
            with open('static/Users.json', 'w') as Usrs:
                json.dump(Users, Usrs)
                return MainMenu()

    return render_template("user.html", User=User, resp=SovietRespulics, Error=Err, Cblog=CrBl)

if __name__ == "__main__":
    app.run(debug=True)