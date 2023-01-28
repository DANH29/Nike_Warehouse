# Nike warehouse stock program

# program has a menu to ask user what operation they would like to use, available operations are:

# Add shoe data
# View all shoe data
# Find the lowest stocked product with option to restock
# Search for a product using shoe code
# Show total value of stock for each product
# Find the highest stocked product and list on sale
# Exit menu

# all shoe stock information is imported from inventory.txt and stored using the class "Shoe"
# program using tabulate to display certain data in a user-friendly manner

from tabulate import tabulate

# class Shoe used to define information imported from inventory.txt
# has 5 attributes: country, code, product, cost and quantity
# contains 3 methods:
# return cost of a shoe
# return quantity of stock of a shoe
# return shoe object as a string

class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost()

    def get_quantity(self):
        return int(self.quantity)

    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


# empty list to store imported data from inventory.txt
shoe_list = []

# function to import data from inventory.txt
# opens inventory.txt then reads file and splits into each line
# loop through all lines in inventory.txt except the first (contains headers)
# splits each line via commas into the 5 attributes then creates a Shoe object using said attributes
# appends Shoe object to shoe_list
# handles IndexErrors

def read_shoes_data():
    inventory_txt = open("inventory.txt", "r")
    inventory = inventory_txt.read().splitlines()

    for line in inventory[1:]:
        try:
            line = line.split(",")
            shoe_object = Shoe(line[0], line[1], line[2], line[3], line[4])
            shoe_list.append(shoe_object)
        except IndexError:
            break
    inventory_txt.close()


# function for user to add new Shoe to shoe_list
# prompts user for 5 attributes of shoe
# uses whiles loops and if statements to validate user input
# uses ValueError handling for cost and quantity
# creates new Shoe object using 5 attributes and appends to shoe_list
# writes new Shoe object to inventory_txt

def capture_shoes():

    while True:
        new_country = input("\nEnter product country of origin: ")
        if new_country == "":
            print("Product country of origin cannot be empty")
        else:
            break

    while True:
        new_code = input("\nEnter product code: ")
        if new_code == "":
            print("Product code cannot be empty")
        else:
            for line in shoe_list:
                if line.code == new_code:
                    print("Product code already exists in inventory.txt")
                    break
            else:
                break

    while True:
        new_product = input("\nEnter product name: ")
        if new_product == "":
            print("Product code cannot be empty")
        else:
            for line in shoe_list:
                if line.product == new_product:
                    print("Product already exists in inventory.txt")
                    break
            else:
                break

    while True:
        try:
            new_cost = int(input("\nEnter product price: "))
            break
        except ValueError:
            print("#ValueError# Please enter product price")

    while True:
        try:
            new_quantity = int(input("\nEnter product quantity: "))
            break
        except ValueError:
            print("#ValueError# Please enter product price")

    new_shoe_object = Shoe(new_country,new_code,new_product,new_cost,new_quantity)
    shoe_list.append(new_shoe_object)

    inventory_txt = open("inventory.txt", "r+")
    inventory_txt.read()
    inventory_txt.write("\n" + new_shoe_object.__str__())
    inventory_txt.close()

    print("\nProduct successfully added!\n")


# function to print all Shoe data in shoe_list
# uses read_shoes_data to import inventory.txt
# starts with a nested list containing Shoe attributes (to be used as headers)
# loops through each Shoe in shoe_list, converts to string then splits into the 5 attributes
# append product to nested list
# print nested list as a table using tabulate

def view_all():
    view_shoe_list = [["Country","Code","Product","Cost","Quantity"]]
    for product in shoe_list:
        view_shoe_list.append(product.__str__().split(","))

    shoe_table = tabulate(view_shoe_list, headers="firstrow", tablefmt="fancy_grid")
    print(f"\n{shoe_table}\n")


# function to print lowest stocked Shoe with option to restock
# uses read_shoes_data to import inventory.txt

def re_stock():
    # variable to determine the lowest stocked product (defined mine as infinity)
    lowest_quantity = float("inf")

    # for each Shoe in shoe_list if the Shoes quantity is less than lowest_quantity
    # lowest_quantity becomes Shoes quantity
    # store all Shoe information as lowest_shoe
    for footwear in shoe_list:
        if footwear.get_quantity() < lowest_quantity:
            lowest_quantity = footwear.get_quantity()
            lowest_shoe = footwear

        # use tabulate to store attributes (headers) and lowest_shoe data as a table
        lowest_shoe_list = [["Country","Code","Product","Cost","Quantity"], lowest_shoe.__str__().split(",")]
        lowest_shoe_table = tabulate(lowest_shoe_list, tablefmt="fancy_grid")

    while True:
        # tell user the lowest stocked Shoe using table above
        # then prompt if they would like to restock or not, or to return to menu
        stock_up = input((f"\nThe shoe with the lowest quantity is:\n{lowest_shoe_table}\n\n"
                          "If you would like to re-stock 10 pairs enter \"yes\"\n"
                          "If you don't want to re-stock enter \"no\"\n"
                          "Enter here: "))

        # if users selects to restock
        if stock_up.lower() == "yes":

            # open inventory.txt and readlines
            inventory_txt = open("inventory.txt", "r")
            inventory = inventory_txt.readlines()

            # find index of lowest_shoe in inventory.txt
            lowest_shoe_index = inventory.index(lowest_shoe.__str__() + "\n")

            # + 10 to lowest_shoe quantity
            # this also changes quantity in shoe_list
            lowest_shoe.quantity = lowest_quantity + 10

            # change lowest_shoe data in inventory_txt to lowest_shoe
            inventory[lowest_shoe_index] = str(lowest_shoe) + "\n"
            inventory_txt.close()

            # open inventory.txt and write each line in inventory
            inventory_txt = open("inventory.txt", "w")
            for line in inventory:
                inventory_txt.write(line)
            inventory_txt.close()

            print("\nStock level successfully updated!\n")
            break

        # if users selects no to restock, return to menu
        elif stock_up.lower() == "no":
            print("\nShoe line has not been re-stocked.\n")
            break

        # if users inputs incorrect option
        else:
            print("\nIncorrect option entered.")


