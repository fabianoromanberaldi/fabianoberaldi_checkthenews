from datetime import datetime


class DateConverter:
    def __init__(self):
        self.current_date = datetime.today()

    def is_date_format(
        self,
        date_str:
        str, format: str
    ) -> bool:
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False

    def convert_text_to_formatted_date(
        self,
        date_text: str,
        format="%Y-%m-%d"
    ) -> str:
        possible_data_formating = (
           "%b. %d, %Y",
           "%B %d, %Y",
           "%b. %d"
        )

        for format_check in possible_data_formating:
            try:
                date = datetime.strptime(date_text, format_check).date()
                break
            except ValueError:
                date_text = date_text + ", " + str(self.current_date.year)
                try:
                    date = datetime.strptime(date_text, format_check).date()
                    break
                except ValueError:
                    continue

        # try:
        #     # Try to convert the text to a date object using
        #     # the format "%B %d, %Y"
        #     if ',' in date_text:
        #         if '.' in date_text:
        #             date = datetime.strptime(date_text, "%b. %d, %Y").date()
        #         else:
        #             date = datetime.strptime(date_text, "%B %d, %Y").date()
        #     else:
        #         if '.' in date_text:
        #             date = datetime.strptime(date_text, "%b. %d, %Y").date()
        #         else:
        #             date = datetime.strptime(date_text, "%B %d, %Y").date()
        # except ValueError:
        #     # If the format is not "%B %d, %Y",
        #     # add the current year and try again
        #     date_text = date_text + ", " + str(self.current_date.year)
        #     try:
        #         date = datetime.strptime(date_text, "%B %d, %Y").date()
        #     except ValueError:  # noqa: E722
        #         date = datetime.strptime(date_text, "%b. %d, %Y")

        # Format the date and return the result
        formatted_date = date.strftime(format)
        return formatted_date.strip()


# Example usage
# converter = DateConverter()
# print(converter.convert_text_to_formatted_date(
#     "Feb. 18, 2024"))  # Output: "2024-02-18"
