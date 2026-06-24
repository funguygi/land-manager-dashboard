import re

def extract_funding_amount(text):

    if not text:
        return 0

    text = str(text)

    text = text.replace(",", "")

    million_match = re.search(
        r"\$?(\d+(\.\d+)?)\s*million",
        text,
        re.IGNORECASE
    )

    if million_match:

        return int(
            float(
                million_match.group(1)
            ) * 1000000
        )

    amount_match = re.search(
        r"\$([0-9]+)",
        text
    )

    if amount_match:

        return int(
            amount_match.group(1)
        )

    return 0


def total_funding(grants):

    return sum(
        extract_funding_amount(
            g[7]
        )
        for g in grants
    )


def format_currency(amount):

    return "${:,.0f}".format(amount)
