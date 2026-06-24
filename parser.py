import re

def extract_grant_info(text):

    info = {
        "agency": "",
        "status": "",
        "open_date": "",
        "funding": ""
    }

    agency = re.search(r"Grantor:\s*(.*?)\s*Portal ID:", text)

    if agency:
        info["agency"] = agency.group(1).strip()

    status = re.search(r"Status:\s*(.*?)\s*Open Date:", text)

    if status:
        info["status"] = status.group(1).strip()

    open_date = re.search(r"Open Date:\s*(.*?)\s*Opportunity Type:", text)

    if open_date:
        info["open_date"] = open_date.group(1).strip()

    info["funding"] = extract_funding(text)

    return info

def extract_deadline(text):

    patterns = [

        r"Application deadline.*?(\d{1,2}/\d{1,2}/\d{2,4}\s+\d{1,2}:\d{2})",

        r"closes at.*?(\d{1,2}:\d{2}.*?\w+\s+\w+\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4})",

        r"due by.*?(\d{1,2}/\d{1,2}/\d{2,4})",

        r"applications due.*?(\d{1,2}/\d{1,2}/\d{2,4})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        if match:
            return match.group(1).strip()

    return ""

def extract_funding(text):

    if not text:
        return ""

    patterns = [

        r"Award Ceiling[:\s]*\$?([\d,]+(?:\.\d+)?)",

        r"Federal Award Ceiling[:\s]*\$?([\d,]+(?:\.\d+)?)",

        r"Maximum Award[:\s]*\$?([\d,]+(?:\.\d+)?)",

        r"Maximum Grant[:\s]*\$?([\d,]+(?:\.\d+)?)",

        r"Up to\s+\$?([\d,]+(?:\.\d+)?)",

        r"Total estimated available funding.*?\$([\d,]+(?:\.\d+)?)",

        r"Estimated Total Program Funding[:\s]*\$?([\d,]+(?:\.\d+)?)",

        r"Funding Amount[:\s]*\$?([\d,]+(?:\.\d+)?)",

        r"Total Funding[:\s]*\$?([\d,]+(?:\.\d+)?)",

        r"Award Amount[:\s]*\$?([\d,]+(?:\.\d+)?)",

        r"\$([\d,]{5,})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        if match:

            amount = match.group(1)

            try:

                value = float(
                    amount.replace(",", "")
                )

                return f"${value:,.0f}"

            except:

                return f"${amount}"

    million_match = re.search(
        r"([\d\.]+)\s*million",
        text,
        flags=re.IGNORECASE
    )

    if million_match:

        value = (
            float(million_match.group(1))
            * 1_000_000
        )

        return f"${value:,.0f}"

    billion_match = re.search(
        r"([\d\.]+)\s*billion",
        text,
        flags=re.IGNORECASE
    )

    if billion_match:

        value = (
            float(billion_match.group(1))
            * 1_000_000_000
        )

        return f"${value:,.0f}"

    return ""

def extract_categories(text):

    categories = []

    category_keywords = {

        "Wildlife": [
            "wildlife",
            "species",
            "habitat"
        ],

        "Restoration": [
            "restoration",
            "revegetation",
            "enhancement"
        ],

        "Watershed": [
            "watershed",
            "water quality",
            "riparian"
        ],

        "Land Protection": [
            "land acquisition",
            "conservation easement",
            "reserve"
        ],

        "Wildfire": [
            "wildfire",
            "fuel reduction",
            "prescribed fire"
        ],

        "Education": [
            "education",
            "training",
            "outreach"
        ]
    }

    text_lower = text.lower()

    for category, keywords in category_keywords.items():

        if any(keyword in text_lower for keyword in keywords):
            categories.append(category)

    return categories