# import reqire packages

import datetime
import time
from tabulate import tabulate


class Tracker():

    """
    Tracker object to hold the wishlist items and track point values
    """

    def __init__(self, username):

        # creates the wishlist dict
        self.__wishlist = dict()
        # captures when the tracker was started
        self.__start_date = datetime.date.today()
        # captures current date for state purposes
        self.__cur_date = datetime.date.today()
        # inital points accumulated
        self.__points = 0
        # initial points value of wishlist
        self.__wl_points = 0
        # initial wishlist cost
        self.__cost = 0
        # get a username
        self.__username = username

    def tracker_info(self, debug = "n"):

        print("Start Date of Tracker:", self.__start_date)
        print("Username is:", self.__username)

        if debug == "y":
            print("Wishlist contains:", self.__wishlist)


    def is_in_wishlist(self, item):

        """
        Function to check whether something is in the wishlist
        """

        return item in self.__wishlist.keys()

    def print_wishlist_old(self, csv = "no"):

        """Function to put the wishlist dict into a df
        for easy viewing with an option to create csv"""

        # have not built in csv functionality
        df = pd.DataFrame(self.__wishlist)
        df_T = df.T

        return df_T[(df_T["redeemed"][0] == "n") & (df_T["del_ind"][0] == "n")]

    def print_wishlist(self, only_active = "y"):

        """
        Function that uses tabulate to create a formatted table for user that
        either contains only active items or all items regardless of deletion
        or redemption
        """
        #QUESTION: add sorting to these tables? Like by date?

        formatted_wl = []


        if only_active == "y":

            for k, v in self.__wishlist.items():
                if v["redeemed"][0] == "n" and v["del_ind"][0] == "n":
                    formatted_wl.append((k, v["date"].strftime("%m/%d/%Y"), v["category"],
                                         float(v["price"]), v["value"]))

            headers = ["Item", "Date", "Category", "Price", "Value"]

        elif only_active == "n":

            for k, v in self.__wishlist.items():
                formatted_wl.append((k, v["date"].strftime("%m/%d/%Y"), v["category"],
                                     float(v["price"]), v["value"], v["del_ind"], v["redeemed"]))

            headers = ["Item", "Date", "Category", "Price", "Value", "Deleted?", "Redeemed?"]

        return tabulate(formatted_wl, headers = headers)

    # getter
    @property
    def points(self):
        return self.__points

    @property
    def wishlist(self):
        return self.__wishlist

    @property
    def points(self):
        return self.__points

    @property
    def cost(self):
        return self.__cost

    @property
    def wl_points(self):
        return self.__wl_points

    #@points.setter
    #def set_points(self, points):

        #"""After calculating the points for the day, set that as the points """

        #self.points = points

    class IsDel(Exception):

        """ Raised when item has been deleted to prevent performing actions on deleted items """

        def __init__(self, item, message = "Unable to perform action. Item has been deleted."):
            self.item = item
            self.message = message
            super().__init__(self.message)

        def __str__(self):

            return "{} --> {}".format(self.item, self.message)


    class IsRedeemed(Exception):

        """ Raised when item has been redeemed to prevent peforming actions on redeemed items"""

        def __init__(self, item, message = "Unable to perform action. Item has been redeemed."):
            self.item = item
            self.message = message
            super().__init__(self.message)

        def __str__(self):

            return "{} --> {}".format(self.item, self.message)

    # QUESTION: should I have this class if I already have the function check whether it's in there...?
    class NotInWishlist(Exception):

        """ Raised when item is not in wishlist """

        def __init__(self, item, message = "Unable to perform action. Item is not in wishlist."):
            self.item = item
            self.message = message
            super().__init__(self.message)

        def __str__(self):

            return "{} --> {}".format(self.item, self.message)

    class NotEnough(Exception):

        """ Raised when item redemption exceeds point total"""

        def __init__(self, item, message = "Unable to perform action. Item value exceeds accumulated point total."):
            self.item = item
            self.message = message
            super().__init__(self.message)

        def __str__(self):

            return "{} --> {}".format(self.item, self.message)

    def add_item(self, item, price, category, value,
                          override_dates = "n", date = datetime.date(1900, 1, 1)):

        """
        Function to add wishlist item if it doesn't already exist in the dict
        """

        if self.is_in_wishlist(item) is False:

            if override_dates == "n":
                self.__wishlist[item] = {"price":price, "category":category,
                                         "value":value, "date":datetime.date.today(),
                                         "redeemed_dt":datetime.date(1900, 1, 1), "redeemed":"n",
                                        "del_ind": "n"}
                print("Item added to wishlist")
            elif override_dates == "y":
                # allows overriding logging today's date in case we're backtracking
                self.__wishlist[item] = {"price":price, "category":category,
                                         "value":value, "date":date,
                                         "redeemed_dt":datetime.date(1900, 1, 1), "redeemed":"n",
                                        "del_ind": "n"}
                print("Item added to wishlist")

        else:
            # revisit to create a way to bypass this upon user confirmation
            print("Item is already in wishlist")



    def del_item(self, item):

        """
        Function to mark an item as deleted. We don't do a hard delete in case we need to backtrack.
        """
        # TO DO: prevent delete if it has already been deleted or redeemed using errors
        try:

            if self.is_in_wishlist(item) is False:
                raise self.NotInWishlist(item)

            if self.__wishlist[item]["del_ind"] == "y":
                raise self.IsDel(item)

            if self.__wishlist[item]["redeemed"] == "y":
                raise self.IsRedeemed(item)

            self.__wishlist[item]["del_ind"] = "y"
            print("Item deleted from wishlist")

        except self.NotInWishlist:
            print("Item not in wishlist.")

        except self.IsDel:
            print("Unable to perform action. Item already has a status of deleted.")

        except self.IsRedeemed:
            print("Unable to perform action. Cannot delete a redeemed item.")


    def update_item(self, item, to_update, update):

        """
        Function to update an item on the wishlist based on the key defined
        """

        try:

            if self.is_in_wishlist(item) is False:
                raise self.NotInWishlist(item)

            if self.__wishlist[item]["del_ind"] == "y":
                raise self.IsDel(item)

            if self.__wishlist[item]["redeemed"] == "y":
                raise self.IsRedeemed(item)


            self.__wishlist[item][to_update] = update
            print("Item has been updated")

        except self.NotInWishlist:
            print("Item not in wishlist.")

        except self.IsDel:
            print("Unable to perform action. Item already has a status of deleted.")

        except self.IsRedeemed:
            print("Unable to perform action. Cannot delete a redeemed item.")

    def calc(self):

        """
        Function to calculate the total points and cost based on the number of non-redeemed items current in the list
        """

        points = 0
        wl_points = 0
        cost = 0

        for item in self.__wishlist.keys():
            temp = self.__wishlist[item]

            # for items that are active and haven't been redeemed or deleted
            if temp["date"] <= datetime.date.today() and temp["redeemed"][0] == "n" and temp["del_ind"][0] == "n":

                points += abs(datetime.date.today() - temp["date"]).days
                wl_points += temp["value"]
                cost += temp["price"]

            # for items that have been redeemed, add back the value up until redeemed
            # then subtracted the value redeemed
            if temp["redeemed_dt"] > datetime.date(1900, 1, 1) and temp["redeemed_dt"] <= datetime.date.today() and temp["del_ind"][0] == "n":

                points += abs(temp["redeemed_dt"] - temp["date"]).days
                points -= temp["value"]

        # set points attribute
        self.__points = points
        self.__cost = cost
        self.__wl_points = wl_points

    def redeem_item(self, item):

        """
        Function to mark an item as redeemed in the wishlist if its point value is not larger
        than the points total, item hasn't been deleted before, item hasn't been redeemed before

        Before redeeming:
        - check that item is in wishlist --> otherwise, keyerror or not in wishlist
        - check that item hasn't been deleted --> otherwise, not in wishlist
        - check that item value is less than or equal to current points total --> otherwise, print error and don't redeem
        """

        try:

            if self.is_in_wishlist(item) is False:
                raise self.NotInWishlist(item)

            if self.__wishlist[item]["del_ind"] == "y":
                raise self.IsDel(item)

            if self.__wishlist[item]["redeemed"] == "y":
                raise self.IsRedeemed(item)

            if self.__wishlist[item]["value"] > self.__points:
                raise self.NotEnough(item)

            # QUESTION: do I need to the private reference here if I set up the getter??
            self.__wishlist[item]["redeemed"] = "y"
            self.__wishlist[item]["redeemed_dt"] = datetime.date.today()
            self.__points -= self.__wishlist[item]["value"]
            self.__cost -= self.__wishlist[item]["price"]

            print("Item successfully redeemed!")

        # QUESTION: do I need all the details in the error classes if I'm just going to print anyway?
        except self.NotInWishlist:
            print("Item not in wishlist.")

        except self.IsDel:
            print("Unable to perform action. Item has a status of deleted.")

        except self.IsRedeemed:
            print("Unable to perform action. Item has already been redeemed.")

        except self.NotEnough:
            print("Unable to perform action. Item value exceeds the accumulated point total!")


    def search_wishlist(self, item):

        # may have to be broken down into other methods depending on search?

        """
        Function to return item dict if item exists
        """

        if self.is_in_wishlist(item):

            return self.__wishlist[item]

        else:
            return False
