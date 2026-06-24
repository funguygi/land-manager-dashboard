from datetime import datetime

def deadline_alert(deadline):

    if not deadline:
        return "⚪"

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

            if days <= 7:
                return "🔴"

            if days <= 14:
                return "🟠"

            if days <= 30:
                return "🟡"

            return "🟢"

        except:
            pass

    return "⚪"