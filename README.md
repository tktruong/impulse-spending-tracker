# Impulse Spending Tracker

### Purpose

I created this application after coming across an [article](https://thefinancialdiet.com/what-an-impulse-journal-is-how-it-keeps-me-from-splurging-download/) about how to curb impulse spending. The gist is when you have the urge to buy something non-essential, you first have to jot it down in a journal and assign it a point value. You can accumulate points each day for the items that you don't purchase. When you would like to buy something, you use the accumulated points to "redeem" it. The idea is to be more mindful about your purchases and the odds are, after a week or so, you might discover that you don't really want that item anymore. The author recommends keeping an impulse journal, but I decided to turn to code instead.

### Application

 The Impulse Spending Tracker is a Python command-line interface (CLI) program that guides you through creating a tracker, adding wishlist items, redeeming wishlist items, and more. The tracker automatically calculates point accumulation based on the items added and any actions performed on them (redemption or deletion). Users can save their trackers and reload them for future use. All data is saved locally via pickling.

### Project Extensions/Improvements

In its current state, the Impulse Spending Tracker is sufficient for personal use. Some enhancements that I'm working on are the ability to import a wishlist as a csv instead of item by item entry, exporting wishlist data as a csv, and making the search/item matching not as sensitive. It would also be great to incorporate better guidelines on how to assign point values to wishlist items. Ideally, with enough data, point values could be suggested to users via model prediction.
