CHECKLIST_RULES = {

    "budget": [
        "Create project budget"
    ],

    "map": [
        "Prepare project maps"
    ],

    "gis": [
        "Prepare GIS data"
    ],

    "letter of support": [
        "Request support letters"
    ],

    "letters of support": [
        "Request support letters"
    ],

    "board approval": [
        "Obtain board approval"
    ],

    "nonprofit": [
        "Verify nonprofit eligibility"
    ],

    "501(c)(3)": [
        "Verify IRS nonprofit status"
    ],

    "match funding": [
        "Confirm matching funds"
    ],

    "partnership": [
        "Contact project partners"
    ],

    "monitoring": [
        "Develop monitoring plan"
    ]
}

DEFAULT_TASKS = [

    "Download grant guidelines",

    "Review eligibility",

    "Review deadline",

    "Prepare application materials",

    "Submit application"
]

def generate_checklist(text):

    text = (text or "").lower()

    tasks = list(DEFAULT_TASKS)

    for keyword, additions in CHECKLIST_RULES.items():

        if keyword.lower() in text:

            for item in additions:

                if item not in tasks:

                    tasks.append(item)

    return tasks
