from tkinter import *
from PIL import Image, ImageTk
import requests
from tkinter import messagebox

def fetch_pokemon_data():
    url = "https://pokeapi.co/api/v2/pokemon"
    response = requests.get(url)
    data = response.json()
    return data["results"][:9]

def get_pokemon_info(url):
    response = requests.get(url)
    data = response.json()

    if 'forms' in data:
        pokedex_number = data["forms"][0]["url"].split("/")[-2]
        name = data["name"]
        types = [t["type"]["name"] for t in data["types"]]
        sprite_url = data["sprites"]["front_default"]
        stats = [(stat["stat"]["name"], stat["base_stat"]) for stat in data["stats"]]
        height = data["height"]
        weight = data["weight"]
    else:
        pokedex_number = data["id"]
        name = data["name"]
        types = [t["type"]["name"] for t in data["types"]]
        sprite_url = data["sprites"]["front_default"]
        stats = [(stat["stat"]["name"], stat["base_stat"]) for stat in data["stats"]]
        height = data["height"]
        weight = data["weight"]

    return {
        "pokedex_number": pokedex_number,
        "name": name,
        "types": types,
        "sprite_url": sprite_url,
        "stats": stats,
        "height": height,
        "weight": weight
    }
    
# show_pokemon_info in seperate window/ message box
def show_pokemon_info(pokemon_info):
    # Fetch sprite image
    sprite_response = requests.get(pokemon_info["sprite_url"], stream=True)
    sprite_image = Image.open(sprite_response.raw)
    sprite_image = sprite_image.resize((175, 175))
    tk_sprite = ImageTk.PhotoImage(sprite_image)

    # Toplevel window for the detailed Pokemon info
    info_window = Toplevel(bg='#BABABA')
    info_window.title("Pokemon Info")
    info_window.geometry('480x485')

    # Header Frame
    header_frame = Frame(info_window, width=480, height=47, bg="#072ac8")
    header_frame.pack(side=TOP, fill=X)

    # Back Button
    back_button = Button(header_frame, text='<', fg='black', command=info_window.destroy, font=('Arial', 12), bd=2,
                         bg='white', width=3)
    back_button.pack(side=LEFT, padx=(10, 0), pady=5)

    # Title Label
    title_label = Label(header_frame, text="PokÉnfo Center", fg="white", bg="#072ac8", font=('Arial', 12, 'bold'))
    title_label.pack(pady=10)

    # Info frame for everything
    top_frame = Frame(info_window, width=460, height=275, relief=RIDGE, borderwidth=10)
    top_frame.pack(pady=10)

    # Bottom Frame with height and Weight
    bottom_frame = Frame(info_window, width=460, height=135, relief=RIDGE, borderwidth=10)
    bottom_frame.pack()

    breed_label = Label(bottom_frame, text="Breeding", font=('Arial', 12, 'bold'))
    breed_label.place(x=10, y=5)

    height_label = Label(bottom_frame, text="Height", font=('Arial', 12))
    height_label.place(x=135, y=30)

    weight_label = Label(bottom_frame, text="Weight", font=('Arial', 12))
    weight_label.place(x=260, y=30)

    height_frame = Frame(bottom_frame, width=130, height=50, bg='#ded4d4', relief=RIDGE, borderwidth=5)
    height_frame.place(x=100, y=55)

    weight_frame = Frame(bottom_frame, width=130, height=50, bg='#ded4d4', relief=RIDGE, borderwidth=5)
    weight_frame.place(x=225, y=55)

    # Display height and weight information
    height_value_label = Label(height_frame, text=f"{pokemon_info['height']} m", font=('Arial', 10), bg='#ded4d4', fg='black')
    height_value_label.pack(padx=35, pady=5)

    weight_value_label = Label(weight_frame, text=f"{pokemon_info['weight']} kg", font=('Arial', 10), bg='#ded4d4', fg='black')
    weight_value_label.pack(padx=35, pady=5)

    # Display other information in the info window
    id_name_label = Label(top_frame, text=f"# {pokemon_info['pokedex_number']}\n",
                          font=('Arial', 12), anchor='w')
    id_name_label.place(x=10, y=10)

    name_label = Label(top_frame, text=pokemon_info['name'].capitalize(), font=('Arial', 14, 'bold'), anchor='w')
    name_label.place(x=10, y=35)

    type_one_label = Label(top_frame, text=f"{'  '.join(pokemon_info['types'])}", font=('Arial', 13))
    type_one_label.place(x=275, y=10)

    # Color mapping for different stats
    stat_color = {
        'hp': '#5ed498',
        'attack': '#f24c3e',
        'defense': '#fcd85d',
        'speed': '#ff8450'
    }

    stat_names = [stat_name for stat_name, _ in pokemon_info['stats'] if stat_name in stat_color]

    for i, stat_name in enumerate(stat_names):
        # Bar representation for stats
        stat_canvas = Canvas(top_frame, width=200, height=10, bg='white', highlightthickness=1, highlightbackground="black")
        stat_canvas.place(x=10, y=100 + i * 40)

        # Display stat bar with corresponding color
        bar_color = stat_color.get(stat_name, 'lightgray')
        base_stat = next(base_stat for s, base_stat in pokemon_info['stats'] if s == stat_name)
        bar_length = base_stat / 2  # You can adjust this scaling factor based on your preference
        stat_canvas.create_rectangle(0, 0, bar_length, 25, fill=bar_color, outline='')

        # Display stat name on top of the corresponding bar
        stat_label = Label(top_frame, text=f"{stat_name.capitalize()}", font=('Arial', 10))
        stat_label.place(x=10, y=90 + i * 40 - 2, anchor='w')

    # Display sprite image in "top_frame" with ridge border
    sprite_label = Label(top_frame, image=tk_sprite, relief=RIDGE, borderwidth=10)
    sprite_label.place(x=230, y=45)

    sprite_label.image = tk_sprite

