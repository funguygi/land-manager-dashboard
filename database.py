import sqlite3

DB_NAME = "grants.db"

APPLICATION_STATUSES = [
    "New",
    "Reviewing",
    "Interested",
    "Preparing",
    "Submitted",
    "Awarded",
    "Declined"
]

def assign_priority(score):

    if score >= 80:
        return "High"

    if score >= 50:
        return "Medium"

    return "Low"

def funding_to_number(funding):

    if not funding:
        return 0

    funding = (
        funding.replace("$", "")
               .replace(",", "")
               .strip()
    )

    try:
        return float(funding)
    except:
        return 0

def opportunity_score(grant):

    score = grant[8]

    funding = funding_to_number(
        grant[7]
    )

    title = grant[1].lower()

    #
    # funding bonus
    #

    if funding >= 10000000:
        score += 25

    elif funding >= 5000000:
        score += 20

    elif funding >= 1000000:
        score += 15

    elif funding >= 250000:
        score += 10

    #
    # California bonus
    #

    california_terms = [
        "california",
        "san diego",
        "southern california"
    ]

    if any(
        term in title
        for term in california_terms
    ):
        score += 20

    #
    # geographic penalties
    #

    penalties = {

        "alaska": 50,
        "atlantic": 50,
        "chesapeake": 50,
        "appalachia": 50,
        "great lakes": 50,
        "new england": 40,
        "midwest": 30,
        "chicago": 30
    }

    for keyword, penalty in penalties.items():

        if keyword in title:
            score -= penalty

    return max(score, 0)

def initialize_database():

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS grants (

        url TEXT PRIMARY KEY,
        title TEXT,
        source TEXT,

        agency TEXT,
        status TEXT,
        open_date TEXT,
        deadline TEXT,
        funding TEXT,

        score INTEGER,
        priority TEXT,

        notes TEXT,
        application_status TEXT,

        archived INTEGER DEFAULT 0
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS grant_scores (

        grant_url TEXT,
        profile TEXT,
        score INTEGER,

        PRIMARY KEY (
            grant_url,
            profile
        )
    )
    """)

    # Migration for existing databases
    columns = [
        row[1]
        for row in conn.execute(
            "PRAGMA table_info(grants)"
        ).fetchall()
    ]

    if "archived" not in columns:
        conn.execute("""
        ALTER TABLE grants
        ADD COLUMN archived INTEGER DEFAULT 0
        """)

    conn.commit()
    conn.close()

    initialize_task_table()

def save_grant(grant):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    INSERT OR REPLACE INTO grants
    (
        url,
        title,
        source,
        agency,
        status,
        open_date,
        deadline,
        funding,
        score,
        priority,
        notes,
        application_status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        grant["url"],
        grant["title"],
        grant.get("source", "California Grants Portal"),
        grant.get("agency", ""),
        grant.get("status", ""),
        grant.get("open_date", ""),
        grant.get("deadline", ""),
        grant.get("funding", ""),
        grant["score"],
        grant.get("priority", assign_priority(grant["score"])),
        grant.get("notes", ""),
        grant.get("application_status", "New")
    ))

    conn.commit()
    conn.close()

def save_score(url, profile, score):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    INSERT OR REPLACE INTO grant_scores
    (
        grant_url,
        profile,
        score
    )
    VALUES (?, ?, ?)
    """, (
        url,
        profile,
        score
    ))

    conn.commit()
    conn.close()

def get_saved_grants():

    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute("""
    SELECT *
    FROM grants
    WHERE archived = 0
    ORDER BY score DESC
    """).fetchall()

    conn.close()

    return rows

def get_profile_scores(profile):

    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute("""
    SELECT
        g.url,
        g.title,
        g.source,
        g.agency,
        g.status,
        g.open_date,
        g.deadline,
        g.funding,
        s.score,
        g.priority,
        g.notes,
        g.application_status
    FROM grants g
    JOIN grant_scores s
        ON g.url = s.grant_url
    WHERE s.profile = ?
    ORDER BY s.score DESC
    """, (profile,)).fetchall()

    conn.close()

    return rows

