# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from typing import Any, Dict, List, Optional
import uuid

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.cloud import firestore
from google.genai import types

MODEL = "gemini-3.8-flash"
FIRESTORE_PROJECT = "qwiklabs-gcp-03-f83654ef0227"

# Persistent Firestore client initialized with explicit project ID
_db: Optional[firestore.Client] = None


def get_firestore_client() -> firestore.Client:
    global _db
    if _db is None:
        _db = firestore.Client(project=FIRESTORE_PROJECT)
    return _db


def list_analysis_reports(sport: Optional[str] = None, player_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves sports game video analysis reports from Firestore.

    Args:
        sport: Optional sport name to filter by (e.g., 'cricket', 'badminton', 'hockey').
        player_name: Optional player name to filter by.

    Returns:
        A list of analysis report dictionaries.
    """
    db = get_firestore_client()
    query = db.collection("analysis_reports")

    if sport:
        query = query.where("sport", "==", sport.lower().strip())
    if player_name:
        query = query.where("player_name", "==", player_name.strip())

    docs = query.stream()
    reports = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        reports.append(data)
    return reports


def get_analysis_report(report_id: str) -> Dict[str, Any]:
    """Retrieves a specific sports analysis report by its ID.

    Args:
        report_id: The unique ID of the report (e.g., 'report-cricket-001').

    Returns:
        The report dictionary, or an error message dictionary if not found.
    """
    db = get_firestore_client()
    doc_ref = db.collection("analysis_reports").document(report_id)
    doc = doc_ref.get()
    if not doc.exists:
        return {"error": f"Report with ID '{report_id}' not found."}
    data = doc.to_dict()
    data["id"] = doc.id
    return data


def save_analysis_report(
    player_name: str,
    sport: str,
    session_title: str,
    what_went_well: List[str],
    what_went_wrong: List[str],
    improvement_drills: List[str],
    strategy_tips: str,
    video_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Saves a new video game analysis report into Firestore.

    Args:
        player_name: Name of the player (e.g., 'Alex').
        sport: Sport analyzed (e.g., 'cricket', 'badminton', 'hockey').
        session_title: Brief title describing the gameplay or drill session.
        what_went_well: List of positive observations, strengths, or successful executions.
        what_went_wrong: List of errors, bad habits, or weaknesses identified.
        improvement_drills: List of recommended drills or practice routines.
        strategy_tips: Strategic advice to apply in subsequent matches.
        video_url: Optional URL or cloud storage path of the analyzed gameplay video.

    Returns:
        A dictionary confirming the created report ID and status.
    """
    db = get_firestore_client()
    report_id = f"report-{sport.lower().strip()}-{uuid.uuid4().hex[:6]}"
    report_data = {
        "id": report_id,
        "player_name": player_name.strip(),
        "sport": sport.lower().strip(),
        "session_title": session_title.strip(),
        "video_url": video_url or "",
        "what_went_well": what_went_well,
        "what_went_wrong": what_went_wrong,
        "improvement_drills": improvement_drills,
        "strategy_tips": strategy_tips,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    db.collection("analysis_reports").document(report_id).set(report_data)
    return {"status": "success", "report_id": report_id, "report": report_data}


def lookup_training_playbook(sport: str, focus_area: Optional[str] = None) -> List[Dict[str, Any]]:
    """Looks up curated training drills, technique cues, and tactical playbook guides.

    Args:
        sport: The sport to query (e.g., 'cricket', 'badminton', 'hockey').
        focus_area: Optional specific technique or weakness to search for (e.g., 'footwork', 'smash', 'drive', 'passing', 'grip').

    Returns:
        A list of matching drill and strategy playbook items.
    """
    playbooks = [
        # Cricket
        {
            "sport": "cricket",
            "drill_name": "Stationary Drop-Ball Drive Drill",
            "focus_area": "footwork and bat swing",
            "difficulty": "Beginner to Intermediate",
            "reps_or_duration": "3 sets of 20 repetitions",
            "coaching_cues": "Align front toe toward cover, bend front knee, and lead with a high elbow.",
            "target_outcome": "Solid contact under the player's eyes without slicing across the line.",
        },
        {
            "sport": "cricket",
            "drill_name": "Cone Hurdle Back-Foot Anchor",
            "focus_area": "footwork",
            "difficulty": "Intermediate",
            "reps_or_duration": "4 sets of 15 drives",
            "coaching_cues": "Place a low cone behind back heel. If the foot drags, it knocks the cone over.",
            "target_outcome": "Stabilizes balance base during full-blooded drives.",
        },
        {
            "sport": "cricket",
            "drill_name": "Spin Release Bat-Face Modulation",
            "focus_area": "grip and spin",
            "difficulty": "Advanced",
            "reps_or_duration": "10 overs of throwdowns",
            "coaching_cues": "Loosen bottom hand pressure at the moment of impact to play softly into gaps.",
            "target_outcome": "Prevents leading edges when facing turning deliveries.",
        },
        # Badminton
        {
            "sport": "badminton",
            "drill_name": "Scissor-Kick Smash & Base Recovery",
            "focus_area": "smash and recovery",
            "difficulty": "Intermediate to Advanced",
            "reps_or_duration": "5 sets of 10 smashes",
            "coaching_cues": "Contact shuttle at 1 o'clock ahead of head, land softly on non-dominant foot, split-step immediately.",
            "target_outcome": "Reduces recovery transition time to under 0.8 seconds.",
        },
        {
            "sport": "badminton",
            "drill_name": "Two-Corner High Racket Feeder",
            "focus_area": "racket carriage",
            "difficulty": "Beginner to Intermediate",
            "reps_or_duration": "12 minutes continuous",
            "coaching_cues": "Racket head must return above chin level immediately following every stroke.",
            "target_outcome": "Eliminates vulnerability to quick flat net counter-attacks.",
        },
        # Hockey
        {
            "sport": "hockey",
            "drill_name": "Disguised Push & Sweep Passing",
            "focus_area": "passing and deception",
            "difficulty": "Intermediate",
            "reps_or_duration": "4 sets of 12 passes each side",
            "coaching_cues": "Maintain identical hip alignment until stick release; disguise intent with vision misdirection.",
            "target_outcome": "Bypasses pressing defenders without telegraphing passing lanes.",
        },
        {
            "sport": "hockey",
            "drill_name": "Slap Shot Low Deflection Accuracy",
            "focus_area": "slap shot and deflections",
            "difficulty": "Advanced",
            "reps_or_duration": "30 target hits",
            "coaching_cues": "Keep hands 6 inches apart, keep ball in line with front foot, follow through low to the turf.",
            "target_outcome": "Generates low trajectory slap shots ideal for baseline deflections.",
        },
    ]

    sport_clean = sport.lower().strip()
    results = [item for item in playbooks if item["sport"] == sport_clean]

    if focus_area:
        query_kw = focus_area.lower().strip()
        filtered = [
            item for item in results
            if query_kw in item["focus_area"].lower() or query_kw in item["drill_name"].lower()
        ]
        if filtered:
            return filtered

    return results if results else [item for item in playbooks if focus_area and focus_area.lower() in item["focus_area"].lower()]


def fetch_pro_athlete_profile(player_name: str) -> Dict[str, Any]:
    """Fetches real-world professional athlete profiles, positions, and details from TheSportsDB public API.

    Useful for benchmarking player stats, technique references, or comparing gameplay against pro athletes.

    Args:
        player_name: The name of the athlete to look up (e.g. 'Virat Kohli', 'Joe Root', 'Lionel Messi').

    Returns:
        A dictionary containing the athlete profile data or a status message.
    """
    import os
    import urllib.parse
    import urllib.request
    import json

    api_key = os.getenv("THESPORTSDB_API_KEY", "3")
    encoded_name = urllib.parse.quote(player_name.strip())
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/searchplayers.php?p={encoded_name}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SportsVideoAnalyst/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            players = data.get("player")
            if not players:
                return {"status": "not_found", "message": f"No professional athlete profile found for '{player_name}'."}
            
            p = players[0]
            return {
                "status": "success",
                "player_name": p.get("strPlayer"),
                "sport": p.get("strSport"),
                "team": p.get("strTeam"),
                "nationality": p.get("strNationality"),
                "position": p.get("strPosition"),
                "birth_date": p.get("dateBorn"),
                "description": (p.get("strDescriptionEN") or "")[:350] + ("..." if len(p.get("strDescriptionEN") or "") > 350 else ""),
                "thumb_url": p.get("strThumb") or "",
            }
    except Exception as e:
        return {"status": "error", "message": f"Failed to fetch athlete profile: {str(e)}"}


STORAGE_BUCKET = "sports-video-analyst-media-f83654ef0227"


async def generate_tactical_diagram(
    sport: str,
    subject_description: str,
    tool_context: Optional[Any] = None,
) -> Dict[str, Any]:
    """Generates a tactical visual or form diagram for a sport using gemini-3.1-flash-lite-image in the global region.

    Saves the image as an artifact in the session (so it appears in Playground's Artifacts panel)
    and uploads the bytes directly to Cloud Storage, returning the public HTTPS URL.

    Args:
        sport: The sport for the diagram (e.g. 'cricket', 'badminton', 'hockey').
        subject_description: Description of the stance, tactic, shot, or drill diagram to illustrate.
        tool_context: ADK ToolContext automatically injected by the runtime.

    Returns:
        A dictionary with the public image URL, filename, and status.
    """
    from google import genai
    from google.cloud import storage
    from google.genai import types as genai_types

    prompt = (
        f"A clean, detailed sports coaching tactical illustration and biomechanical form diagram for {sport}. "
        f"{subject_description}. Professional athletic diagram with clear posture lines, field/court markings, and technique arrows."
    )

    try:
        # Generate image using gemini-3.1-flash-lite-image in the global location
        client = genai.Client(vertexai=True, project=FIRESTORE_PROJECT, location="global")
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-image",
            contents=prompt,
        )

        image_bytes = None
        mime_type = "image/jpeg"
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    image_bytes = part.inline_data.data
                    mime_type = part.inline_data.mime_type or "image/jpeg"
                    break

        if not image_bytes:
            return {"status": "error", "message": "No image data was generated by the model."}

        extension = "png" if "png" in mime_type else "jpg"
        clean_sport = sport.lower().strip()
        filename = f"diagram_{clean_sport}_{uuid.uuid4().hex[:6]}.{extension}"

        # 1. Save artifact in session context so it appears in Playground Artifacts panel
        if tool_context is not None and hasattr(tool_context, "save_artifact"):
            try:
                artifact_part = genai_types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
                await tool_context.save_artifact(filename=filename, artifact=artifact_part)
            except Exception as artifact_err:
                print(f"Warning: tool_context.save_artifact failed: {artifact_err}")

        # 2. Upload bytes to public Cloud Storage bucket
        gcs_client = storage.Client(project=FIRESTORE_PROJECT)
        bucket = gcs_client.bucket(STORAGE_BUCKET)
        blob = bucket.blob(filename)
        blob.upload_from_string(image_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{STORAGE_BUCKET}/{filename}"
        return {
            "status": "success",
            "filename": filename,
            "public_url": public_url,
            "sport": sport,
            "description": subject_description,
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to generate diagram: {str(e)}"}


async def generate_sports_video(
    sport: str,
    action_description: str,
    tool_context: Optional[Any] = None,
) -> Dict[str, Any]:
    """Generates a short sports gameplay or drill video using Google's Omni model (gemini-omni-flash-preview) in the global region.

    Saves the video as an artifact in the session (so it appears in Playground's Artifacts panel)
    and uploads the bytes directly to Cloud Storage, returning the public HTTPS URL.

    Args:
        sport: The sport for the video (e.g. 'badminton', 'cricket', 'hockey').
        action_description: Specific action, drill, or technique to illustrate in motion (e.g., 'badminton jumping smash footwork', 'cricket forward defensive shot', 'field hockey penalty corner drag flick').
        tool_context: ADK ToolContext automatically injected by the runtime.

    Returns:
        A dictionary with the public video URL, filename, and status.
    """
    import base64
    import time
    import uuid
    import google.auth
    from google.auth.transport.requests import Request
    from google.cloud import storage
    from google.genai import types as genai_types
    import requests

    prompt = (
        f"A cinematic short sports clip showing {sport}: {action_description}. "
        "Clear professional broadcast angle, realistic athletic movement, high visual clarity."
    )

    try:
        creds, _ = google.auth.default()
        creds.refresh(Request())

        url = f"https://aiplatform.googleapis.com/v1beta1/projects/{FIRESTORE_PROJECT}/locations/global/interactions"
        headers = {
            "Authorization": f"Bearer {creds.token}",
            "Content-Type": "application/json",
        }
        body = {
            "model": "gemini-omni-flash-preview",
            "input": [{"type": "text", "text": prompt}],
        }

        resp = requests.post(url, json=body, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()

        video_bytes = None
        mime_type = "video/mp4"

        # Check steps in initial response
        for step in data.get("steps", []):
            if step.get("type") == "model_output":
                for item in step.get("content", []):
                    if item.get("type") == "video" and "data" in item:
                        video_bytes = base64.b64decode(item["data"])
                        mime_type = item.get("mime_type", "video/mp4")
                        break

        # If asynchronous or in_progress, poll interaction
        if not video_bytes and data.get("id"):
            interaction_id = data["id"]
            poll_url = f"{url}/{interaction_id}"
            for _ in range(20):
                time.sleep(3)
                creds.refresh(Request())
                headers["Authorization"] = f"Bearer {creds.token}"
                poll_resp = requests.get(poll_url, headers=headers, timeout=60)
                if poll_resp.status_code == 200:
                    poll_data = poll_resp.json()
                    for step in poll_data.get("steps", []):
                        if step.get("type") == "model_output":
                            for item in step.get("content", []):
                                if item.get("type") == "video" and "data" in item:
                                    video_bytes = base64.b64decode(item["data"])
                                    mime_type = item.get("mime_type", "video/mp4")
                                    break
                    if video_bytes or poll_data.get("status") == "completed":
                        break

        if not video_bytes:
            return {"status": "error", "message": "No video data returned from gemini-omni-flash-preview."}

        clean_sport = sport.lower().strip().replace(" ", "_")
        filename = f"video_{clean_sport}_{uuid.uuid4().hex[:6]}.mp4"

        # 1. Save artifact in session context so it appears in Playground Artifacts panel
        if tool_context is not None and hasattr(tool_context, "save_artifact"):
            try:
                artifact_part = genai_types.Part.from_bytes(data=video_bytes, mime_type=mime_type)
                await tool_context.save_artifact(filename=filename, artifact=artifact_part)
            except Exception as artifact_err:
                print(f"Warning: tool_context.save_artifact failed: {artifact_err}")

        # 2. Upload bytes to public Cloud Storage bucket
        gcs_client = storage.Client(project=FIRESTORE_PROJECT)
        bucket = gcs_client.bucket(STORAGE_BUCKET)
        blob = bucket.blob(filename)
        blob.upload_from_string(video_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{STORAGE_BUCKET}/{filename}"
        return {
            "status": "success",
            "filename": filename,
            "public_url": public_url,
            "sport": sport,
            "action": action_description,
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to generate video: {str(e)}"}


from google.adk.agents.callback_context import CallbackContext
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

SANDBOX_RESOURCE_NAME = (
    "projects/354866654922/locations/us-east1/reasoningEngines/7223964017813880832/sandboxEnvironments/4306188911673081856"
)

MEMORY_BANK_ID = "7223964017813880832"


async def generate_memories_callback(callback_context: CallbackContext):
    """WRITE: after each turn, send the session to Memory Bank for durable fact extraction."""
    await callback_context.add_session_to_memory()
    return None


code_executor = AgentEngineSandboxCodeExecutor(
    sandbox_resource_name=SANDBOX_RESOURCE_NAME
)

from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager
from app.a2ui_utils import a2ui_callback

a2ui_schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

a2ui_instruction = a2ui_schema_manager.generate_system_prompt(
    role_description=(
        "You are an expert Multi-Sport Video Game Analyst and Tactical Coach specializing in cricket, badminton, hockey, "
        "and other sports. Your goal is to analyze player gameplay, break down what went well and what went wrong, recommend "
        "specific improvement drills, and provide winning game strategies for upcoming matches. "
        "You always remember the athlete's stated preferences, all user allergies (food, environmental, and medicinal), "
        "medical conditions, injury history, past weaknesses, and playing habits across sessions, taking special care to never "
        "recommend nutrition or hydration containing known allergens. "
        "Use the Firestore analysis report tools to lookup historical reports, retrieve past session findings, and record new "
        "analysis reports. Use the lookup_training_playbook tool to fetch specific coaching drills and technical cues when "
        "recommending training routines. Use fetch_pro_athlete_profile to look up real-world professional player benchmarks. "
        "Use generate_tactical_diagram to create visual tactical diagrams or stance illustrations whenever visual aid, "
        "court positioning, or posture correction is requested, and present the resulting public image URL. "
        "When performing complex calculations, metric trends analysis, physics calculations (e.g. shot speed, bat swing velocity, "
        "or trajectory angles), write and execute Python code using your secure code execution environment."
    ),
    workflow_description="Analyze the request, call relevant tools or execute code, and return structured UI when appropriate.",
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the URL an image tool returns after uploading "
        "to a public bucket). Set the Image url to that exact https link, for example "
        '{"Image": {"url": {"literalString": "https://..."}}}. Never point an '
        "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=a2ui_instruction,
    tools=[
        PreloadMemoryTool(),
        list_analysis_reports,
        get_analysis_report,
        save_analysis_report,
        lookup_training_playbook,
        fetch_pro_athlete_profile,
        generate_tactical_diagram,
        generate_sports_video,
    ],
    after_agent_callback=generate_memories_callback,
    after_model_callback=a2ui_callback,
    code_executor=code_executor,
)

app = App(
    root_agent=root_agent,
    name="app",
)






