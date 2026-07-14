import json
import os
from pathlib import Path

import ee


LOCAL_KEY_FILE = (
    Path.home()
    / ".astraair"
    / "earth-engine-key.json"
)


def initialize_gee():
    # 1. Streamlit Cloud / deployed service account
    service_account_json = os.getenv(
        "EE_SERVICE_ACCOUNT_JSON"
    )

    if service_account_json:
        service_account_info = json.loads(
            service_account_json
        )

        project_id = service_account_info["project_id"]
        client_email = service_account_info["client_email"]

        credentials = ee.ServiceAccountCredentials(
            client_email,
            key_data=service_account_json,
        )

        ee.Initialize(
            credentials=credentials,
            project=project_id,
        )

        print(
            "✅ Earth Engine connected using "
            "deployment service account"
        )
        return

    # 2. Local service-account JSON
    if LOCAL_KEY_FILE.exists():
        with open(
            LOCAL_KEY_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            service_account_info = json.load(file)

        project_id = service_account_info["project_id"]
        client_email = service_account_info["client_email"]

        credentials = ee.ServiceAccountCredentials(
            client_email,
            str(LOCAL_KEY_FILE),
        )

        ee.Initialize(
            credentials=credentials,
            project=project_id,
        )

        print(
            "✅ Earth Engine connected using "
            "local service account"
        )
        return

    # 3. Optional personal local authentication
    project_id = os.getenv("EE_PROJECT_ID")

    if not project_id:
        raise RuntimeError(
            "Earth Engine project ID is missing. "
            "Add the service-account JSON file at "
            f"{LOCAL_KEY_FILE} or set EE_PROJECT_ID."
        )

    ee.Initialize(project=project_id)

    print(
        "✅ Earth Engine connected using "
        "local authenticated credentials"
    )