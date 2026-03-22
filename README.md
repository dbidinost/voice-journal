# Voice Journal

A browser-based voice journaling app. Record audio entries from any device, store them in Firebase, and transcribe them with Whisper (OpenAI API or local server).

**Live app:** [voice-journal-kappa.vercel.app](https://voice-journal-kappa.vercel.app)

---

## How it works

```
Browser (index.html)
  │
  ├── Records audio via MediaRecorder API → .webm blob
  ├── Uploads audio to Firebase Storage  → journals/*.webm
  │
  └── Transcription (on demand, per entry)
        ├── Option A: OpenAI Whisper API  (works on any device, needs API key)
        └── Option B: Local Flask server  (free, needs server.py running locally)
              └── server.py → Whisper base model → returns text
                    └── Transcript saved to Firebase → journals/*.txt
```

Everything persistent lives in Firebase Storage under the `journals/` folder:

| File | Description |
|------|-------------|
| `journal_<timestamp>.webm` | Audio recording |
| `journal_<timestamp>.txt` | Transcription (same base name) |

Firebase credentials and OpenAI API key are stored in browser `localStorage` — they never leave your device.

---

## First-time setup

### 1. Firebase project

1. Go to [console.firebase.google.com](https://console.firebase.google.com) and create a project
2. Enable **Storage** (start in test mode or set rules as needed)
3. Go to **Project Settings → Your apps → Web app** and copy the config values
4. If accessing from multiple devices/origins, set CORS on the bucket:

```bash
gsutil cors set cors.json gs://YOUR-BUCKET-NAME
```

The included [cors.json](cors.json) allows all origins. Edit it to restrict to your domain if needed.

### 2. Open the app

Go to [voice-journal-kappa.vercel.app](https://voice-journal-kappa.vercel.app) and enter your Firebase credentials (one-time setup per browser):

- API Key
- Auth Domain (`your-app.firebaseapp.com`)
- Project ID
- Storage Bucket (`your-app.appspot.com`)

### 3. Transcription setup (pick one)

**Option A — OpenAI API (recommended for phone/tablet use):**

1. Get an API key from [platform.openai.com](https://platform.openai.com)
2. Paste it into the **OpenAI Key** field in the app and click Save
3. Transcription will use `whisper-1` via the OpenAI API

**Option B — Local Whisper server (free, desktop only):**

```bash
pip install -r requirements.txt
python server.py
```

Server runs on `http://localhost:5000`. Leave the OpenAI key field empty and the app will fall back to this server automatically.

---

## Recording & saving entries

1. Tap **TAP TO RECORD** → speak → tap again to stop
2. Preview the audio, then choose:
   - **Save to Firebase** — stores the `.webm` in Firebase
   - **Download Local** — saves the file to your device (not synced)
3. Alternatively, use **Upload Audio File** to add an existing recording

---

## Transcribing an entry

In the **Your Audio Journal** list, each entry has:

- **Transcribe** — runs transcription and saves a `.txt` to Firebase alongside the audio
- **Transcript** — appears after transcription; downloads the `.txt` file
- **Play** — streams audio directly from Firebase
- **Download** — saves the `.webm` to your device
- **Delete** — removes the entry from Firebase

---

## Making changes

### Frontend (index.html)

The entire frontend is a single self-contained HTML file — no build step needed.

- **Recording logic:** `startRecording()` / `stopRecording()` (~line 651)
- **Firebase upload:** `saveToFirebaseBtn` click handler (~line 741)
- **Load & render entries:** `loadEntries()` (~line 803)
- **Transcription logic:** `transcribeEntry()` (~line 943) — handles both OpenAI and local server paths

After editing, push to GitHub and Vercel deploys automatically.

### Backend (server.py)

Used only for local transcription (Option B). Flask app with a single `/transcribe` endpoint:

- Accepts a `multipart/form-data` POST with a `file` field
- Saves to a temp file, runs `whisper.load_model("base").transcribe()`, deletes temp file, returns `{"text": "..."}`
- Change `"base"` to `"small"`, `"medium"`, or `"large"` for better accuracy (slower)

The backend is **not deployed to Vercel** — it runs locally only.

---

## Deploying changes

```bash
git add index.html          # or any other changed files
git commit -m "your message"
git push origin main
```

Vercel picks up the push and redeploys automatically. The backend (`server.py`) is not deployed — it's local only.

---

## Repository

[github.com/dbidinost/voice-journal](https://github.com/dbidinost/voice-journal)

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vanilla HTML/CSS/JS, no framework |
| Audio recording | Browser MediaRecorder API |
| Storage | Firebase Storage |
| Transcription (cloud) | OpenAI Whisper API (`whisper-1`) |
| Transcription (local) | Python + [openai-whisper](https://github.com/openai/whisper) + Flask |
| Hosting | Vercel (static, index.html only) |
