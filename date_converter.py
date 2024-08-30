from datetime import datetime


class DateConverter:
    def __init__(self):
        self.current_date = datetime.today()

    def standardize_month_name(
            self,
            date_text: str,
            split_separator: str
    ) -> str:
        month_dict = {
            "Jan": "January",
            "Feb": "February",
            "Mar": "March",
            "Apr": "April",
            "May": "May",
            "Jun": "June",
            "Jul": "July",
            "Aug": "August",
            "Sep": "September",
            "Oct": "October",
            "Nov": "November",
            "Dec": "December"
        }

        for month_key in month_dict.keys():
            date_arr = date_text.split(split_separator)

            if date_arr[0].strip().lower().startswith(month_key.lower()):
                date_arr[0] = month_dict[month_key]
                return " ".join(date_arr)

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

        date_text = self.standardize_month_name(date_text, " ")

        for format_check in possible_data_formating:
            try:
                date = datetime.strptime(date_text, format_check).date()
                break
            except ValueError:
                if "," not in date_text:
                    date_text = date_text + ", " + str(self.current_date.year)
                try:
                    date = datetime.strptime(date_text, format_check).date()
                    break
                except ValueError:
                    continue

        # Format the date and return the result
        formatted_date = date.strftime(format)
        return formatted_date.strip()


# Example usage
# converter = DateConverter()
# print(converter.convert_text_to_formatted_date(
#     "Feb. 18, 2024"))  # Output: "2024-02-18"
