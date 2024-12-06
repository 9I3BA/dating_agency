import sqlite3
import ttkbootstrap
from tkinter import Toplevel, filedialog, messagebox, Label, Entry, Text, Button, ttk
from PIL import Image, ImageTk
from PIL._tkinter_finder import tk
from ttkbootstrap.constants import *
import tkinter as tk
import os
import shutil

# Создаем подключение к базе данных
db = sqlite3.connect("users.db")
c = db.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users(
    login VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50),
    gender TEXT,
    age INTEGER,
    city TEXT,
    profile_photo TEXT,
    profile_text TEXT
)""")
db.commit()

# Создание и подключение к базе данных
db = sqlite3.connect('users.db')
c = db.cursor()

# Создание таблицы для лайков, если её ещё нет
c.execute("""
CREATE TABLE IF NOT EXISTS likes(
    id INTEGER PRIMARY KEY,
    liked_login VARCHAR(50),
    user_login VARCHAR(50)
)""")
db.commit()

# Создание и подключение к базе данных
db = sqlite3.connect('users.db')
c = db.cursor()

# Создание таблицы для лайков, если её ещё нет
c.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    sender TEXT,
    receiver TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)""")

# Создание таблицы городов, если она не существует
c.execute("""
CREATE TABLE IF NOT EXISTS city (
    id INTEGER PRIMARY KEY,
    name TEXT
)""")

# Главное окно авторизации
window = ttkbootstrap.Window(themename="vapor")
window.title("Авторизация")
window.geometry("500x300+500+200")

