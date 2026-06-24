import requests

def fetch_grantsgov_grants():

    try:

        response = requests.post(
            "https://api.grants.gov/v1/api/search2",
            json={
                "rows": 100,
                "keyword": "environment OR ecology OR conservation OR wildlife",
                "oppStatuses": "posted"
            },
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        print(data.keys())
        print(data)

        grants = []

        opp_hits = (
            data.get("oppHits")
            or data.get("data", {}).get("oppHits")
            or []
        )

        print(f"Found {len(opp_hits)} opportunities")

        for opp in opp_hits:

            title = opp.get(
                "title",
                ""
            )

            keywords = [
                "environment",
                "ecology",
                "conservation",
                "wildlife",
                "habitat",
                "restoration",
                "forest",
                "grassland",
                "wetland",
                "natural resource",
                "park",
                "fish",
                "species"
            ]

            if not any(
                k in title.lower()
                for k in keywords
            ):
                continue

            if not opp.get("agency"):
                print(opp)
            
            grants.append({

                "title": title,

                "url":
                    f"https://www.grants.gov/search-results-detail/{opp.get('number', '')}",

                "source": "Grants.gov",

                "agency": (
                    opp.get("agency")
                    or opp.get("agencyName")
                    or opp.get("agencyCode")
                    or "Unknown"
                ),

                "status": opp.get(
                    "oppStatus",
                    ""
                ),

                "open_date": opp.get(
                    "openDate",
                    ""
                ),

                "deadline": opp.get(
                    "closeDate",
                    ""
                ),

                "funding": (
                    opp.get("awardCeiling")
                    or opp.get("awardFloor")
                    or ""
                )
            })

        print(
            f"Returning {len(grants)} Grants.gov grants"
        )
        
        return grants

    except Exception as e:

        print(
            f"Grants.gov error: {e}"
        )

        return []