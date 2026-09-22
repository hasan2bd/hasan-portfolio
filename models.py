from database import db
from flask_login import UserMixin


# =========================
# PROJECT
# =========================

class Project(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(50),
        default="IN PROGRESS"
    )

    tools = db.Column(
        db.Text
    )

    image_url = db.Column(
        db.String(500)
    )

    project_url = db.Column(
        db.String(500)
    )

    featured = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


# =========================
# SKILL
# =========================

class Skill(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    level = db.Column(
        db.String(50)
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


# =========================
# EDUCATION
# =========================

class Education(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    institution = db.Column(
        db.String(200),
        nullable=False
    )

    degree = db.Column(
        db.String(200)
    )

    field = db.Column(
        db.String(200)
    )

    start_year = db.Column(
        db.String(20)
    )

    end_year = db.Column(
        db.String(20)
    )

    description = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


# =========================
# EXPERIENCE
# =========================

class Experience(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    organization = db.Column(
        db.String(200)
    )

    period = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

# =========================
# GALLERY IMAGE
# =========================

class GalleryImage(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200)
    )

    image_url = db.Column(
        db.String(500),
        nullable=False
    )

    caption = db.Column(
        db.Text
    )

    display_order = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # =========================
# SITE SETTINGS
# =========================

class SiteSetting(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(
        db.String(500),
        default="images/profile.jpg"
    )
# =========================
# ADMIN
# =========================

class Admin(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )