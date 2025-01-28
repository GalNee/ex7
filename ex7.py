import csv
from operator import contains

# Global BST root
ownerRoot = None


########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {"ID": int(row[0]), "Name": str(row[1]), "Type": str(row[2]), "HP": int(row[3]), "Attack": int(row[4]),
                 "Can Evolve": str(row[5]).upper()}
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")


########################
# 1) Helper Functions
########################

# a function to inout an int and make sure it's an int
def read_int_safe(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)


# a function to get the pokemon by the id
def get_poke_dict_by_id(poke_id):
    if 0 < poke_id <= len(HOENN_DATA):
        return HOENN_DATA[poke_id - 1]
    return None


# a function to print a pokemon list
def display_pokemon_list(poke_list):
    if len(poke_list) == 0:
        print("There are no Pokemons in this Pokedex that match the criteria.")
    else:
        for pokemon in poke_list:
            print(f"ID: {pokemon['ID']}, Name: {pokemon['Name']}, Type: {pokemon['Type']}, HP: {pokemon['HP']},"
                  f" Attack: {pokemon['Attack']}, Can Evolve: {pokemon['Can Evolve']}")


########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, pokedex):
    owner = {"name": owner_name, "pokedex": pokedex, "left": None, "right": None}
    return owner


# a function to inset an owner to the bst by name
def insert_owner_bst(root, new_node):
    if root["name"].lower() > new_node["name"].lower():
        if root["left"] is None:
            root["left"] = new_node
        else:
            insert_owner_bst(root["left"], new_node)
    else:
        if root["right"] is None:
            root["right"] = new_node
        else:
            insert_owner_bst(root["right"], new_node)


# a function that returns the owner by a given name
def find_owner_bst(root, owner_name):
    if root is None:
        return None
    if root["name"].lower() == owner_name.lower():
        return root
    if root["name"].lower() > owner_name.lower():
        return find_owner_bst(root["left"], owner_name)
    if root["name"].lower() < owner_name.lower():
        return find_owner_bst(root["right"], owner_name)


# a function that gets a root and returns it with it deleted
def remove_owner_bst(root):
    if root["left"] is None:
        return root["right"]
    if root["right"] is None:
        return root["left"]
    # if the root has 2 "children" then swap it with the next biggest value(by name)
    cur = root["right"]
    prev = None
    while cur['left'] is not None:
        prev = cur
        cur = cur['left']
    root["name"] = cur["name"]
    root["pokedex"] = cur["pokedex"]
    if prev is None:
        root["right"] = cur["right"]
    else:
        prev["left"] = cur["right"]
    return root


# a function that finds the owner by name and removes it
def delete_owner_bst_by_name(root, owner_name):
    if root["name"].lower() > owner_name.lower():
        root["left"] = delete_owner_bst_by_name(root["left"], owner_name)
        return root
    if root["name"].lower() < owner_name.lower():
        root["right"] = delete_owner_bst_by_name(root["right"], owner_name)
        return root
    return remove_owner_bst(root)


def delete_pokedex():
    global ownerRoot
    name = input("Enter owner to delete: ")
    if find_owner_bst(ownerRoot, name) is None:
        print(f"Owner '{name}' not found.")
        return
    print(f"Deleting {name}'s entire Pokedex...")
    ownerRoot = delete_owner_bst_by_name(ownerRoot, name)
    print("Pokedex deleted.")


# a function to add an owner to the bfs
def open_pokedex_menu():
    global ownerRoot
    name = input("Owner name: ")
    if find_owner_bst(ownerRoot, name) is not None:
        print(f"Owner '{name}' already exists. No new Pokedex created.")
        return
    choice = read_int_safe('''Choose your starter Pokemon:
1) Treecko
2) Torchic
3) Mudkip
Your choice: ''')
    pokemon = get_poke_dict_by_id(3 * choice - 2)
    owner = create_owner_node(name, [pokemon])
    if ownerRoot is None:
        ownerRoot = owner
    else:
        insert_owner_bst(ownerRoot, owner)
    print(f"New Pokedex created for {name} with starter {pokemon['Name']}.")


########################
# 3) BST Traversals
########################