# function for user to input Shoe code and then print Shoe data from shoe_list

def search_shoe():
    # boolean variable to determine if Shoe has been found
    found_shoe = False

    # prompt user to enter Shoe code or return to menu
    while not found_shoe:
        shoe_code = input("\nEnter the shoe code you would like to search for, or enter \"m\" to return to menu: ")

        # if user chooses to return to menu
        if shoe_code.lower() == "m":
            break

        else:
            # loop through shoe_list, if user inputs == Shoe code from list
            for footwear in shoe_list:
                if shoe_code == footwear.code:

                    # store Shoe in a nested list along with attribute names (to be used as headers)
                    # store as a table using tabulate and print
                    found_shoe_list = [["Country","Code","Product","Cost","Quantity"], footwear.__str__().split(",")]
                    found_shoe_table = tabulate(found_shoe_list, tablefmt="fancy_grid")

                    print(f"\nYou searched for:\n{found_shoe_table}\n")

                    found_shoe = True
                    break

            # if user input Shoe code does not match any Shoe code in shoe_list
            if not found_shoe:
                print("\nThe shoe code you have entered does not exist.")


# function to print total value of each Shoe's stock
# uses read_shoes_data to import inventory.txt
# stores 5 Shoe attributes in a nested list
# loops through shoe_list and multiplies each Shoes quantity by Shoes cost
# appends Shoe: product, code, quantity and total value to nested list
# prints nested list as a table using tabulate

def value_per_item():
    value_list = [["Product", "Code", "Stock Quantity", "Total Stock Value"]]

    for footwear in shoe_list:
        total_value = int(footwear.quantity) * int(footwear.cost)
        value_list.append([footwear.product,footwear.code,footwear.quantity,total_value])

    value_table = tabulate(value_list, headers="firstrow", tablefmt="fancy_grid")
    print(f"\n{value_table}\n")


# function to find Shoe with the highest amount of stock
# uses read_shoes_data to import inventory.txt
# variable to store highest quantity (starting with 0)
# for each Shoe in shoe_list if the Shoes quantity is higher than highest_quantity
# highest_quantity becomes Shoes quantity and store Shoe data as highest_shoe
# uses a nested list to store Shoe sale information (Shoe cost has a 30% reduction)
# converted nested list to table using tabulate and then print

def highest_qty():
    highest_quantity = 0
    highest_shoe = ""

    for footwear in shoe_list:
        if footwear.get_quantity() > highest_quantity:
            highest_quantity = footwear.get_quantity()
            highest_shoe = footwear

    for_sale = [["The latest shoe to now go sale is..."],
                [highest_shoe.product],
                [f"With a 30% reduction from {highest_shoe.cost} to {(int(highest_shoe.cost) / 100) * 70}!"]]

    sale_table = tabulate(for_sale, tablefmt="fancy_grid")
    print(f"\n{sale_table}\n")


# call function to import inventory.txt data
read_shoes_data()

# user menu
# stores menu information and options in a nested list
# converts and prints nested list as a table using tabulate
# then request user input of which operation they would like to use
while True:
    menu = [["Add shoe data", "add"],
            ["View all shoe data", "view"],
            ["Find the lowest stocked product with option to restock", "low"],
            ["Search for a product using shoe code", "search"],
            ["Show total value of stock for each product", "value"],
            ["Find the highest stocked product and list on sale", "sale"],
            ["To exit menu", "exit"]]

    menu_table = tabulate(menu, tablefmt="fancy_grid")
    print("-------------------------------MENU--------------------------------")
    print(menu_table)

    menu_input = input("Enter the option you would like to choose:                ")

    # if/elif/else statements to determine user input and which functions are required

    if menu_input.lower() == "add":
        capture_shoes()

    elif menu_input.lower() == "view":
        view_all()

    elif menu_input.lower() == "low":
        re_stock()

    elif menu_input.lower() == "search":
        search_shoe()

    elif menu_input.lower() == "value":
        value_per_item()

    elif menu_input.lower() == "sale":
        highest_qty()

    elif menu_input.lower() == "exit":
        print("\nGoodbye!!!")
        exit()

    else:
        print("\nOops incorrect option entered!\n")