def display_pokemon_images(pokemon_data):
    def clear_canvas(canvas_list):
        for canvas in canvas_list:
            canvas.destroy()

    def display_pokemon(pokemon_info, row, col, canvas_list):
        sprite_response = requests.get(pokemon_info["sprite_url"], stream=True)
        sprite_image = Image.open(sprite_response.raw)
        sprite_image = sprite_image.resize((square_size, square_size))
        tk_sprite = ImageTk.PhotoImage(sprite_image)

        canvas = Canvas(root, width=square_size, height=square_size)
        canvas.grid(row=row + 1, column=col, padx=5, pady=10)

        # color mapping to corresponding types
        type_bg_color = {
            'grass': '#01b246',
            'fire': '#fd0400',
            'water': '#159bd8',
            'normal': '#c1b4a7',
            'electric': '#fc8e00',
            'psychic': '#f02b94',
            'fighting': '#992e13',
            'rock': '#d08f01',
            'ground': '#fdc101',
            'flying': '#567edd',
            'bug': '#84940d',
            'poison': '#a2398c',
            'dark': '#39281d',
            'ghost': '#43419d',
            'ice': '#0bd1f6',
            'steel': '#81807e',
            'dragon': '#8165e0',
            'fairy': '#faa7f6'
        }

        if len(pokemon_info['types']) == 2:
            bg_color1 = type_bg_color.get(pokemon_info['types'][0], 'lightgray')
            bg_color2 = type_bg_color.get(pokemon_info['types'][1], 'lightgray')
            canvas.create_rectangle(0, 0, square_size / 2, square_size, fill=bg_color1, outline='')
            canvas.create_rectangle(square_size / 2, 0, square_size, square_size, fill=bg_color2, outline='')
        else:
            bg_color = type_bg_color.get(pokemon_info['types'][0], 'lightgray')
            canvas.create_rectangle(0, 0, square_size, square_size, fill=bg_color, outline='')

        canvas.create_image(0, 0, anchor='nw', image=tk_sprite)
        canvas.bind("<Button-1>", lambda event, p=pokemon_info: show_pokemon_info(p))
        canvas.image = tk_sprite

        # Append the canvas to the list for reference
        canvas_list.append(canvas)

    # Clear the canvas and display the new images
    def search_button_clicked():
        query = entry_widget.get().lower()

        # Fetch Pokémon info based on the search query
        search_url = f"https://pokeapi.co/api/v2/pokemon/{query.lower()}"
        search_response = requests.get(search_url)

        if search_response.status_code == 200:
            pokemon_info = get_pokemon_info(search_url)
            clear_canvas(pokemon_canvases)

            # Display the found Pokémon
            display_pokemon(pokemon_info, 0, 0, pokemon_canvases)
        else:
            messagebox.showinfo("Pokémon Not Found", f"No Pokémon found with the name '{query}'.")

    root = Tk()
    root.title("PokÉnfo Center")
    root.geometry('480x485')
    
    # Icon Image
    icon_image = Image.open("Python Assessment II/pokebal-clear.png")  # Replace "path_to_pokeball_icon.ico" with the actual path to your Pokeball icon file
    icon_image = icon_image.resize((32, 32))
    tk_icon = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, tk_icon)

    header_frame = Frame(root, width=480, height=47, bg="#072ac8")
    header_frame.grid(row=0, column=0, columnspan=3)

    entry_widget = Entry(header_frame, width=35, font=('Arial', 12), bd=5, relief=RIDGE)
    entry_widget.place(relx=0.05, rely=0.5, anchor='w')

    B1 = Button(header_frame, text='Search', width=10, height=1, bg='lightgray', font=('Arial', 10), bd=2, relief=RIDGE)
    B1.place(relx=0.95, rely=0.5, anchor='e')
    B1.configure(command=search_button_clicked)

    entry_widget.config(fg="black", bg="white", highlightthickness=0, borderwidth=5, insertbackground='black')

    square_size = 110
    pokemon_canvases = []

    for i, pokemon in enumerate(pokemon_data):
        row, col = divmod(i, 3)
        pokemon_info = get_pokemon_info(pokemon["url"])
        display_pokemon(pokemon_info, row, col, pokemon_canvases)

    bottom_container = Frame(root, width=470, height=30, bg="#072ac8")
    bottom_container.place(x=5, y=450)  # Adjusted row placement

    title_label = Label(bottom_container, text="PokÉnfo Center", fg="white", bg="#072ac8", font=('Arial', 12, 'bold'))
    title_label.place(relx=0.5, rely=0.5, anchor='center')

    root.mainloop()

if __name__ == "__main__":
    pokemon_data = fetch_pokemon_data()
    display_pokemon_images(pokemon_data)