# a funcrion to print the owners by level in the bfs
def bfs_traversal(root):
    queue = [root]
    counter = 0
    while counter < len(queue):
        print_owner(queue[counter])
        if queue[counter]["left"] is not None:
            queue.append(queue[counter]["left"])
        if queue[counter]["right"] is not None:
            queue.append(queue[counter]["right"])
        counter += 1


def pre_order(root):
    if root is None:
        return
    print_owner(root)
    pre_order(root["left"])
    pre_order(root["right"])


def in_order(root):
    if root is None:
        return
    in_order(root["left"])
    print_owner(root)
    in_order(root["right"])


def post_order(root):
    if root is None:
        return
    post_order(root["left"])
    post_order(root["right"])
    print_owner(root)


########################
# 4) Pokedex Operations
########################

# a function to add a pokemon to an owner
def add_pokemon_to_owner(owner_node):
    pok_id = read_int_safe("Enter Pokemon ID to add: ")
    if contains(owner_node["pokedex"], get_poke_dict_by_id(pok_id)):
        print("Pokemon already in the list. No changes made.")
        return
    owner_node["pokedex"].append(get_poke_dict_by_id(pok_id))
    print(f"Pokemon {owner_node["pokedex"][-1]["Name"]} (ID {owner_node["pokedex"][-1]["ID"]})"
          f" added to {owner_node["name"]}'s Pokedex.")


# a function to release a pokemon
def release_pokemon_by_name(owner_node):
    name = input("Enter Pokemon Name to release: ")
    for i in range(len(owner_node["pokedex"])):
        if owner_node["pokedex"][i]['Name'].lower() == name.lower():
            owner_node["pokedex"].pop(i)
            print(f"Releasing {owner_node['pokedex'][i]['Name']} from {owner_node['name']}.")
            return
    print(f"No Pokemon named '{name}' in {owner_node['name']}'s Pokedex")


def evolve_pokemon_by_name(owner_node):
    name = input("Enter Pokemon Name to evolve: ")
    for i in range(len(owner_node["pokedex"])):
        if owner_node["pokedex"][i]['Name'].lower() == name.lower():
            old_pok = owner_node["pokedex"][i]
            # if the pokemon can't evolve
            if not old_pok['Can Evolve']:
                print(f"Pokemon {owner_node['pokedex'][i]['Name']} (ID {owner_node['pokedex'][i]['ID']})"
                      " can't evolve.")
                return
            new_pok = get_poke_dict_by_id(old_pok['ID'] + 1)
            print(f"Pokemon evolved from {old_pok['Name']} (ID {old_pok['ID']}) to {new_pok['Name']} "
                  "(ID {new_pok['ID']}).")
            owner_node['pokedex'].pop(i)
            # if the evolved pokemon is already in the list
            if contains(owner_node["pokedex"], new_pok['Name']):
                print(f'{new_pok['Name']} was already present; releasing it immediately.')
            else:
                owner_node["pokedex"].append(new_pok)
            return
    print(f"No Pokemon named '{name}' in {owner_node['name']}'s Pokedex")


########################
# 5) Sorting Owners by # of Pokemon
########################
#a function to gather all the pokemons to a list
def gather_all_owners(root, arr):
    if root is None:
        return
    arr.append(create_owner_node(root["name"], root["pokedex"]))
    gather_all_owners(root["left"], arr)
    gather_all_owners(root["right"], arr)


def sort_owners_by_num_pokemon():
    global ownerRoot
    if ownerRoot is None:
        print("No owners at all.")
        return
    arr = []
    gather_all_owners(ownerRoot, arr)
    #bubble sort
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            if (len(arr[j]["pokedex"]) > len(arr[j + 1]["pokedex"]) or (
                    len(arr[j]["pokedex"]) == len(arr[j + 1]["pokedex"]) and arr[j]["name"].lower() > arr[j + 1][
                "name"].lower())):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    ownerRoot = arr[0]
    print("=== The Owners we have, sorted by number of Pokemons ===")
    for i in range(len(arr)):
        print(f"Owner: {arr[i]["name"]} (has {len(arr[i]["pokedex"])} Pokemon)")
        if i != 0:
            insert_owner_bst(ownerRoot, arr[i])


########################
# 6) Print All
########################

