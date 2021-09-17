
# import required packages

from Tracker import Tracker
import datetime
import pickle
import os
import time
from tabulate import tabulate
from sys import exit

class Session():

    """
    User interface for the Impulse Tracker
    """
    # hold all the tracker names that are created
    tracker_names = set()

    def __init__(self):
        self.cur_tracker = None
        self.cur_username = ''

    def display_main(self):
        """
        Displays the main menu of creating a new tracker, loading previous tracker, or quit
        """

        while True:
            print("""
                     __             __   ___     __   __   ___       __          __
            |  |\/| |__) |  | |    /__` |__     /__` |__) |__  |\ | |  \ | |\ | / _`
            |  |  | |    \__/ |___ .__/ |___    .__/ |    |___ | \| |__/ | | \| \__>

            ___  __        __        ___  __
             |  |__)  /\  /  ` |__/ |__  |__)
             |  |  \ /~~\ \__, |  \ |___ |  \
            """)

            print("""
            Welcome to Impulse Spending Tracker, where you can create a wishlist and curb
            impulse spending using a point system. The longer items stay un-redeemed on
            your wishlist, the more points you accumulate. Accumulate enough points and you
            can redeem items from your wishlist.

            What would you like to do?

            1) Create a new tracker
            2) Load a saved tracker
            3) Quit
            """)

            resp = input("Enter your response here: ")

            if resp == '1':
                self.create_tracker()
                break
            elif resp == '2':
                self.load_tracker()
                break
            elif resp == '3':
                self.quit()
            else:
                print("Invalid response. Please try again.")

    def display_post_create(self):
        """
        Displays the menu after you initialize a new tracker with create_tracker
        """

        print("""
        To get started...

        QUICK START MENU

        1) Add an item to the wishlist
        2) Go to main menu
        3) Save and quit

        """)

        while True:

            resp = input("What would you like to do? ")

            if resp == '1':
                self.add_item_run()
                self.display_functions()
            elif resp == '2':
                self.display_functions()
            elif resp == '3':
                # have it save by default
                self.save_tracker()
                self.quit()
                break



    def display_functions(self):
        """
        Displays the functional menu after you either create a new tracker and
        add at least one item or if you load a saved tracker
        """

        while True:
            print("""
            Select one of the following options:

            1) Add an item to the wishlist
            2) Update an item in the wishlist
            3) Delete an item from the wishlist
            4) Redeem an item from the wishlist
            5) Search for a wishlist item by name
            6) View wishlist
            7) View tracker info
            8) Save tracker
            9) Save tracker and quit
            """)
            resp = input("What would you like to do? ")

            if resp == "1":
                self.add_item_run()
            elif resp == "2":
                self.update_item()
            elif resp == "3":
                self.del_item()
            elif resp == "4":
                self.redeem_item()
            elif resp == "5":
                self.search_item()
            elif resp == "6":
                self.view_wishlist()
            elif resp == "7":
                self.tracker_info()
            elif resp == "8":
                self.save_tracker()
            elif resp == "9":
                self.quit()
            else:
                print("Invalid response. Please try again.")

    def run(self):
        # upon running, if there isn't a data folder created, make one
        # load the tracker dict so later we can check to see if there's a conflict if
        # someone tries to use the same username

        if not os.path.isdir("data"):
            os.makedirs("data")

        # then check if there's a pickle file for the tracker names
        # if so, load the most recent one and assign to tracker_names

        pickles = ["data/" + f for f in os.listdir("data") if f[0:13] == "tracker_names"]

        if len(pickles) > 0:

            newest = max(pickles , key = os.path.getctime)

            with open(newest, "rb") as f:
                self.tracker_names = pickle.load(f)

        self.display_main()


    def create_tracker(self):
        """
        Creates a new tracker object if username/tracker doesn't already exist
        """
        print("Let's make a new Tracker!")

        while True:

            username = input("Enter a username to associate with the Tracker: ")

            if username in self.tracker_names:
                print("""
                Username already exists in system.

                1) Return to main menu to load tracker associated with that username
                2) Select another username
                """)

                resp = input("Enter a response: ")

                if resp == "1":
                    self.display_main()
                elif resp == "2":
                    continue

            else:
                break

        # initialize Tracker
        tracker = Tracker(username)

        # add tracker to menu's tracker names
        self.tracker_names.add(username)
        # set this new tracker as the current tracker
        self.cur_tracker = tracker
        self.cur_username = username
        print("Tracker successfully created!")
        self.display_post_create()


    def load_tracker(self):
        """
        Checks if inputted username is in tracker_names, which is loaded and assigned
        based on whether a pickle file for the tracker name exists. If does exist,
        then load the most recent tracker pickle file associated with that name inside
        the data directory
        """
        while True:

            # if there are saved trackers to load
            if len(self.tracker_names) > 0:

                username = input("Enter the username of the tracker you want to load: ")

                if username not in self.tracker_names:
                    print("""
                    Sorry, there is no saved tracker for that username.

                    1) Re-enter the username
                    2) Create a new tracker
                    """)

                    resp = input("What would you like to do? ")

                    if resp == '1':
                        continue
                    elif resp == '2':
                        self.create_tracker()
                        break
                    else:
                        print("Invalid response. Try again.")
                else:
                    break
            else:
                print("There are no saved trackers in the system. Please create a new Tracker.")
                self.create_tracker()
                break


        # find the latest file of the corresponding username
        # set current username to username
        self.cur_username = username

        # make a list of all the files that correspond to username
        pickles = ["data/" + f for f in os.listdir("data") if f[0:len(username)] == username]

        # if there's at least one file, find the most recent one
        # and load it as the current tracker

        if len(pickles) > 0:

            newest = max(pickles , key = os.path.getctime)

            with open(newest, "rb") as f:
                self.cur_tracker = pickle.load(f)

        # calculate the latest points and cost since last save
        self.cur_tracker.calc()
        print("Tracker successfully loaded!")

        self.display_functions()

    def add_item_date(self):

        """
        Asks user if they want to override date timestamp
        Checks if the date inputs are correct
        Returns formatted date object for the Tracker.add_item()
        """

        while True:

            print("""
            When an item is added or redeemed with the wishlist, it is timestamped with today's date
            by default. You have the option to override this and input a custom date.
            For example, if you were tracking items elsewhere. Note: Item dates are used
            to calculate point accummulation so altering them will affect your points.
                  """)
            resp = input("Do you want to override the item date? y/n: ")

            if resp[0].lower() == "y":

                while True:
                    str_date = input("Enter a custom item date in the following format (MM/DD/YYYY): ")

                    try:

                        if datetime.datetime.strptime(str_date, "%m/%d/%Y").date() > datetime.date(1970, 1, 1):

                            return "y", datetime.datetime.strptime(str_date, "%m/%d/%Y").date()

                        else:
                            print("Is this correct? Dates should be at least after 1/1/1970! Try again.")

                    except:
                        print("Invalid date. Please use the MM/DD/YYYY format. Try again.")


            elif resp[0].lower() == "n":

                return "n", None

            else:
                print("Invalid response. Please try again.")

    def add_item_price(self):

        """
        Asks user to enter price of the item
        Performs error checking
        Returns the object
        """

        while True:

            resp = input("Enter the item price $:")

            try:
                # no zero dollars or negative numbers
                if float(resp) <= 0:
                    print("Please enter a price that is greater than 0 dollars.")
                    continue
                else:
                    return float(resp)

            except:
                # catches if they put non-numerical values
                print("Invalid monetary value. Please try again.")


    def add_item_cat(self):

        """
        Asks user to select a category for the item
        Performs error checking
        Returns the object
        """

        categories = {"1": "Beauty/Skincare", "2":"Books", "3":"Clothing/Accessories",
                      "4": "Electronics", "5":"Food", "6":"Jewelry", "7":"Other"}

        while True:

            print("""
            Item Categories:

            1) Beauty/Skincare
            2) Books
            3) Clothing/Accessories
            4) Electronics
            5) Food
            6) Jewelry
            7) Other

            """)

            resp = input("Select an item category by the number: ")

            # if valid response then return it
            if resp in [str(i) for i in range(1, 8)]:

                return categories[resp]
            else:
                print("Invalid response. Please try again.")

    def add_item_value(self):

        """
        Asks user to enter a point value for the item
        Performs error checking (no negatives, nothing too high)
        Returns object
        """

        while True:

            print('''
            Enter a point value for the item. This is what it will
            "cost" to redeem the item once you accumulate enough points.
            Point values can range from 100 to 2000 depending on your own
            personal factors such as price, necessity, timing, etc.
            ''')

            resp = input("Item point value: ")

            if int(resp) >= 100 and int(resp) <= 2000:
                return int(resp)
            else:
                print("Invalid response. Please try again.")

    def add_item_run(self):
        """
        Adds an item to the wishlist utilizing Tracker function after
        running the functions to error check inputs to the Tracker.add_item() function
        """

        while True:

            item = input("To get started with adding an item to the wishlist, enter the item name: ")

            if self.cur_tracker.is_in_wishlist(item):
                print("""
                This item already exists in the wishlist.
                1) Enter a new item
                2) Update existing item
                """)
                resp = input("What would you like to do? ")

                if resp == "1":
                    continue
                elif resp == "2":
                    self.update_item()
                    self.display_functions()
                else:
                    continue
            else:
                break

        try:
            category = self.add_item_cat()
            price = self.add_item_price()
            value = self.add_item_value()
            override, date = self.add_item_date()

            self.cur_tracker.add_item(item = item, price = price, category = category,
                                      value = value, override_dates = override, date = date)
        except:
            print("Unable to add item. Returning to Main Menu.")

        finally:
            self.display_functions()



    def update_item(self):
        """
        Asks user what item to updated and what part they want to update
        """

        while True:

            resp = input("What is the name of the item you would like to update? ")

            if self.cur_tracker.is_in_wishlist(resp) and self.cur_tracker.is_deleted(resp) == False and self.cur_tracker.is_redeemed(resp) == False:

                print("""
                What would you like to update for this item?

                1) Category
                2) Price
                3) Point value
                """)

                options = {"1":["category", self.add_item_cat],
                           "2":["price", self.add_item_price],
                           "3":["value", self.add_item_value]}

                resp2 = input("Select one of the options above by typing in the number: ")

                if resp2 in options.keys():

                    # run the corresponding function which has error checking
                    resp3 = options[resp2][1]()

                self.cur_tracker.update_item(resp, options[resp2][0], resp3)

                if resp2 == "2" or resp2 == "3":
                    self.cur_tracker.calc()
                break

            else:
                print("That item is not in the wishlist. Please try again.")


    def del_item(self):

        """
        Asks user what item they want to delete, checks if it's in wishlist,
        deletes if in wishlist.

        Note: this is not a hard delete. It marks the delete_ind as yes
        """

        while True:

            resp = input("What item do you want to delete from the wishlist? Please type the exact name: ")

            if self.cur_tracker.is_in_wishlist(resp) and self.cur_tracker.is_deleted(resp) == False and self.cur_tracker.is_redeemed(resp) == False:

                resp2 = input("Please type Y to confirm that you want to delete this item: ")

                if resp2.lower() == 'y':

                    self.cur_tracker.del_item(resp)
                    time.sleep(2)

                else:
                    print("Item deletion canceled. \n")

                break
                #else:
                    #continue
            else:
                print("Item not in wishlist. Please try again.")


    def redeem_item(self):

        """
        Runs the redeem function from tracker. Asks user what item to mark as redeemed.
        If item is in wishlist, then redeem it. Subtract the points and cost from the
        tracker totals.

        """

        while True:

            resp = input("What item do you want to redeem from the wishlist? Please type the exact name: ")

            if self.cur_tracker.is_in_wishlist(resp) and self.cur_tracker.is_deleted(resp) == False and self.cur_tracker.is_redeemed(resp) == False:

                resp2 = input("Please type Y to confirm that you want to redeem this item: ")

                if resp2.lower() == 'y':

                    override, date = self.add_item_date()
                    self.cur_tracker.redeem_item(resp, override, date)

                else:
                    print("Item redemption canceled. \n")

                break
            else:
                print("Item not in wishlist. Please try again.")

    def search_item(self):

        while True:

            resp = input("What is the name of the item you want to search for? ")

            if self.cur_tracker.is_in_wishlist(resp):

                temp = self.cur_tracker.search_wishlist(resp)
                # print the item info

                print("""Item Name: {} \n
                       Category: {} \n
                       Value: {} \n
                       Price: {} \n
                       Date Entered: {} \n
                       Redeemed: {} \n""".format(resp, temp["category"], temp["value"],
                                              temp["price"], temp["date"], temp["redeemed"]))
                break
            else:
                print("Item not in wishlist. Please try again using the exact name of the item.")


    def view_wishlist(self):
        """
        Utilizes the view wishlist function the tracker to present
        either a wishlist of only active items or the full wishlist regardless
        of deletion or redemption
        """

        while True:

            resp = input("Do you want to see only active items? Please enter y/n: ")

            if resp.lower()[0] == "y":
                print(self.cur_tracker.view_wishlist())
                break
            elif resp.lower()[0] == "n":
                print(self.cur_tracker.view_wishlist(only_active = 'n'))
                break
            else:
                print("Invalid response. Please try again.")


    def tracker_info(self, debug = "n"):

        """ Displays information about the tracker """

        self.cur_tracker.calc()

        while True:

            resp = input("View tracker info in debugging mode? y/n: ")

            print("""
                {}'s current points are: {}
                {}'s wishlist current point totals up to: {}
                {}'s wishlist current cost totals up to: {:.2f}
                """.format(self.cur_username, self.cur_tracker._Tracker__points,
                self.cur_username, self.cur_tracker._Tracker__wl_points,
                self.cur_username, self.cur_tracker._Tracker__cost))

            if resp == "y":
                self.cur_tracker.tracker_info(debug = "y")
                break
            elif resp == "n":
                self.cur_tracker.tracker_info(debug = "n")
                break


    def save_tracker(self):
        """
        Saves the tracker names into a pickle file inside the data directory
        Saves the current tracker into a pickle file inside the data directory
        """

        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        names_file = "data/tracker_names_" + now + ".pickle"
        tracker_file = "data/" + self.cur_username + "_" + now + ".pickle"

        with open(names_file, "wb") as f:
            pickle.dump(self.tracker_names, f)

        with open(tracker_file, "wb") as f:
            pickle.dump(self.cur_tracker, f)

        print("Impulse Spending Tracker successfully saved.")


    def quit(self):

        """Function that saves before exiting if a user session is active"""

        if self.cur_username != '':
            self.save_tracker()

        print("The program will now exit. Thank you for using the Impulse Tracker!")
        exit(0)
