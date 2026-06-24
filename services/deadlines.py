from datetime import datetime

def days_until_deadline(deadline):

    if not deadline:
        return ""

    formats = [
        "%m/%d/%y",
        "%m/%d/%Y",
        "%m/%d/%y %H:%M",
        "%m/%d/%Y %H:%M"
    ]

    for fmt in formats:

        try:

            date_part = deadline.split()[0]

            due = datetime.strptime(
                date_part,
                fmt
            )

            days = (
                due - datetime.now()
            ).days

            if days < 0:
                return "OVERDUE"

            return f"{days} days"

        except:
            pass

    return ""

def deadline_sort_key(deadline):

    if not deadline:
        return datetime.max

    formats = [
        "%m/%d/%y",
        "%m/%d/%Y",
        "%m/%d/%y %H:%M",
        "%m/%d/%Y %H:%M"
    ]

    for fmt in formats:

        try:

            date_part = deadline.split()[0]

            return datetime.strptime(
                date_part,
                fmt
            )

        except:
            pass

    return datetime.max

def deadline_sort_value(deadline):

    return deadline_sort_key(deadline)

def deadline_is_future(deadline):

    if not deadline:
        return False

    return deadline_sort_key(
        deadline
    ) > datetime.now()
