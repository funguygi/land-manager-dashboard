from datetime import datetime

def deadline_flag(deadline):

    if not deadline:
        return ""

    formats = [
        "%m/%d/%Y",
        "%m/%d/%y",
        "%m/%d/%y %H:%M",
        "%m/%d/%Y %H:%M"
    ]

    for fmt in formats:

        try:

            dt = datetime.strptime(
                deadline.strip(),
                fmt
            )

            days = (
                dt - datetime.now()
            ).days

            if days <= 7:
                return "🔥"

            if days <= 30:
                return "⚠"

            return "✓"

        except:
            pass

    return ""