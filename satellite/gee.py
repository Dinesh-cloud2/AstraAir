import json
import os
from pathlib import Path

import ee

try:
    import streamlit as st
except ImportError:
    st = None


LOCAL_KEY_FILE = (
    Path.home()
    / ".astraair"
    / "earth-engine-key.json"
)


def initialize_gee():

    # --------------------------------------------------
    # 1. Streamlit Cloud Secrets (Recommended)
    # --------------------------------------------------
    if st is not None:
        try:
            if "earth_engine" in st.secrets:

                service_account_info = dict(
                    st.secrets["earth_engine"]
                )

                project_id = st.secrets["EE_PROJECT_ID"]

                client_email = service_account_info[
                    "client_email"
                ]

                credentials = ee.ServiceAccountCredentials(
                    client_email,
                    key_data=json.dumps(service_account_info),
                )

                ee.Initialize(
                    credentials=credentials,
                    project=project_id,
                )

                print(
                    "✅ Earth Engine connected using Streamlit Secrets"
                )
                return

        except Exception as e:
            print(
                f"Streamlit Secrets initialization failed: {e}"
            )

    # --------------------------------------------------
    # 2. Environment Variable
    # --------------------------------------------------
    service_account_json = os.getenv(
        "EE_SERVICE_ACCOUNT_JSON"
    )

    if service_account_json:

        service_account_info = json.loads(
            service_account_json
        )

        project_id = service_account_info["project_id"]

        client_email = service_account_info[
            "client_email"
        ]

        credentials = ee.ServiceAccountCredentials(
            client_email,
            key_data=service_account_json,
        )

        ee.Initialize(
            credentials=credentials,
            project=project_id,
        )

        print(
            "✅ Earth Engine connected using environment variable"
        )
        return

    # --------------------------------------------------
    # 3. Local JSON file
    # --------------------------------------------------
    if LOCAL_KEY_FILE.exists():

        with open(
            LOCAL_KEY_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            service_account_info = json.load(file)

        project_id = service_account_info[
            "project_id"
        ]

        client_email = service_account_info[
            "client_email"
        ]

        credentials = ee.ServiceAccountCredentials(
            client_email,
            str(LOCAL_KEY_FILE),
        )

        ee.Initialize(
            credentials=credentials,
            project=project_id,
        )

        print(
            "✅ Earth Engine connected using local JSON"
        )
        return

    # --------------------------------------------------
    # 4. Personal authentication
    # --------------------------------------------------
    project_id = os.getenv("EE_PROJECT_ID")

    if project_id:

        ee.Initialize(project=project_id)

        print(
            "✅ Earth Engine connected using personal authentication"
        )
        return

    raise RuntimeError(
        "Earth Engine authentication could not be initialized."
    )