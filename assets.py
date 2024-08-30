from robocorp import storage

# SELECTORS

locators = storage.get_json('nyt_locators')

list_location = locators["list_location"]
list_items_location = locators["list_items_location"]

reject_all_button_location = locators["reject_all_button_location"]
show_more_button_location = locators["show_more_button_location"]

date_text_class_name = locators["date_text_class_name"]
title_text_class_name = locators["title_text_class_name"]
description_text_class_name = locators["description_text_class_name"]