# Создаем интерфейс для авторизации
ttkbootstrap.Label(window, text="Введите логин:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=10)
entry_login = ttkbootstrap.Entry(window, width=30, bootstyle=ttkbootstrap.PRIMARY)
entry_login.pack()

# Поле ввода пароля
ttkbootstrap.Label(window, text="Введите пароль:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=10)
entry_password = ttkbootstrap.Entry(window, width=30, show="*", bootstyle=ttkbootstrap.PRIMARY)
entry_password.pack()

# Функция для переключения видимости пароля
def showpass():
    if entry_password["show"] == "*":
        entry_password["show"] = ""
    else:
        entry_password["show"] = "*"

# Окно регистрации нового пользователя
def reg_window():
    # Создаем новое окно для регистрации
    reg_win = Toplevel(window)
    reg_win.title("Регистрация")
    reg_win.geometry("500x600+500+200")

    ttkbootstrap.Label(reg_win, text="Введите логин:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=10)
    entry_reg_login = ttkbootstrap.Entry(reg_win, width=40, bootstyle=ttkbootstrap.PRIMARY)
    entry_reg_login.pack()

    ttkbootstrap.Label(reg_win, text="Введите пароль:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=10)
    entry_reg_password = ttkbootstrap.Entry(reg_win, width=40, bootstyle=ttkbootstrap.PRIMARY)
    entry_reg_password.pack()

    # Выбор пола
    ttkbootstrap.Label(reg_win, text="Выберите пол:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=10)
    gender_var = tk.StringVar(value="")  # Значение по умолчанию (пустое)

    ttkbootstrap.Radiobutton(reg_win, text="Мужской", variable=gender_var, value="Мужской", bootstyle=ttkbootstrap.PRIMARY).pack()
    ttkbootstrap.Radiobutton(reg_win, text="Женский", variable=gender_var, value="Женский", bootstyle=ttkbootstrap.PRIMARY).pack()

    # Выбор города
    ttkbootstrap.Label(reg_win, text="Выберите город:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=10)
    city_var = tk.StringVar(value="")  # Значение по умолчанию (пустое)
    city_combobox = ttk.Combobox(reg_win, textvariable=city_var, state="readonly", width=38)

    # Загрузка городов из базы данных
    c.execute("SELECT name FROM city")
    cities = [row[0] for row in c.fetchall()]
    city_combobox['values'] = cities
    city_combobox.pack(pady=10)

    # Ввод возраста
    ttkbootstrap.Label(reg_win, text="Введите возраст:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=10)
    entry_reg_age = ttkbootstrap.Entry(reg_win, width=40, bootstyle=ttkbootstrap.PRIMARY)
    entry_reg_age.pack()

    # Кнопка завершения регистрации
    ttkbootstrap.Button(reg_win, text="Завершить регистрацию", bootstyle=ttkbootstrap.PRIMARY, command=lambda: register(entry_reg_login.get(), entry_reg_password.get(), gender_var.get(), city_var.get(), entry_reg_age.get(), reg_win,),).pack(pady=20)

# Функция для обработки регистрации пользователя
def register(user_login, user_password, user_gender, user_city, user_age, reg_win):
    try:
        user_age = int(user_age)  # Преобразуем введённый возраст в целое число
    except ValueError:
        ttkbootstrap.dialogs.dialogs.Messagebox.ok("Заполните все поля!", "Ошибка")
        return

    if user_age < 16:  # Проверяем, не меньше ли возраст 16 лет
        ttkbootstrap.dialogs.dialogs.Messagebox.ok("Регистрация невозможна: вам должно быть не менее 16 лет!", "Ошибка")
        return

    # Проверка всех обязательных полей
    if user_login and user_password and user_gender and user_city and user_age:  # Проверка на пустые поля
        c.execute("SELECT login FROM users WHERE login=?", (user_login,))
        if c.fetchone() is None:
            # Обновляем запрос на вставку, чтобы включить пол, возраст, город
            c.execute(
                "INSERT INTO users (login, password, gender, age, city, profile_photo, profile_text) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_login, user_password, user_gender, user_age, user_city, None, None),
            )
            db.commit()
            ttkbootstrap.dialogs.dialogs.Messagebox.ok("Пользователь добавлен в базу данных", "Вы успешно зарегистрировались")
            reg_win.destroy()  # Закрываем окно регистрации
            window.deiconify()  # Возвращаемся к окну авторизации
        else:
            ttkbootstrap.dialogs.dialogs.Messagebox.ok("Такой пользователь уже существует!", "Ошибка")
    else:
        ttkbootstrap.dialogs.dialogs.Messagebox.ok("Заполните все пункты регистрации!", "Ошибка")

# Функция для входа в систему
def login():
    global current_user
    user_login = entry_login.get()
    user_password = entry_password.get()

    # Проверка входа для администратора
    if user_login == "Admin" and user_password == "ADMINNN":
        ttkbootstrap.dialogs.dialogs.Messagebox.ok("Добро пожаловать", "Вы вошли как администратор")
        open_admin_interface()  # Открыть интерфейс администратора
        window.withdraw()  # Скрыть окно авторизации
        return

    # Проверка пользователя в базе данных
    c.execute("SELECT * FROM users WHERE login=? AND password=?", (user_login, user_password))
    user = c.fetchone()
    if user:
        current_user = user
        ttkbootstrap.dialogs.dialogs.Messagebox.ok("Добро пожаловать", "Вы успешно авторизировались")
        open_main_menu()  # Открытие главного меню
        window.withdraw()  # Скрыть окно авторизации
    else:
        ttkbootstrap.dialogs.dialogs.Messagebox.ok("Неверный логин или пароль", "Ошибка")

# Кнопки в окне авторизации
ttkbootstrap.Button(window, text="Показать пароль", command=showpass).pack(pady=10)
ttkbootstrap.Button(window, text="Войти", bootstyle=ttkbootstrap.PRIMARY, command=login).pack(pady=10)
ttkbootstrap.Button(window, text="Зарегистрироваться", bootstyle=ttkbootstrap.PRIMARY, command=reg_window).pack(pady=10)


# Глобальные переменные для хранения текущего пользователя
current_user = None

#Меню администратора
def open_admin_interface():
    admin_win = Toplevel(window)
    admin_win.title("Меню администратора")
    admin_win.geometry("500x400+500+200")

    # Заголовок панели администратора
    ttkbootstrap.Label(admin_win, text="Панель администратора", bootstyle=ttkbootstrap.PRIMARY, font=("Arial", 16)).pack(pady=20)

    # Кнопки администратора
    ttkbootstrap.Button(admin_win, text="Управление пользователями", bootstyle=ttkbootstrap.PRIMARY, command=manage_users).pack(pady=10)
    ttkbootstrap.Button(admin_win, text="Управление городами", bootstyle=PRIMARY, command=open_city_management).pack(pady=10)
    ttkbootstrap.Button(admin_win, text="Чаты пользователей", bootstyle=PRIMARY, command=open_user_chats).pack(pady=10)
    ttkbootstrap.Button(admin_win, text="Завершить сеанс", bootstyle=ttkbootstrap.DANGER, command=window.quit).pack(pady=20)

# Открытие списка чатов конкретного пользователя
def open_user_chats():
    # Окно для ввода логина пользователя
    chat_admin_win = Toplevel(window)
    chat_admin_win.title("Чаты пользователя")
    chat_admin_win.geometry("500x400")

    # Поле ввода логина пользователя
    ttkbootstrap.Label(chat_admin_win, text="Введите логин пользователя:", bootstyle=PRIMARY).pack(pady=10)
    user_login_entry = ttkbootstrap.Entry(chat_admin_win, width=40)
    user_login_entry.pack(pady=10)

    # Фрейм для списка чатов
    chat_list_frame = ttkbootstrap.Frame(chat_admin_win)
    chat_list_frame.pack(fill="both", expand=True, pady=10)

    # Поиск чатов пользователя
    def search_chats():
        # Очистка предыдущего содержимого списка чатов
        for widget in chat_list_frame.winfo_children():
            widget.destroy()

        user_login = user_login_entry.get().strip()

        if not user_login:
            messagebox.showerror("Ошибка", "Введите логин пользователя!")
            return

        # Проверяем, существует ли пользователь
        c.execute("SELECT login FROM users WHERE login=?", (user_login,))
        if not c.fetchone():
            messagebox.showerror("Ошибка", f"Пользователь {user_login} не найден!")
            return

        # Получение чатов пользователя
        c.execute("""
        SELECT DISTINCT
            CASE WHEN sender = ? THEN receiver ELSE sender END AS chat_partner
        FROM messages
        WHERE sender = ? OR receiver = ?
        """, (user_login, user_login, user_login))
        chats = c.fetchall()

        if not chats:
            ttkbootstrap.Label(chat_list_frame, text="У пользователя нет чатов.", bootstyle=PRIMARY).pack(pady=10)
            return

        # Отображение списка чатов
        for chat in chats:
            chat_partner = chat[0]
            ttkbootstrap.Button(
                chat_list_frame,
                text=f"Чат с {chat_partner}",
                bootstyle=PRIMARY,
                command=lambda partner=chat_partner: open_chat_admin(user_login, partner)
            ).pack(pady=5)

    ttkbootstrap.Button(chat_admin_win, text="Найти чаты", bootstyle=PRIMARY, command=search_chats).pack(pady=10)

# Открытие переписки двух пользователей для просмотра администратором
def open_chat_admin(user_login, chat_partner):
    chat_win = Toplevel(window)
    chat_win.title(f"Переписка: {user_login} и {chat_partner}")
    chat_win.geometry("500x400")

    chat_text = Text(chat_win, state='disabled', wrap="word", width=60, height=20)
    chat_text.pack(pady=10)

    # Загрузка переписки
    def load_chat():
        c.execute("""
        SELECT sender, message, timestamp
        FROM messages
        WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
        ORDER BY timestamp
        """, (user_login, chat_partner, chat_partner, user_login))
        messages = c.fetchall()

        chat_text.config(state='normal')
        chat_text.delete("1.0", "end")
        for sender, message, timestamp in messages:
            chat_text.insert("end", f"{timestamp} - {sender}: {message}\n")
        chat_text.config(state='disabled')

    load_chat()

# Окно для управления городами
def open_city_management():
    city_win = Toplevel(window)
    city_win.title("Управление городами")
    city_win.geometry("500x400")

    # Функция для добавления города
    def add_city():
        city_name = city_entry.get().strip()
        if city_name:
            c.execute("INSERT INTO city (name) VALUES (?)", (city_name,))
            db.commit()
            city_entry.delete(0, 'end')
            load_cities()
        else:
            messagebox.showerror("Ошибка", "Название города не может быть пустым")

    # Функция для удаления города
    def delete_city(city_id):
        c.execute("DELETE FROM city WHERE id = ?", (city_id,))
        db.commit()
        load_cities()

    # Поле ввода и кнопка для добавления города
    city_entry = Entry(city_win, width=30)
    city_entry.pack(pady=10)
    ttkbootstrap.Button(city_win, text="Добавить город", bootstyle=PRIMARY, command=add_city).pack(pady=5)

    # Список городов
    cities_frame = ttkbootstrap.Frame(city_win)
    cities_frame.pack(fill="both", expand=True, pady=10)

    # Загрузка и отображение списка городов
    def load_cities():
        # Очистить список городов
        for widget in cities_frame.winfo_children():
            widget.destroy()

        # Загрузить города из базы данных
        c.execute("SELECT id, name FROM city")
        cities = c.fetchall()

        for city_id, city_name in cities:
            city_row = ttkbootstrap.Frame(cities_frame, padding=5)
            city_row.pack(fill="x", pady=2)

            ttkbootstrap.Label(city_row, text=city_name, bootstyle=PRIMARY).pack(side="left", padx=10)
            ttkbootstrap.Button(city_row, text="Удалить", bootstyle=DANGER, command=lambda cid=city_id: delete_city(cid)).pack(side="right", padx=10)

    # Загрузить города при открытии окна
    load_cities()

# Окно управления пользователями (для администратора)
def manage_users():
    users_win = Toplevel(window)
    users_win.title("Управление пользователями")
    users_win.geometry("800x600")

    # Поле поиска
    search_label = ttkbootstrap.Label(users_win, text="Поиск:", bootstyle=PRIMARY)
    search_label.pack(pady=5)
    search_entry = ttkbootstrap.Entry(users_win, width=50, bootstyle=PRIMARY)
    search_entry.pack(pady=5)

    # Функция поиска пользователя
    def search_users():
        query = search_entry.get()
        c.execute("SELECT login, profile_photo, profile_text FROM users WHERE login LIKE ?", (f"%{query}%",))
        display_users(c.fetchall())

    ttkbootstrap.Button(users_win, text="Искать", bootstyle=PRIMARY, command=search_users).pack(pady=5)

    # Таблица пользователей
    users_frame = ttkbootstrap.Frame(users_win)
    users_frame.pack(fill="both", expand=True)

    # Отображение пользователей
    def display_users(users):
        for widget in users_frame.winfo_children():
            widget.destroy()

        for user in users:
            user_frame = ttkbootstrap.Frame(users_frame, padding=10)
            user_frame.pack(fill="x", pady=5)

            ttkbootstrap.Label(user_frame, text=f"Логин: {user[0]}", bootstyle=PRIMARY).pack(side="left", padx=10)
            ttkbootstrap.Button(user_frame, text="Открыть анкету", bootstyle=PRIMARY, command=lambda u=user[0]: open_user_profile(u)).pack(side="right", padx=10)

    # Просмотр анкеты пользователя
    def open_user_profile(user_login):
        profile_win = Toplevel(users_win)
        profile_win.title(f"Анкета пользователя {user_login}")
        profile_win.geometry("500x400+500+200")

        # Загрузка данных пользователя из базы
        c.execute("SELECT profile_photo, profile_text FROM users WHERE login=?", (user_login,))
        user_info = c.fetchone()

        if user_info:
            user_photo, user_text = user_info

            # Отображение фото
            if user_photo:
                try:
                    img = Image.open(user_photo).resize((200, 250))
                    photo = ImageTk.PhotoImage(img)
                    Label(profile_win, image=photo).image = photo
                    Label(profile_win, image=photo).pack(pady=10)
                except:
                    Label(profile_win, text="Фото не загружено").pack(pady=10)
            else:
                Label(profile_win, text="Фото отсутствует").pack(pady=10)

            # Текст профиля
            Label(profile_win, text=f"Логин: {user_login}", font=("Arial", 16)).pack(pady=5)
            Label(profile_win, text=user_text or "Описание отсутствует", wraplength=400, justify="center").pack(pady=10)

        else:
            Label(profile_win, text="Анкета не найдена", font=("Arial", 14)).pack(pady=20)

    # Загрузка всех пользователей при открытии окна
    c.execute("SELECT login, profile_photo, profile_text FROM users")
    display_users(c.fetchall())

# Главное меню пользователя после входа
def open_main_menu():  # Создаем новое окно для главного меню
    main_menu_win = Toplevel(window)
    main_menu_win.title("Главное меню")
    main_menu_win.geometry("400x350+500+200")

    # Кнопки в главное меню
    ttkbootstrap.Button(main_menu_win, text="Уведомления", bootstyle=ttkbootstrap.PRIMARY, command=show_notifications).pack(pady=10)
    ttkbootstrap.Button(main_menu_win, text="Ваши чаты", bootstyle=PRIMARY, command=chats).pack(pady=10)
    ttkbootstrap.Button(main_menu_win, text="Смотреть анкеты", bootstyle=PRIMARY, command=open_filter_and_apply).pack(pady=10)
    ttkbootstrap.Button(main_menu_win, text="Ваша анкета", bootstyle=ttkbootstrap.PRIMARY, command=open_profile).pack(pady=10)
    ttkbootstrap.Button(main_menu_win, text="Завершить сеанс", bootstyle=ttkbootstrap.DANGER, command=window.quit).pack(pady=10)

# Открытие окна чатов пользователя
def chats():
    chats_win = Toplevel(window)
    chats_win.title("Список чатов")
    chats_win.geometry("400x300")

    Label(chats_win, text="Чаты", font=("Arial", 14)).pack(pady=10)

    # Словарь для отслеживания активных чатов
    active_chats = {}

    # Получаем список пользователей, которым понравилась ваша анкета
    c.execute("SELECT user_login FROM likes WHERE liked_login=?", (current_user[1],))
    liked_users = c.fetchall()

    if liked_users:
        for liked_user in liked_users:
            user_login = liked_user[0]
            # Проверяем, поставил ли этот пользователь лайк обратно
            c.execute("SELECT user_login FROM likes WHERE liked_login=? AND user_login=?", (user_login, current_user[1]))
            mutual_like = c.fetchone()

            if mutual_like:
                # Если чат с пользователем не открыт, создаём кнопку
                if user_login not in active_chats:
                    chat_button = Button(
                        chats_win,
                        text=f"Чат с {user_login}",
                        command=lambda user=user_login: open_chat(user, active_chats, chat_button)
                    )
                    chat_button.pack(pady=5)
                    active_chats[user_login] = chat_button
    else:
        Label(chats_win, text="На данный момент у вас нет чатов", font=("Arial", 12)).pack(pady=5)

# Открытие чата с пользователем
def open_chat(username, active_chats, chat_button):
    chat_win = Toplevel(window)
    chat_win.title(f"Чат с {username}")
    chat_win.geometry("400x350")

    # Поле для отображения сообщений
    chat_text = Text(chat_win, state='disabled', width=50, height=15)
    chat_text.pack(pady=10)

    # Поле для ввода нового сообщения
    message_entry = Entry(chat_win, width=50)
    message_entry.pack(pady=(0, 10))

    # Отправка сообщения
    def send_message():
        message = message_entry.get()
        if message:
            # Сохранение сообщения в базу данных
            c.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)", (current_user[1], username, message))
            db.commit()

            # Обновляем поле переписки
            chat_text.config(state='normal')
            chat_text.insert('end', f"Вы: {message}\n")
            chat_text.config(state='disabled')
            message_entry.delete(0, 'end')

    Button(chat_win, text="Отправить", command=send_message).pack(pady=5)

    # Загрузка предыдущих сообщений
    load_previous_messages(chat_text, username)

# Загрузка истории сообщений
def load_previous_messages(chat_text, username):
    c.execute("""
    SELECT sender, message FROM messages WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)""", (current_user[1], username, username, current_user[1]))
    messages = c.fetchall()

    chat_text.config(state='normal')
    for msg in messages:
        chat_text.insert('end', f"{msg[0]}: {msg[1]}\n")
    chat_text.config(state='disabled')

# Открытие окна уведомлений
def show_notifications():
    notifications_win = Toplevel(window)
    notifications_win.title("Уведомления")

    # Создаем поле для уведомлений
    notifications_frame = tk.Frame(notifications_win)
    notifications_frame.pack()

    # Получаем все лайки из базы данных
    c.execute("SELECT user_login FROM likes WHERE liked_login=?", (current_user[1],))
    likes = c.fetchall()

    if likes:
        for like in reversed(likes):  # Перебираем лайки в обратном порядке
            user_login = like[0]
            # Создаем новый Frame для каждого уведомления
            notification_frame = tk.Frame(notifications_frame)
            notification_frame.pack(side="top", fill="x", padx=5, pady=5)

            # Отображаем уведомление
            Label(notification_frame, text=f"Пользователю {user_login} понравилась ваша анкета", font=("Arial", 12)).pack(side="left")
            # Добавляем кнопку "Посмотреть анкету"
            Button(notification_frame, text="Посмотреть анкету", command=lambda login=user_login: show_profile(login)).pack(side="right")
    else:
        Label(notifications_frame, text="Нет уведомлений", font=("Arial", 12)).pack(pady=5)

# Показать анкету пользователя
def show_profile(user_login):
    # Создаем новое окно для профиля пользователя
    profile_win = Toplevel(window)
    profile_win.title("Анкета пользователя")
    profile_win.geometry("500x500+500+200")

    # Получаем информацию о пользователе из базы данных
    c.execute("SELECT profile_photo, profile_text FROM users WHERE login=?", (user_login,))
    user_info = c.fetchone()

    if user_info is None:
        Label(profile_win, text="Профиль не найден", font=("Arial", 14)).pack(pady=20)
        return

    user_photo, user_text = user_info

    # Загружаем и отображаем фотографию, если она есть
    if user_photo:
        try:
            image = Image.open(user_photo)  # Путь к изображению
            image = image.resize((150, 200))  # Изменение размера изображения
            photo = ImageTk.PhotoImage(image)
            Label(profile_win, image=photo).image = photo
            Label(profile_win, image=photo).pack(pady=10)
        except Exception as e:
            print(f"Ошибка при загрузке фото: {e}")
            Label(profile_win, text="Фото недоступно", font=("Arial", 12)).pack(pady=10)

    # Отображение текста профиля
    Label(profile_win, text=f"Логин: {user_login}", font=("Arial", 16)).pack(pady=5)
    Label(profile_win, text=user_text, wraplength=400, justify="center", font=("Arial", 12)).pack(pady=10)

    # Кнопка для лайка профиля
    Button(profile_win, text="Мне нравится", command=lambda: like_user(user_login)).pack(pady=5)

# Лайкнуть пользователя
def like_user(user_login):
    c.execute("INSERT INTO likes (liked_login, user_login) VALUES (?, ?)", (user_login, current_user[0]))
    db.commit()
    messagebox.showinfo("Лайк", f"Вы оценили анкету пользователя: {user_login}")

# Окно для фильтров поиска анкет
def open_filter_and_apply():
    filter_win = Toplevel(window)
    filter_win.title("Фильтры")
    filter_win.geometry("350x450")

    # Пол для выбора пола
    user_gender = tk.StringVar(value="Не указан")
    ttkbootstrap.Label(filter_win, text="Пол:").pack(pady=10)
    ttkbootstrap.Radiobutton(filter_win, text="Мужской", variable=user_gender, value="Мужской").pack()
    ttkbootstrap.Radiobutton(filter_win, text="Женский", variable=user_gender, value="Женский").pack()
    ttkbootstrap.Radiobutton(filter_win, text="Не указан", variable=user_gender, value="Не указан").pack()

    # Поле ввода интересующего возраста (диапазон)
    ttkbootstrap.Label(filter_win, text="Интересующий возраст:").pack(pady=10)
    ttkbootstrap.Label(filter_win, text="От:").pack()
    entry_age_from = ttkbootstrap.Entry(filter_win)
    entry_age_from.pack(pady=5)
    ttkbootstrap.Label(filter_win, text="До:").pack()
    entry_age_to = ttkbootstrap.Entry(filter_win)
    entry_age_to.pack(pady=5)

    # Поле для выбора города
    ttkbootstrap.Label(filter_win, text="Выберите город:").pack(pady=10)
    city_var = tk.StringVar(value="Все города")
    city_combobox = ttk.Combobox(filter_win, textvariable=city_var, state="readonly", width=30)
    city_combobox.pack(pady=5)

    # Загрузка списка городов из базы данных
    c.execute("SELECT name FROM city")
    cities = [row[0] for row in c.fetchall()]
    city_combobox['values'] = ["Все города"] + cities  # Добавляем опцию "Все города"
    city_combobox.current(0)  # Устанавливаем "Все города" по умолчанию

    # Применить фильтр
    def apply_filter():
        gender_filter = user_gender.get()
        age_from_filter = None
        age_to_filter = None
        city_filter = city_var.get()

        # Проверяем, что возраста введены корректно
        try:
            if entry_age_from.get():
                age_from_filter = int(entry_age_from.get())
            if entry_age_to.get():
                age_to_filter = int(entry_age_to.get())
        except ValueError:
            ttkbootstrap.messagebox.showerror("Ошибка", "Возраст должен быть числом.")
            return

        # Закрываем окно фильтров
        filter_win.destroy()

        # Передаём параметры в функцию отображения анкет
        open_announcements_with_filters(
            gender_filter,
            city_filter,
            age_from_filter,
            age_to_filter
        )

    ttkbootstrap.Button(filter_win, text="Применить", bootstyle=PRIMARY, command=apply_filter).pack(pady=20)

# Открытие анкет с учетом фильтров
def open_announcements_with_filters(gender_filter=None, city_filter=None, age_from_filter=None, age_to_filter=None):
    announcements_win = Toplevel(window)
    announcements_win.title("Анкеты пользователей")
    announcements_win.geometry("500x600+500+200")

    current_index = [0]

    # Функция для получения списка пользователей с учетом фильтров
    def fetch_users():
        query = "SELECT login, age, gender, city, profile_photo, profile_text FROM users WHERE login != ?"
        parameters = [current_user[0]]

        if gender_filter and gender_filter != "Не указан":
            query += " AND gender = ?"
            parameters.append(gender_filter)

        if city_filter and city_filter != "Все города":
            query += " AND city = ?"
            parameters.append(city_filter)

        if age_from_filter is not None and age_to_filter is not None:
            query += " AND age BETWEEN ? AND ?"
            parameters.extend([age_from_filter, age_to_filter])
        elif age_from_filter is not None:
            query += " AND age >= ?"
            parameters.append(age_from_filter)
        elif age_to_filter is not None:
            query += " AND age <= ?"
            parameters.append(age_to_filter)

        # Добавляем случайный порядок
        query += " ORDER BY RANDOM()"

        c.execute(query, parameters)
        return c.fetchall()

    # Функция для отображения конкретной анкеты
    def show_user(index):
        for widget in announcements_win.winfo_children():
            widget.destroy()

        if index < 0 or index >= len(users):
            return

        user = users[index]
        user_login, user_age, user_gender, user_city, user_photo, user_text = user

        # Отображение фото пользователя
        if user_photo:
            try:
                image = Image.open(user_photo).resize((150, 200))
                photo = ImageTk.PhotoImage(image)
                Label(announcements_win, image=photo).image = photo
                Label(announcements_win, image=photo).pack(pady=10)
            except:
                Label(announcements_win, text="Фото не загружено").pack()

        # Отображение информации о пользователе
        Label(announcements_win, text=f"Логин: {user_login}", font=("Arial", 16)).pack(pady=5)
        Label(announcements_win, text=f"Возраст: {user_age}", font=("Arial", 16)).pack(pady=5)
        Label(announcements_win, text=f"Пол: {user_gender}", font=("Arial", 16)).pack(pady=5)
        Label(announcements_win, text=f"Город: {user_city}", font=("Arial", 16)).pack(pady=5)
        Label(announcements_win, text=user_text, wraplength=400, justify="center").pack(pady=10)

        # Кнопки навигации
        if index > 0:
            Button(announcements_win, text="Предыдущая", command=lambda: show_user(index - 1)).pack(pady=5)
        if index < len(users) - 1:
            Button(announcements_win, text="Следующая", command=lambda: show_user(index + 1)).pack(pady=5)

        # Кнопка "Мне нравится"
        Button(announcements_win, text="Мне нравится", command=lambda: like_user(user_login)).pack(pady=10)

    users = fetch_users()
    if not users:
        Label(announcements_win, text="Нет доступных анкет").pack(pady=20)
    else:
        show_user(current_index[0])


# Открытие профиля текущего пользователя
def open_profile():
    profile_win = Toplevel(window)
    profile_win.title("Ваша анкета")
    profile_win.geometry("500x600+500+200")

    # Загрузка текущего профиля пользователя
    c.execute("SELECT profile_photo, profile_text FROM users WHERE login=?", (current_user[0],))
    profile_info = c.fetchone()

    global profile_photo_path
    profile_photo_path = profile_info[0] if profile_info and profile_info[0] else ""

    # Отображение текущей фотографии
    def update_photo():
        """Обновляет отображаемую фотографию."""
        for widget in photo_frame.winfo_children():
            widget.destroy()  # Удаляем старые элементы

        if profile_photo_path:
            img = Image.open(profile_photo_path)
            img = img.resize((200, 250), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            photo_label = Label(photo_frame, image=img)
            photo_label.image = img  # сохранить ссылку для отображения
            photo_label.pack(pady=10)
        else:
            photo_label = Label(photo_frame, text="Фото не загружено")
            photo_label.pack(pady=10)

    photo_frame = tk.Frame(profile_win)
    photo_frame.pack()
    update_photo()

    # Поле для текста анкеты
    ttkbootstrap.Label(profile_win, text="Напишите анкету:").pack(pady=10)
    profile_text_box = Text(profile_win, height=5, width=40)
    profile_text_box.pack(pady=10)

    # Предзаполнение текста анкеты
    if profile_info and profile_info[1]:
        profile_text_box.insert("1.0", profile_info[1])

    # Кнопки для загрузки фото и сохранения анкеты
    def save_and_update():
        """Сохраняет профиль и обновляет интерфейс."""
        save_profile(profile_text_box.get("1.0", "end-1c"))
        update_photo()

    ttkbootstrap.Button(profile_win, text="Загрузить фото", bootstyle=ttkbootstrap.PRIMARY, command=upload_photo).pack(pady=5)
    ttkbootstrap.Button(profile_win, text="Сохранить анкету", bootstyle=ttkbootstrap.PRIMARY, command=save_and_update).pack(pady=5)
    ttkbootstrap.Button(profile_win, text="Назад", bootstyle=ttkbootstrap.PRIMARY, command=profile_win.destroy).pack(pady=10)

# Загрузка фото для профиля
def upload_photo():
    global profile_photo_path

    # Создаем папку для хранения фото, если ее еще нет
    photos_dir = "photos"
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir)

    # Диалоговое окно для выбора фото
    file_path = filedialog.askopenfilename(title="Выберите фото", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])

    if file_path:
        # Получаем только имя файла
        file_name = os.path.basename(file_path)

        # Создаем новый путь внутри папки `photos`
        new_file_path = os.path.join(photos_dir, file_name)

        # Копируем файл в папку
        shutil.copy(file_path, new_file_path)

        # Сохраняем путь к новому файлу
        profile_photo_path = new_file_path
        messagebox.showinfo("Загрузка фото", "Фото успешно загружено!")

# Сохранение изменений профиля
def save_profile(profile_text):
    c.execute("UPDATE users SET profile_photo=?, profile_text=? WHERE login=?", (profile_photo_path, profile_text, current_user[0]))
    db.commit()
    messagebox.showinfo("Сохранение анкеты", "Анкета успешно сохранена!")

window.mainloop()
db.close()