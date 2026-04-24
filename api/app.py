from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from db import get_db
import os

# Directories
API_DIR      = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR     = os.path.abspath(os.path.join(API_DIR, ".."))
ADMIN_DIR    = os.path.join(ROOT_DIR, "admin")

app = Flask(__name__, static_folder=ROOT_DIR, static_url_path="")
CORS(app, origins=["*"])  # Restrict to your domain in production


# ─────────────────────────────────────────
# FRONTEND ROUTES
# ─────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(ROOT_DIR, "index.html")


@app.route("/admin/")
@app.route("/admin")
def admin():
    return send_from_directory(ADMIN_DIR, "index.html")


# ─────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


# ─────────────────────────────────────────
# BIO
# ─────────────────────────────────────────
@app.route("/api/bio", methods=["GET"])
def get_bio():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bio LIMIT 1")
    row = cursor.fetchone()
    cursor.close()
    return jsonify(row or {})


@app.route("/api/bio", methods=["POST"])
def update_bio():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO bio (id, name, role, bio, tagline, github, linkedin, email, photo)
        VALUES (1, %(name)s, %(role)s, %(bio)s, %(tagline)s, %(github)s, %(linkedin)s, %(email)s, %(photo)s)
        ON DUPLICATE KEY UPDATE
            name=VALUES(name), role=VALUES(role), bio=VALUES(bio),
            tagline=VALUES(tagline), github=VALUES(github),
            linkedin=VALUES(linkedin), email=VALUES(email), photo=VALUES(photo)
    """, {
        "name":     data.get("name", ""),
        "role":     data.get("role", ""),
        "bio":      data.get("bio", ""),
        "tagline":  data.get("tagline", ""),
        "github":   data.get("github", ""),
        "linkedin": data.get("linkedin", ""),
        "email":    data.get("email", ""),
        "photo":    data.get("photo", ""),
    })
    db.commit()
    cursor.close()
    return jsonify({"success": True})


# ─────────────────────────────────────────
# PROJECTS
# ─────────────────────────────────────────
@app.route("/api/projects", methods=["GET"])
def get_projects():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects ORDER BY sort_order ASC, created_at ASC")
    rows = cursor.fetchall()
    cursor.close()
    for row in rows:
        row["tags"]          = row["tags"].split(",") if row.get("tags") else []
        row["features"]      = row["features"].split("\n") if row.get("features") else []
        row["code_snippets"] = row["code_snippets"] if row.get("code_snippets") else []
        row["images"]        = row["images"] if row.get("images") else []
    return jsonify(rows)


@app.route("/api/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects WHERE id=%s", (project_id,))
    row = cursor.fetchone()
    cursor.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    row["tags"]          = row["tags"].split(",") if row.get("tags") else []
    row["features"]      = row["features"].split("\n") if row.get("features") else []
    row["code_snippets"] = row["code_snippets"] if row.get("code_snippets") else []
    row["images"]        = row["images"] if row.get("images") else []
    return jsonify(row)


@app.route("/api/projects", methods=["POST"])
def create_project():
    import json as _json
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO projects (name, type, description, tags, url, features, sort_order,
                              full_description, overview, challenges, outcome, tech_stack,
                              code_snippets, images)
        VALUES (%(name)s, %(type)s, %(desc)s, %(tags)s, %(url)s, %(features)s, %(sort_order)s,
                %(full_description)s, %(overview)s, %(challenges)s, %(outcome)s, %(tech_stack)s,
                %(code_snippets)s, %(images)s)
    """, {
        "name":             data.get("name", ""),
        "type":             data.get("type", "sw"),
        "desc":             data.get("desc", ""),
        "tags":             ",".join(data.get("tags", [])),
        "url":              data.get("url", ""),
        "features":         "\n".join(data.get("features", [])),
        "sort_order":       data.get("sort_order", 0),
        "full_description": data.get("full_description", ""),
        "overview":         data.get("overview", ""),
        "challenges":       data.get("challenges", ""),
        "outcome":          data.get("outcome", ""),
        "tech_stack":       data.get("tech_stack", ""),
        "code_snippets":    _json.dumps(data.get("code_snippets", [])),
        "images":           _json.dumps(data.get("images", [])),
    })
    db.commit()
    new_id = cursor.lastrowid
    cursor.close()
    return jsonify({"success": True, "id": new_id})


