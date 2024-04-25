# from robocorp import storage

# # SELECTORS

# locators = storage.get_json('nwt_locators')

# list_location = locators["list_location"]
# list_items_location = locators["list_items_location"]

# reject_all_button_location = locators["reject_all_button_location"]
# show_more_button_location = locators["show_more_button_location"]

# date_text_class_name = locators["date_text_class_name"]
# title_text_class_name = locators["title_text_class_name"]
# description_text_class_name = locators["description_text_class_name"]

list_location = "//ol[@data-testid='search-results']"
list_items_location = "//li[@data-testid='search-bodega-result']"

reject_all_button_location = "//button[@data-testid='Reject all-btn']"
show_more_button_location = (
    "//button[@data-testid='search-show-more-button']"
)

date_text_class_name = "css-17ubb9w"
title_text_class_name = "css-2fgx4k"
description_text_class_name = "css-16nhkrn"