def update_application_status(url, new_status):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    UPDATE grants
    SET application_status = ?
    WHERE url = ?
    """, (
        new_status,
        url
    ))

    conn.commit()
    conn.close()

def update_notes(url, notes):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    UPDATE grants
    SET notes = ?
    WHERE url = ?
    """, (
        notes,
        url
    ))

    conn.commit()
    conn.close()

def get_grant(url):

    conn = sqlite3.connect(DB_NAME)

    row = conn.execute("""
    SELECT *
    FROM grants
    WHERE url = ?
    """, (url,)).fetchone()

    conn.close()

    return row

def get_pipeline_grants():

    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute("""
    SELECT *
    FROM grants
    WHERE application_status IN (
        'Interested',
        'Preparing',
        'Submitted'
    )
    ORDER BY score DESC
    """).fetchall()

    conn.close()

    return rows

def get_active_grants():

    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute("""
    SELECT *
    FROM grants
    WHERE application_status IN (
        'Interested',
        'Preparing',
        'Submitted'
    )
    """).fetchall()

    conn.close()

    return rows

def initialize_task_table():

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS grant_tasks (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        grant_url TEXT,

        task_name TEXT,

        completed INTEGER DEFAULT 0,

        UNIQUE(grant_url, task_name)
    )
    """)

    conn.commit()
    conn.close()

def save_task(grant_url, task_name):

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO grant_tasks
    (
        grant_url,
        task_name,
        completed
    )
    VALUES (?, ?, 0)
    """, (
        grant_url,
        task_name
    ))

    conn.commit()
    conn.close()

def get_tasks(grant_url):

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
    SELECT
        id,
        task_name,
        completed
    FROM grant_tasks
    WHERE grant_url = ?
    ORDER BY id
    """, (grant_url,))

    rows = cur.fetchall()

    conn.close()

    return rows

def toggle_task(task_id):

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
    UPDATE grant_tasks

    SET completed =
        CASE
            WHEN completed = 1 THEN 0
            ELSE 1
        END

    WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()

def delete_declined_grants():

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    DELETE FROM grants
    WHERE application_status = 'Declined'
    """)

    conn.commit()
    conn.close()

def delete_overdue_grants():

    from datetime import date

    today = date.today().isoformat()

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    DELETE FROM grants
    WHERE deadline != ''
    AND deadline < ?
    AND application_status != 'Awarded'
    """, (today,))

    conn.commit()
    conn.close()

def delete_old_grants():

    delete_declined_grants()

    delete_overdue_grants()

def archive_declined_grants():

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    UPDATE grants
    SET archived = 1
    WHERE application_status = 'Declined'
    """)

    conn.commit()
    conn.close()

def archive_overdue_grants():

    from datetime import date

    today = date.today().isoformat()

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    UPDATE grants
    SET archived = 1
    WHERE deadline != ''
    AND deadline < ?
    AND application_status != 'Awarded'
    """, (today,))

    conn.commit()
    conn.close()

def archive_old_grants():

    archive_declined_grants()

    archive_overdue_grants()

def get_archived_grants():

    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute("""
    SELECT *
    FROM grants
    WHERE archived = 1
    ORDER BY score DESC
    """).fetchall()

    conn.close()

    return rows

def restore_grant(url):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    UPDATE grants
    SET archived = 0
    WHERE url = ?
    """, (url,))

    conn.commit()
    conn.close()

def archive_grant(url):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    UPDATE grants
    SET archived = 1
    WHERE url = ?
    """, (url,))

    conn.commit()
    conn.close()

def delete_grant(url):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    DELETE FROM grants
    WHERE url = ?
    """, (url,))

    conn.commit()
    conn.close()