@app.route("/api/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    import json as _json
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE projects SET
            name=%(name)s, type=%(type)s, description=%(desc)s,
            tags=%(tags)s, url=%(url)s, features=%(features)s,
            sort_order=%(sort_order)s, full_description=%(full_description)s,
            overview=%(overview)s, challenges=%(challenges)s,
            outcome=%(outcome)s, tech_stack=%(tech_stack)s,
            code_snippets=%(code_snippets)s, images=%(images)s
        WHERE id=%(id)s
    """, {
        "name":             data.get("name", ""),
        "type":             data.get("type", "sw"),
        "desc":             data.get("desc", ""),
        "tags":             ",".join(data.get("tags", [])),
        "url":              data.get("url", ""),
        "features":         "\n".join(data.get("features", [])),
        "sort_order":       data.get("sort_order", 0),
        "full_description": data.get("full_description", ""),
        "overview":         data.get("overview", ""),
        "challenges":       data.get("challenges", ""),
        "outcome":          data.get("outcome", ""),
        "tech_stack":       data.get("tech_stack", ""),
        "code_snippets":    _json.dumps(data.get("code_snippets", [])),
        "images":           _json.dumps(data.get("images", [])),
        "id":               project_id,
    })
    db.commit()
    cursor.close()
    return jsonify({"success": True})


@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM projects WHERE id=%s", (project_id,))
    db.commit()
    cursor.close()
    return jsonify({"success": True})


# ─────────────────────────────────────────
# BLOG POSTS
# ─────────────────────────────────────────
@app.route("/api/posts", methods=["GET"])
def get_posts():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts ORDER BY date DESC, created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    for row in rows:
        if row.get("date"):
            row["date"] = str(row["date"])
        if row.get("created_at"):
            row["created_at"] = str(row["created_at"])
    return jsonify(rows)


@app.route("/api/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO posts (title, category, excerpt, content, url, date)
        VALUES (%(title)s, %(category)s, %(excerpt)s, %(content)s, %(url)s, %(date)s)
    """, {
        "title":    data.get("title", ""),
        "category": data.get("category", ""),
        "excerpt":  data.get("excerpt", ""),
        "content":  data.get("content", ""),
        "url":      data.get("url", ""),
        "date":     data.get("date") or None,
    })
    db.commit()
    new_id = cursor.lastrowid
    cursor.close()
    return jsonify({"success": True, "id": new_id})


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE posts SET
            title=%(title)s, category=%(category)s, excerpt=%(excerpt)s,
            content=%(content)s, url=%(url)s, date=%(date)s
        WHERE id=%(id)s
    """, {
        "title":    data.get("title", ""),
        "category": data.get("category", ""),
        "excerpt":  data.get("excerpt", ""),
        "content":  data.get("content", ""),
        "url":      data.get("url", ""),
        "date":     data.get("date") or None,
        "id":       post_id,
    })
    db.commit()
    cursor.close()
    return jsonify({"success": True})


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM posts WHERE id=%s", (post_id,))
    db.commit()
    cursor.close()
    return jsonify({"success": True})



# ─────────────────────────────────────────
# CONTACT
# ─────────────────────────────────────────
@app.route("/api/contact", methods=["POST"])
def contact():
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    data    = request.get_json()
    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not all([name, email, message]):
        return jsonify({"success": False, "error": "Missing fields"}), 400

    # Get email config from .env
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    mail_to   = os.getenv("CONTACT_EMAIL", smtp_user)

    if not smtp_user or not smtp_pass:
        # If SMTP not configured, just log and return success
        print(f"Contact form: {name} <{email}>: {message}")
        return jsonify({"success": True})

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Portfolio Contact: {name}"
        msg["From"]    = smtp_user
        msg["To"]      = mail_to
        msg["Reply-To"] = email

        body = f"""New message from your portfolio contact form:

Name:    {name}
Email:   {email}

Message:
{message}
"""
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, mail_to, msg.as_string())

        return jsonify({"success": True})
    except Exception as e:
        print(f"SMTP error: {e}")
        return jsonify({"success": False, "error": "Failed to send email"}), 500


if __name__ == "__main__":
    app.run(debug=True)
