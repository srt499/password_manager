import tkinter.messagebox
from tkinter import *
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    [password_list.append(choice(letters)) for _ in range(randint(8, 10))]
    [password_list.append(choice(numbers)) for _ in range(randint(2, 4))]
    [password_list.append(choice(symbols)) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)
    # Copying generated password to clipboard (so it can be pasted)
    pyperclip.copy(password)

    # Enter password into the password field
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    new_data = {
        website_entry.get(): {
            "email": email_entry.get(),
            "password": password_entry.get(),
        }
    }

    if len(website_entry.get()) < 1 or len(password_entry.get()) < 1:
        tkinter.messagebox.showerror(title="Missing Info", message="You did not enter all the correct info, please try again.")
    else:
        try:
            with open('data.json', 'r') as f:
                # Reading old data
                data = json.load(f)
                # Updating old data with new data
                data.update(new_data)
        except FileNotFoundError:
            pass
            data = new_data
        finally:
            with open("data.json", "w") as f:
                # Saving updated data
                json.dump(data, f, indent=4)

            website_entry.delete(0, END)
            password_entry.delete(0, END)


def search():
    website = website_entry.get()

    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        tkinter.messagebox.showinfo(title="Login Information", message="This login info does not exist.")
    else:
        if website in data:
            tkinter.messagebox.showinfo(title="Login Information", message=f"Website: {website}\n"
                                                                           f"Email: {data[website]['email']}\n"
                                                                           f"Password: {data[website]['password']}")
        elif website == "":
            tkinter.messagebox.showinfo(title="Error", message=f"No website name was entered.")
        else:
            tkinter.messagebox.showinfo(title="Error", message=f"No details for {website} exist.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
password_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=password_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=24)
website_entry.focus()
website_entry.get()
website_entry.grid(row=1, column=1, sticky='nsew')
email_entry = Entry(width=41)
email_entry.insert(0, "srt499@yahoo.com")
email_entry.grid(row=2, column=1, columnspan=2, sticky='nsew')
password_entry = Entry(width=24)
password_entry.grid(row=3, column=1, sticky='nsew')

# Buttons
generate_password_button = Button(text="Generate Password", command=gen_password, width=15)
generate_password_button.grid(column=2, row=3, sticky="w")
add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky='w')
search_button = Button(text="Search", width=15, command=search)
search_button.grid(row=1, column=2, sticky="w")

window.mainloop()