def print_all_owners():
    choice = read_int_safe('''1) BFS
2) Pre-Order
3) In-Order
4) Post-Order
Your choice: ''')
    if choice == 1:
        bfs_traversal(ownerRoot)
    elif choice == 2:
        pre_order(ownerRoot)
    elif choice == 3:
        in_order(ownerRoot)
    elif choice == 4:
        post_order(ownerRoot)


def print_owner(owner_node):
    print(f"\nOwner: {owner_node['name']}")
    display_pokemon_list(owner_node["pokedex"])


########################
# 7) The Display Filter Sub-Menu
########################

def display_certain_type(pokedex):
    pok_type = input("Which Type? (e.g. GRASS, WATER): ")
    displayed = []
    for pokemon in pokedex:
        if pokemon["Type"].lower() == pok_type.lower():
            displayed.append(pokemon)
    display_pokemon_list(displayed)


def display_only_evolvable(pokedex):
    displayed = []
    for pokemon in pokedex:
        if pokemon['Can Evolve']:
            displayed.append(pokemon)
    display_pokemon_list(displayed)


def display_above_attack(pokedex):
    attack_min = read_int_safe("Enter Attack threshold: ")
    displayed = []
    for pokemon in pokedex:
        if pokemon['Attack'] >= attack_min:
            displayed.append(pokemon)
    display_pokemon_list(displayed)


def display_above_hp(pokedex):
    hp_min = read_int_safe("Enter HP threshold: ")
    displayed = []
    for pokemon in pokedex:
        if pokemon['HP'] >= hp_min:
            displayed.append(pokemon)
    display_pokemon_list(displayed)


def display_with_starting_letters(pokedex):
    starting_letters = input("Starting letter(s): ")
    displayed = []
    for pokemon in pokedex:
        if pokemon['Name'].startswith(starting_letters):
            displayed.append(pokemon)
    display_pokemon_list(displayed)


def display_filter_sub_menu(owner_node):
    choice = 0
    while choice != 7:
        choice = read_int_safe('''
-- Display Filter Menu --
1. Only a certain Type
2. Only Evolvable
3. Only Attack above __
4. Only HP above __
5. Only names starting with letter(s)
6. All of them!
7. Back
Your choice: ''')
        if choice == 1:
            display_certain_type(owner_node["pokedex"])
        elif choice == 2:
            display_only_evolvable(owner_node["pokedex"])
        elif choice == 3:
            display_above_attack(owner_node["pokedex"])
        elif choice == 4:
            display_above_hp(owner_node["pokedex"])
        elif choice == 5:
            display_with_starting_letters(owner_node["pokedex"])
        elif choice == 6:
            display_pokemon_list(owner_node["pokedex"])
        else:
            print("Back to Pokedex Menu.")


########################
# 8) Sub-menu & Main menu
########################

def existing_pokedex():
    name = input("Owner name: ")
    owner = find_owner_bst(ownerRoot, name)
    if owner is None:
        print(f"owner '{name}' not found.")
        return

    choice = 0
    while choice != 5:
        choice = read_int_safe(f'''
-- {owner["name"]}'s Pokedex Menu --
1. Add Pokemon
2. Display Pokedex
3. Release Pokemon
4. Evolve Pokemon
5. Back to Main
Your choice: ''')
        if choice == 1:
            add_pokemon_to_owner(owner)
        elif choice == 2:
            display_filter_sub_menu(owner)
        elif choice == 3:
            release_pokemon_by_name(owner)
        elif choice == 4:
            evolve_pokemon_by_name(owner)
        else:
            print("back to main menu.")


def main_menu():
    choice = 0
    while choice != 6:
        choice = read_int_safe("""
=== Main Menu ===
1. New Pokedex
2. Existing Pokedex
3. Delete a Pokedex
4. Sort owners
5. Print all
6. Exit
Your choice: """)
        if choice == 1:
            open_pokedex_menu()
        elif choice == 2:
            existing_pokedex()
        elif choice == 3:
            delete_pokedex()
        elif choice == 4:
            sort_owners_by_num_pokemon()
        elif choice == 5:
            print_all_owners()
        else:
            print("Goodbye!")


def main():
    main_menu()


if __name__ == "__main__":
    main()
