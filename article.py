import re


class Article:
    def __init__(self,
                 date: str,
                 search_phrase: str,
                 title: str,
                 description: str,
                 picture_filename: str,
                 picture_link: str):
        self.date = date
        self.search_phrase = search_phrase
        self.title = title
        self.description = description
        self.picture_filename = picture_filename
        self.picture_link = picture_link

    @property
    def has_money(self) -> bool:
        """Checks if the title or description contains any amount of money.
        Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
        """
        # check if description or title has currency characters
        money_pattern = r"\$[\d,]+(\.\d+)?|\d+ dollars|\d+ USD"

        has_money = bool(
            re.search(
                money_pattern,
                self.title + " " + self.description)
        )

        return has_money

    @property
    def phrase_count(self) -> int:
        """Checks if the title or description contains the searched phrase

        Args:
            phrase (str): searched phrase
        """
        sentence = self.title + " " + self.description

        has_phrase = (
            self.search_phrase.lower() in (sentence.lower())
        )

        if has_phrase:
            return (
                sentence.lower().count(self.search_phrase.lower())
            )

        else:
            return 0
