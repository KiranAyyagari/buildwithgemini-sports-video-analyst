import datetime
from google.cloud import firestore

FIRESTORE_PROJECT = "qwiklabs-gcp-03-f83654ef0227"

def seed():
    db = firestore.Client(project=FIRESTORE_PROJECT)
    collection = db.collection("analysis_reports")

    sample_reports = [
        {
            "id": "report-cricket-001",
            "player_name": "Alex",
            "sport": "cricket",
            "session_title": "Cover Drive & Bat Swing Mechanics",
            "video_url": "gs://sports-clips/cricket_cover_drive_01.mp4",
            "what_went_well": [
                "Excellent head position over the ball on front foot drives.",
                "Smooth follow-through with high elbow."
            ],
            "what_went_wrong": [
                "Back foot dragged too early on deliveries outside off-stump.",
                "Slight delay in opening the bat face against spin."
            ],
            "improvement_drills": [
                "Stationary drop-ball cover drive drill (3 sets of 20 reps).",
                "Cone hurdle footwork drill to keep back foot anchored."
            ],
            "strategy_tips": "Against outswing bowlers, play with soft hands and leave deliveries in the corridor of uncertainty early in the innings.",
            "metrics": {
                "stance_balance_score": 8.5,
                "reaction_time_sec": 0.28,
                "shot_execution_accuracy_pct": 78
            },
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        {
            "id": "report-badminton-001",
            "player_name": "Jordan",
            "sport": "badminton",
            "session_title": "Forehand Jump Smash & Recovery",
            "video_url": "gs://sports-clips/badminton_smash_01.mp4",
            "what_went_well": [
                "High contact point at peak jump.",
                "Fast wrist snap generating steep smash angles."
            ],
            "what_went_wrong": [
                "Landing awkwardly on the right ankle instead of split-step recovery.",
                "Racket carriage dropped low after smash, exposing mid-court return."
            ],
            "improvement_drills": [
                "Shadow jump smashes with immediate scissor-kick recovery to base (5 sets of 10).",
                "Two-corner feeder drill focusing on keeping racket up after power shots."
            ],
            "strategy_tips": "Do not force repeated smashes when opponent is entrenched deep; use cross-court slice drops to break defensive rhythm.",
            "metrics": {
                "stance_balance_score": 7.2,
                "smash_speed_kmh": 285,
                "recovery_time_sec": 0.85
            },
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        {
            "id": "report-hockey-001",
            "player_name": "Sam",
            "sport": "hockey",
            "session_title": "Slap Shot & Penalty Corner Injection",
            "video_url": "gs://sports-clips/hockey_slapshot_01.mp4",
            "what_went_well": [
                "Crisp stick contact with explosive hip rotation.",
                "Kept weight forward on delivery."
            ],
            "what_went_wrong": [
                "Hands were positioned too close together on the grip for low passes.",
                "Telegraphed pass direction by shifting body orientation too early."
            ],
            "improvement_drills": [
                "Targeted push-and-sweep wall drills with varied grip spacing (15 minutes).",
                "Disguised passing drill facing a dummy defender."
            ],
            "strategy_tips": "Look for stick deflections at the far post rather than aiming straight for goalkeeper pads.",
            "metrics": {
                "stance_balance_score": 8.0,
                "shot_velocity_kmh": 115,
                "target_accuracy_pct": 82
            },
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    ]

    for report in sample_reports:
        doc_id = report["id"]
        collection.document(doc_id).set(report)
        print(f"Seeded report: {doc_id} ({report['sport']})")

    print(f"Successfully seeded {len(sample_reports)} reports into Firestore.")

if __name__ == "__main__":
    seed()
