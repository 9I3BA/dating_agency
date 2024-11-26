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

# Главное окно авторизации
window = ttkbootstrap.Window(themename="vapor")
window.title("Авторизация")
window.geometry("500x300+500+200")

# Создаем интерфейс для авторизации
ttkbootstrap.Label(window, text="Введите логин:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=10)
entry_login = ttkbootstrap.Entry(window, width=30, bootstyle=ttkbootstrap.PRIMARY)
entry_login.pack()

ttkbootstrap.Label(window, text="Введите пароль:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=10)

entry_password = ttkbootstrap.Entry(window, width=30, show="*", bootstyle=ttkbootstrap.PRIMARY)
entry_password.pack()
def showpass():
    if entry_password["show"] == "*":
        entry_password["show"] = ""
    else:
        entry_password["show"] = "*"
def reg_window():
    # Создаем новое окно для регистрации
    reg_win = Toplevel(window)
    reg_win.title("Регистрация")
    reg_win.geometry("500x500+500+200")

    ttkbootstrap.Label(reg_win, text="Введите логин:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=20)
    entry_reg_login = ttkbootstrap.Entry(reg_win, width=40, bootstyle=ttkbootstrap.PRIMARY)
    entry_reg_login.pack()

    ttkbootstrap.Label(reg_win, text="Введите пароль:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=20)
    entry_reg_password = ttkbootstrap.Entry(reg_win, width=40, show="*", bootstyle=ttkbootstrap.PRIMARY)
    entry_reg_password.pack()

    # Добавляем выбор пола
    ttkbootstrap.Label(reg_win, text="Выберите пол:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=20)

    gender_var = tk.StringVar(value="Не указан")  # Устанавливаем значение по умолчанию

    ttkbootstrap.Radiobutton(reg_win, text="Мужчина", variable=gender_var, value="Мужчина", bootstyle=ttkbootstrap.PRIMARY).pack()
    ttkbootstrap.Radiobutton(reg_win, text="Женщина", variable=gender_var, value="Женщина", bootstyle=ttkbootstrap.PRIMARY).pack()
    ttkbootstrap.Radiobutton(reg_win, text="Не указан", variable=gender_var, value="Не указан", bootstyle=ttkbootstrap.PRIMARY).pack()

    # Добавляем ввод возраста
    ttkbootstrap.Label(reg_win, text="Введите возраст:", bootstyle=ttkbootstrap.PRIMARY).pack(pady=20)
    entry_reg_age = ttkbootstrap.Entry(reg_win, width=40, bootstyle=ttkbootstrap.PRIMARY)
    entry_reg_age.pack()

    ttkbootstrap.Button(reg_win, text="Завершить регистрацию", bootstyle=ttkbootstrap.PRIMARY, command=lambda: register(entry_reg_login.get(), entry_reg_password.get(), gender_var.get(), entry_reg_age.get(), reg_win)).pack(pady=20)

def register(user_login, user_password, user_gender, user_age, reg_win):
    if user_login and user_password and user_age:  # Проверка на пустые поля
        c.execute("SELECT login FROM users WHERE login=?", (user_login,))
        if c.fetchone() is None:
            # Обновляем запрос на вставку, чтобы включить пол и возраст
            c.execute("INSERT INTO users (login, password, gender, age) VALUES (?, ?, ?, ?)", (user_login, user_password, user_gender, user_age))
            db.commit()
            ttkbootstrap.dialogs.dialogs.Messagebox.ok("Вы успешно зарегистрировались!", "Регистрация")
            reg_win.destroy()  # Закрываем окно регистрации
            window.deiconify()  # Возвращаемся к окну авторизации
        else:
            ttkbootstrap.dialogs.dialogs.Messagebox.ok("Ошибка", "Такой пользователь уже существует!")
    else:
        ttkbootstrap.dialogs.dialogs.Messagebox.ok("Ошибка", "Пожалуйста, заполните все поля!")

def login():
    global current_user
    user_login = entry_login.get()
    user_password = entry_password.get()

    if user_login == "Admin" and user_password == "ADMINNN":
        ttkbootstrap.dialogs.dialogs.Messagebox.ok("Добро пожаловать", "Вы вошли как администратор")
        open_admin_interface()  # Открыть интерфейс администратора
        window.withdraw()  # Скрыть окно авторизации
        return

    c.execute("SELECT * FROM users WHERE login=? AND password=?", (user_login, user_password))
    user = c.fetchone()
    if user:
        current_user = user
        ttkbootstrap.dialogs.dialogs.Messagebox.ok("Добро пожаловать", "Вы успешно авторизировались")
        open_main_menu()  # Открытие главного меню
        window.withdraw()  # Скрыть окно авторизации
    else:
        ttkbootstrap.dialogs.dialogs.Messagebox.ok("Ошибка", "Неверный логин или пароль")

ttkbootstrap.Button(window, text="Показать пароль", command=showpass).pack(pady=10)
ttkbootstrap.Button(window, text="Войти", bootstyle=ttkbootstrap.PRIMARY, command=login).pack(pady=10)
ttkbootstrap.Button(window, text="Зарегистрироваться", bootstyle=ttkbootstrap.PRIMARY, command=reg_window).pack(pady=10)


# Глобальные переменные для хранения текущего пользователя
current_user = None

def open_admin_interface():
    admin_win = Toplevel(window)
    admin_win.title("Администраторский интерфейс")
    admin_win.geometry("500x400+500+200")

    ttkbootstrap.Label(admin_win, text="Панель администратора", bootstyle=ttkbootstrap.PRIMARY, font=("Arial", 16)).pack(pady=20)

    # Кнопки администратора
    ttkbootstrap.Button(admin_win, text="Управление пользователями", bootstyle=ttkbootstrap.PRIMARY, command=manage_users).pack(pady=10)
    ttkbootstrap.Button(admin_win, text="Выход", bootstyle=ttkbootstrap.DANGER, command=admin_win.destroy).pack(pady=20)

def manage_users():
    users_win = Toplevel(window)
    users_win.title("Управление пользователями")
    users_win.geometry("800x600")

    # Поле поиска
    search_label = ttkbootstrap.Label(users_win, text="Поиск:", bootstyle=PRIMARY)
    search_label.pack(pady=5)
    search_entry = ttkbootstrap.Entry(users_win, width=50, bootstyle=PRIMARY)
    search_entry.pack(pady=5)

    def search_users():
        query = search_entry.get()
        c.execute("SELECT login, profile_photo, profile_text FROM users WHERE login LIKE ?", (f"%{query}%",))
        display_users(c.fetchall())

    ttkbootstrap.Button(users_win, text="Искать", bootstyle=PRIMARY, command=search_users).pack(pady=5)

    # Таблица пользователей
    users_frame = ttkbootstrap.Frame(users_win)
    users_frame.pack(fill="both", expand=True)

    def display_users(users):
        for widget in users_frame.winfo_children():
            widget.destroy()

        for user in users:
            user_frame = ttkbootstrap.Frame(users_frame, padding=10)
            user_frame.pack(fill="x", pady=5)

            ttkbootstrap.Label(user_frame, text=f"Логин: {user[0]}", bootstyle=PRIMARY).pack(side="left", padx=10)
            ttkbootstrap.Button(user_frame, text="Редактировать", bootstyle=PRIMARY,command=lambda u=user[0]: edit_user(u)).pack(side="right", padx=10)
            ttkbootstrap.Button(user_frame, text="Удалить", bootstyle=DANGER,command=lambda u=user[0]: delete_user(u)).pack(side="right", padx=10)

    def edit_user(login):
        edit_win = Toplevel(users_win)
        edit_win.title(f"Редактирование пользователя {login}")

        c.execute("SELECT profile_photo, profile_text FROM users WHERE login=?", (login,))
        user = c.fetchone()
        if not user:
            return

        ttkbootstrap.Label(edit_win, text="Описание профиля:").pack(pady=5)
        text_entry = Text(edit_win, height=5, width=50)
        text_entry.insert("1.0", user[1] if user[1] else "")
        text_entry.pack(pady=5)

        def save_changes():
            new_text = text_entry.get("1.0", "end-1c")
            c.execute("UPDATE users SET profile_text=? WHERE login=?", (new_text, login))
            db.commit()
            messagebox.showinfo("Успех", "Данные пользователя обновлены")
            edit_win.destroy()

        ttkbootstrap.Button(edit_win, text="Сохранить", bootstyle=PRIMARY, command=save_changes).pack(pady=10)

    def delete_user(login):
        if messagebox.askyesno("Удаление", f"Вы уверены, что хотите удалить пользователя {login}?"):
            c.execute("DELETE FROM users WHERE login=?", (login,))
            db.commit()
            search_users()  # Обновить список пользователей

    # Загрузка всех пользователей при открытии окна
    c.execute("SELECT login, profile_photo, profile_text FROM users")
    display_users(c.fetchall())

def open_main_menu():  # Создаем новое окно для главного меню
    main_menu_win = Toplevel(window)
    main_menu_win.title("Главное меню")
    main_menu_win.geometry("400x300+500+200")

    # Добавляем кнопки в главное меню
    ttkbootstrap.Button(main_menu_win, text="Чат", bootstyle=PRIMARY, command=chats).pack(pady=10)
    ttkbootstrap.Button(main_menu_win, text="Фильтр анкет", bootstyle=PRIMARY, command=open_filter_and_apply).pack(pady=10)
    ttkbootstrap.Button(main_menu_win, text="Уведомления", bootstyle=ttkbootstrap.PRIMARY, command=show_notifications).pack(pady=10)
    ttkbootstrap.Button(main_menu_win, text="Все анкеты", bootstyle=ttkbootstrap.PRIMARY, command=open_announcements_with_filters).pack(pady=10)
    ttkbootstrap.Button(main_menu_win, text="Профиль", bootstyle=ttkbootstrap.PRIMARY, command=open_profile).pack(pady=10)
    ttkbootstrap.Button(main_menu_win, text="Выход", bootstyle=ttkbootstrap.PRIMARY, command=main_menu_win.destroy).pack(pady=10)

def chats():
    chats_win = Toplevel(window)
    chats_win.title("Чат")
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
        Label(chats_win, text="Нет пользователей, которым понравилась ваша анкета", font=("Arial", 12)).pack(pady=5)

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


def load_previous_messages(chat_text, username):
    # Получаем и отображаем предыдущие сообщения
    c.execute("""
    SELECT sender, message FROM messages WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)""", (current_user[1], username, username, current_user[1]))
    messages = c.fetchall()

    chat_text.config(state='normal')
    for msg in messages:
        chat_text.insert('end', f"{msg[0]}: {msg[1]}\n")
    chat_text.config(state='disabled')

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

# Предполагаем, что вы объявили users глобально в начале вашего скрипта

def show_profile(user_login):
    # Создаем новое окно для профиля пользователя
    profile_win = Toplevel(window)
    profile_win.title("Профиль пользователя")
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

def like_user(user_login):
    c.execute("INSERT INTO likes (liked_login, user_login) VALUES (?, ?)", (user_login, current_user[0]))
    db.commit()
    messagebox.showinfo("Лайк", f"Вы лайкнули анкету пользователя: {user_login}")

def open_filter_and_apply():
    filter_win = Toplevel(window)
    filter_win.title("Фильтры")
    filter_win.geometry("300x200")

    user_gender = tk.StringVar(value="Не указан")  # Переменная для пола
    entry_age = ttkbootstrap.Entry(filter_win)    # Поле ввода возраста

    ttkbootstrap.Label(filter_win, text="Пол:").pack(pady=10)
    ttkbootstrap.Radiobutton(filter_win, text="Мужчина", variable=user_gender, value="Мужчина").pack()
    ttkbootstrap.Radiobutton(filter_win, text="Женщина", variable=user_gender, value="Женщина").pack()
    ttkbootstrap.Radiobutton(filter_win, text="Не указан", variable=user_gender, value="Не указан").pack()

    ttkbootstrap.Label(filter_win, text="Минимальный возраст:").pack(pady=10)
    entry_age.pack()

    def apply_filter():
        gender_filter = user_gender.get()
        try:
            age_filter = int(entry_age.get()) if entry_age.get() else None
        except ValueError:
            messagebox.showerror("Ошибка", "Возраст должен быть числом.")
            return

        filter_win.destroy()  # Закрываем окно фильтров
        open_announcements_with_filters(gender_filter, age_filter)  # Открываем анкеты с фильтром

    ttkbootstrap.Button(filter_win, text="Применить", bootstyle=PRIMARY, command=apply_filter).pack(pady=10)

def open_announcements_with_filters(gender_filter=None, age_filter=None):
    announcements_win = Toplevel(window)
    announcements_win.title("Анкеты пользователей")
    announcements_win.geometry("500x500+500+200")

    current_index = [0]

    def fetch_users():
        query = "SELECT login, age, gender, profile_photo, profile_text FROM users WHERE login != ?"
        parameters = [current_user[0]]

        if gender_filter and gender_filter != "Не указан":
            query += " AND gender = ?"
            parameters.append(gender_filter)

        if age_filter:
            query += " AND age >= ?"
            parameters.append(age_filter)

        c.execute(query, parameters)
        return c.fetchall()

    def show_user(index):
        for widget in announcements_win.winfo_children():
            widget.destroy()

        if index < 0 or index >= len(users):
            return

        user = users[index]
        user_login, user_age, user_gender, user_photo, user_text = user

        if user_photo:
            try:
                image = Image.open(user_photo).resize((150, 200))
                photo = ImageTk.PhotoImage(image)
                Label(announcements_win, image=photo).image = photo
                Label(announcements_win, image=photo).pack(pady=10)
            except:
                Label(announcements_win, text="Фото не загружено").pack()
        Label(announcements_win, text=f"Логин: {user_login}", font=("Arial", 16)).pack(pady=5)
        Label(announcements_win, text=f"Возраст: {user_age}", font=("Arial", 16)).pack(pady=5)
        Label(announcements_win, text=f"Пол: {user_gender}", font=("Arial", 16)).pack(pady=5)
        Label(announcements_win, text=user_text, wraplength=400, justify="center").pack(pady=10)

        if index > 0:
            Button(announcements_win, text="Предыдущая", command=lambda: show_user(index - 1)).pack(pady=5)
        if index < len(users) - 1:
            Button(announcements_win, text="Следующая", command=lambda: show_user(index + 1)).pack(pady=5)

        Button(announcements_win, text="Мне нравится", command=lambda: like_user(user_login)).pack(pady=10)

    users = fetch_users()
    if not users:
        Label(announcements_win, text="Нет доступных анкет").pack(pady=20)
    else:
        show_user(current_index[0])

def open_profile():
    profile_win = Toplevel(window)
    profile_win.title("Профиль")
    profile_win.geometry("500x600+500+200")

    # Загрузка текущего профиля пользователя
    c.execute("SELECT profile_photo, profile_text FROM users WHERE login=?", (current_user[0],))
    profile_info = c.fetchone()

    global profile_photo_path
    profile_photo_path = profile_info[0] if profile_info and profile_info[0] else ""

    # Отображение текущей фотографии
    if profile_photo_path:
        img = Image.open(profile_photo_path)
        img = img.resize((200, 250), Image.LANCZOS)  # Изменено с ANTIALIAS на LANCZOS
        img = ImageTk.PhotoImage(img)
        photo_label = Label(profile_win, image=img)
        photo_label.image = img  # сохранить ссылку для отображения
        photo_label.pack(pady=10)
    else:
        photo_label = Label(profile_win, text="Фото не загружено")
        photo_label.pack(pady=10)

    # Поле для текста анкеты
    ttkbootstrap.Label(profile_win, text="Напишите анкету:").pack(pady=10)
    profile_text_box = Text(profile_win, height=5, width=40)
    profile_text_box.pack(pady=10)

    # Предзаполнение текста анкеты
    if profile_info and profile_info[1]:
        profile_text_box.insert("1.0", profile_info[1])

    # Кнопки для загрузки фото и сохранения анкеты
    ttkbootstrap.Button(profile_win, text="Загрузить фото", bootstyle=ttkbootstrap.PRIMARY, command=upload_photo).pack(pady=5)
    ttkbootstrap.Button(profile_win, text="Сохранить анкету", bootstyle=ttkbootstrap.PRIMARY, command=lambda: save_profile(profile_text_box.get("1.0", "end-1c"))).pack(pady=5)
    ttkbootstrap.Button(profile_win, text="Назад", bootstyle=ttkbootstrap.PRIMARY, command=profile_win.destroy).pack(pady=10)

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

def save_profile(profile_text):
    c.execute("UPDATE users SET profile_photo=?, profile_text=? WHERE login=?", (profile_photo_path, profile_text, current_user[0]))
    db.commit()
    messagebox.showinfo("Сохранение профиля", "Профиль успешно сохранен!")

window.mainloop()
db.close()