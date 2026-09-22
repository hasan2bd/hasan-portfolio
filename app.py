from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from config import Config
from database import db

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import (
    check_password_hash
)

from werkzeug.utils import secure_filename

from models import GalleryImage

import os


# =========================
# APPLICATION SETUP
# =========================

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


# =========================
# PROFILE IMAGE UPLOAD
# =========================

PROFILE_UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "static",
    "uploads",
    "profile"
)

os.makedirs(
    PROFILE_UPLOAD_FOLDER,
    exist_ok=True
)


# =========================
# FLASK LOGIN
# =========================

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "admin_login"


@login_manager.user_loader
def load_user(user_id):

    from models import Admin

    return db.session.get(
        Admin,
        int(user_id)
    )

from io import BytesIO
from xml.sax.saxutils import escape

from flask import send_file

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)

# =========================
# DOWNLOAD CV
# =========================

@app.route("/download-cv")
def download_cv():

    from models import (
        Project,
        Education,
        Experience,
        Skill
    )

    # =========================
    # GET DATA
    # =========================

    education = Education.query.order_by(
        Education.created_at.desc()
    ).all()

    experiences = Experience.query.order_by(
        Experience.created_at.desc()
    ).all()

    skills = Skill.query.order_by(
        Skill.category.asc(),
        Skill.created_at.desc()
    ).all()

    projects = Project.query.order_by(
        Project.created_at.desc()
    ).all()

    # =========================
    # PDF SETUP
    # =========================

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="MD. Mahmudul Hasan - CV",
        author="MD. Mahmudul Hasan"
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "Name",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=27,
        textColor=colors.HexColor("#111318"),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#555A63"),
        spaceAfter=5
    )

    contact_style = ParagraphStyle(
        "Contact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=13,
        textColor=colors.HexColor("#555A63"),
        spaceAfter=2
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#D71920"),
        spaceBefore=10,
        spaceAfter=5,
        uppercase=True
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=13,
        textColor=colors.HexColor("#33373D"),
        spaceAfter=3
    )

    item_title_style = ParagraphStyle(
        "ItemTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#111318"),
        spaceAfter=2
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#555A63")
    )

    # =========================
    # STORY
    # =========================

    story = []

    # =========================
    # HEADER
    # =========================

    story.append(
        Paragraph(
            "MD. MAHMUDUL HASAN",
            name_style
        )
    )

    story.append(
        Paragraph(
            "BA (Hons) in English | Green University of Bangladesh",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            "mahmudul2bd@gmail.com &nbsp; | &nbsp; "
            "github.com/hasan2bd &nbsp; | &nbsp; "
            "linkedin.com/",
            contact_style
        )
    )

    story.append(
        Spacer(1, 4)
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#D71920"),
            spaceBefore=2,
            spaceAfter=8
        )
    )

    # =========================
    # PROFILE
    # =========================

    story.append(
        Paragraph(
            "PROFILE",
            section_style
        )
    )

    story.append(
        Paragraph(
            "BA (Hons) English student at Green University of Bangladesh "
            "with developing strengths in communication, public speaking, "
            "analytical thinking, and business-oriented technical skills. "
            "Interested in combining English, technology, and practical "
            "problem-solving to build a career in modern business environments.",
            body_style
        )
    )

    # =========================
    # EDUCATION
    # =========================

    if education:

        story.append(
            Paragraph(
                "EDUCATION",
                section_style
            )
        )

        for item in education:

            institution = escape(
                item.institution or ""
            )

            degree = escape(
                item.degree or ""
            )

            field = escape(
                item.field or ""
            )

            start_year = escape(
                item.start_year or ""
            )

            end_year = escape(
                item.end_year or ""
            )

            years = ""

            if start_year or end_year:
                years = f" ({start_year}–{end_year})"

            title = degree

            if field:
                title += f" — {field}"

            story.append(
                Paragraph(
                    f"{title}",
                    item_title_style
                )
            )

            story.append(
                Paragraph(
                    f"{institution}{years}",
                    small_style
                )
            )

            if item.description:

                story.append(
                    Paragraph(
                        escape(item.description),
                        body_style
                    )
                )

            story.append(
                Spacer(1, 3)
            )

    # =========================
    # EXPERIENCE
    # =========================

    if experiences:

        story.append(
            Paragraph(
                "EXPERIENCE",
                section_style
            )
        )

        for item in experiences:

            title = escape(
                item.title or ""
            )

            organization = escape(
                item.organization or ""
            )

            period = escape(
                item.period or ""
            )

            story.append(
                Paragraph(
                    title,
                    item_title_style
                )
            )

            meta = organization

            if period:
                if meta:
                    meta += f" &nbsp; | &nbsp; {period}"
                else:
                    meta = period

            if meta:

                story.append(
                    Paragraph(
                        meta,
                        small_style
                    )
                )

            if item.description:

                story.append(
                    Paragraph(
                        escape(item.description),
                        body_style
                    )
                )

            story.append(
                Spacer(1, 3)
            )

    # =========================
    # SKILLS
    # =========================

    if skills:

        story.append(
            Paragraph(
                "SKILLS",
                section_style
            )
        )

        skill_rows = []

        for skill in skills:

            category = escape(
                skill.category or "Skills"
            )

            name = escape(
                skill.name or ""
            )

            level = escape(
                skill.level or ""
            )

            skill_rows.append(
                [
                    Paragraph(
                        f"<b>{category}</b>",
                        small_style
                    ),
                    Paragraph(
                        name,
                        small_style
                    ),
                    Paragraph(
                        level,
                        small_style
                    )
                ]
            )

        table = Table(
            skill_rows,
            colWidths=[
                38 * mm,
                90 * mm,
                35 * mm
            ],
            repeatRows=0
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        0
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        3
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        3
                    )
                ]
            )
        )

        story.append(table)

    # =========================
    # PROJECTS
    # =========================

    if projects:

        story.append(
            Paragraph(
                "SELECTED PROJECTS",
                section_style
            )
        )

        for project in projects:

            title = escape(
                project.title or ""
            )

            category = escape(
                project.category or ""
            )

            description = escape(
                project.description or ""
            )

            tools = escape(
                project.tools or ""
            )

            story.append(
                Paragraph(
                    title,
                    item_title_style
                )
            )

            if category:

                story.append(
                    Paragraph(
                        category,
                        small_style
                    )
                )

            if description:

                story.append(
                    Paragraph(
                        description,
                        body_style
                    )
                )

            if tools:

                story.append(
                    Paragraph(
                        f"<b>Tools:</b> {tools}",
                        small_style
                    )
                )

            story.append(
                Spacer(1, 4)
            )

    # =========================
    # BUILD PDF
    # =========================

    document.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=False,
        download_name="MD-Mahmudul-Hasan-CV.pdf"
    )
# =========================
# PUBLIC WEBSITE
# =========================

# =========================
# PUBLIC WEBSITE
# =========================

@app.route("/")
def home():

    from models import (
        Project,
        Education,
        Experience,
        GalleryImage,
        Skill,
        SiteSetting
    )

    projects = Project.query.order_by(
        Project.created_at.desc()
    ).all()

    education = Education.query.order_by(
        Education.created_at.desc()
    ).all()

    experiences = Experience.query.order_by(
        Experience.id.desc()
    ).all()

    gallery_images = GalleryImage.query.order_by(
        GalleryImage.display_order.asc(),
        GalleryImage.id.desc()
    ).all()

    skills = Skill.query.order_by(
        Skill.created_at.desc()
    ).all()

    # =========================
    # PROFILE PICTURE
    # =========================

    profile_setting = SiteSetting.query.first()

    if profile_setting is None:

        profile_setting = SiteSetting(
            profile_image="images/profile.jpg"
        )

    return render_template(
        "index.html",
        projects=projects,
        education=education,
        experiences=experiences,
        gallery_images=gallery_images,
        skills=skills,
        profile_setting=profile_setting
    )


# =========================
# ADMIN LOGIN
# =========================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        from models import Admin

        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(
            username=username
        ).first()

        if admin and check_password_hash(
            admin.password_hash,
            password
        ):

            login_user(admin)

            return redirect(
                url_for("admin_dashboard")
            )

        flash(
            "Invalid username or password."
        )

    return render_template(
        "admin/login.html"
    )


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin")
@login_required
def admin_dashboard():

    from models import (
        Project,
        Skill,
        Education,
        Experience,
        GalleryImage
    )

    project_count = Project.query.count()
    skill_count = Skill.query.count()
    education_count = Education.query.count()
    experience_count = Experience.query.count()
    gallery_count = GalleryImage.query.count()

    return render_template(
        "admin/dashboard.html",
        project_count=project_count,
        skill_count=skill_count,
        education_count=education_count,
        experience_count=experience_count,
        gallery_count=gallery_count
    )


# =========================
# ADMIN PROJECTS
# =========================

@app.route("/admin/projects")
@login_required
def admin_projects():

    from models import Project

    projects = Project.query.order_by(
        Project.created_at.desc()
    ).all()

    return render_template(
        "admin/projects.html",
        projects=projects
    )


@app.route(
    "/admin/projects/add",
    methods=["GET", "POST"]
)
@login_required
def admin_add_project():

    from models import Project

    if request.method == "POST":

        project = Project(
            title=request.form.get("title"),
            category=request.form.get("category"),
            description=request.form.get("description"),
            status=request.form.get("status"),
            tools=request.form.get("tools"),
            image_url=request.form.get("image_url"),
            project_url=request.form.get("project_url"),
            featured=request.form.get("featured") == "on"
        )

        db.session.add(project)
        db.session.commit()

        return redirect(
            url_for("admin_projects")
        )

    return render_template(
        "admin/project_form.html"
    )


@app.route(
    "/admin/projects/<int:project_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def admin_edit_project(project_id):

    from models import Project

    project = db.session.get(
        Project,
        project_id
    )

    if project is None:

        return redirect(
            url_for("admin_projects")
        )

    if request.method == "POST":

        project.title = request.form.get(
            "title"
        )

        project.category = request.form.get(
            "category"
        )

        project.description = request.form.get(
            "description"
        )

        project.status = request.form.get(
            "status"
        )

        project.tools = request.form.get(
            "tools"
        )

        project.image_url = request.form.get(
            "image_url"
        )

        project.project_url = request.form.get(
            "project_url"
        )

        project.featured = (
            request.form.get("featured") == "on"
        )

        db.session.commit()

        return redirect(
            url_for("admin_projects")
        )

    return render_template(
        "admin/project_form.html",
        project=project
    )


@app.route(
    "/admin/projects/<int:project_id>/delete",
    methods=["POST"]
)
@login_required
def admin_delete_project(project_id):

    from models import Project

    project = db.session.get(
        Project,
        project_id
    )

    if project is not None:

        db.session.delete(project)
        db.session.commit()

    return redirect(
        url_for("admin_projects")
    )


# =========================
# ADMIN SKILLS
# =========================

@app.route("/admin/skills")
@login_required
def admin_skills():

    from models import Skill

    skills = Skill.query.order_by(
        Skill.created_at.desc()
    ).all()

    return render_template(
        "admin/skills.html",
        skills=skills
    )


@app.route(
    "/admin/skills/add",
    methods=["GET", "POST"]
)
@login_required
def admin_add_skill():

    from models import Skill

    if request.method == "POST":

        skill = Skill(
            name=request.form.get("name"),
            category=request.form.get("category"),
            level=request.form.get("level")
        )

        db.session.add(skill)
        db.session.commit()

        return redirect(
            url_for("admin_skills")
        )

    return render_template(
        "admin/skill_form.html"
    )


@app.route(
    "/admin/skills/<int:skill_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def admin_edit_skill(skill_id):

    from models import Skill

    skill = db.session.get(
        Skill,
        skill_id
    )

    if skill is None:

        return redirect(
            url_for("admin_skills")
        )

    if request.method == "POST":

        skill.name = request.form.get(
            "name"
        )

        skill.category = request.form.get(
            "category"
        )

        skill.level = request.form.get(
            "level"
        )

        db.session.commit()

        return redirect(
            url_for("admin_skills")
        )

    return render_template(
        "admin/skill_form.html",
        skill=skill
    )


@app.route(
    "/admin/skills/<int:skill_id>/delete",
    methods=["POST"]
)
@login_required
def admin_delete_skill(skill_id):

    from models import Skill

    skill = db.session.get(
        Skill,
        skill_id
    )

    if skill is not None:

        db.session.delete(skill)
        db.session.commit()

    return redirect(
        url_for("admin_skills")
    )


# =========================
# ADMIN EDUCATION
# =========================

@app.route("/admin/education")
@login_required
def admin_education():

    from models import Education

    education = Education.query.order_by(
        Education.created_at.desc()
    ).all()

    return render_template(
        "admin/education.html",
        education=education
    )


@app.route(
    "/admin/education/add",
    methods=["GET", "POST"]
)
@login_required
def admin_add_education():

    from models import Education

    if request.method == "POST":

        education = Education(
            institution=request.form.get(
                "institution"
            ),
            degree=request.form.get(
                "degree"
            ),
            field=request.form.get(
                "field"
            ),
            start_year=request.form.get(
                "start_year"
            ),
            end_year=request.form.get(
                "end_year"
            ),
            description=request.form.get(
                "description"
            )
        )

        db.session.add(education)
        db.session.commit()

        return redirect(
            url_for("admin_education")
        )

    return render_template(
        "admin/education_form.html"
    )


@app.route(
    "/admin/education/<int:education_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def admin_edit_education(education_id):

    from models import Education

    education = db.session.get(
        Education,
        education_id
    )

    if education is None:

        return redirect(
            url_for("admin_education")
        )

    if request.method == "POST":

        education.institution = request.form.get(
            "institution"
        )

        education.degree = request.form.get(
            "degree"
        )

        education.field = request.form.get(
            "field"
        )

        education.start_year = request.form.get(
            "start_year"
        )

        education.end_year = request.form.get(
            "end_year"
        )

        education.description = request.form.get(
            "description"
        )

        db.session.commit()

        return redirect(
            url_for("admin_education")
        )

    return render_template(
        "admin/education_form.html",
        education=education
    )


@app.route(
    "/admin/education/<int:education_id>/delete",
    methods=["POST"]
)
@login_required
def admin_delete_education(education_id):

    from models import Education

    education = db.session.get(
        Education,
        education_id
    )

    if education is not None:

        db.session.delete(education)
        db.session.commit()

    return redirect(
        url_for("admin_education")
    )

# =========================
# ADMIN EXPERIENCE
# =========================

@app.route("/admin/experience")
@login_required
def admin_experience():

    from models import Experience

    experiences = Experience.query.order_by(
        Experience.id.desc()
    ).all()

    return render_template(
        "admin/experience.html",
        experiences=experiences
    )


@app.route(
    "/admin/experience/add",
    methods=["GET", "POST"]
)
@login_required
def admin_add_experience():

    from models import Experience

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        organization = request.form.get(
            "organization", ""
        ).strip()
        period = request.form.get(
            "period", ""
        ).strip()
        description = request.form.get(
            "description", ""
        ).strip()

        if not title:
            return render_template(
                "admin/experience_form.html",
                error="Experience title is required."
            )

        new_experience = Experience(
            title=title,
            organization=organization,
            period=period,
            description=description
        )

        db.session.add(new_experience)
        db.session.commit()

        return redirect(
            url_for("admin_experience")
        )

    return render_template(
        "admin/experience_form.html"
    )


@app.route(
    "/admin/experience/<int:experience_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def admin_edit_experience(experience_id):

    from models import Experience

    experience = db.session.get(
        Experience,
        experience_id
    )

    if experience is None:
        return redirect(
            url_for("admin_experience")
        )

    if request.method == "POST":

        title = request.form.get(
            "title", ""
        ).strip()

        organization = request.form.get(
            "organization", ""
        ).strip()

        period = request.form.get(
            "period", ""
        ).strip()

        description = request.form.get(
            "description", ""
        ).strip()

        if not title:
            return render_template(
                "admin/experience_form.html",
                experience=experience,
                error="Experience title is required."
            )

        experience.title = title
        experience.organization = organization
        experience.period = period
        experience.description = description

        db.session.commit()

        return redirect(
            url_for("admin_experience")
        )

    return render_template(
        "admin/experience_form.html",
        experience=experience
    )


@app.route(
    "/admin/experience/<int:experience_id>/delete",
    methods=["POST"]
)
@login_required
def admin_delete_experience(experience_id):

    from models import Experience

    experience = db.session.get(
        Experience,
        experience_id
    )

    if experience is not None:

        db.session.delete(experience)
        db.session.commit()

    return redirect(
        url_for("admin_experience")
    )

# =========================
# ADMIN GALLERY
# =========================

@app.route("/admin/gallery")
@login_required
def admin_gallery():

    from models import GalleryImage

    gallery_images = GalleryImage.query.order_by(
        GalleryImage.display_order.asc(),
        GalleryImage.id.desc()
    ).all()

    return render_template(
        "admin/gallery.html",
        gallery_images=gallery_images
    )


@app.route(
    "/admin/gallery/add",
    methods=["GET", "POST"]
)
@login_required
def admin_add_gallery():

    from models import GalleryImage

    if request.method == "POST":

        title = request.form.get(
            "title", ""
        ).strip()

        image_url = request.form.get(
            "image_url", ""
        ).strip()

        caption = request.form.get(
            "caption", ""
        ).strip()

        display_order = request.form.get(
            "display_order", "1"
        ).strip()

        if not image_url:

            return render_template(
                "admin/gallery_form.html",
                error="Image URL is required."
            )

        try:

            display_order = int(
                display_order or 1
            )

        except ValueError:

            display_order = 1

        new_image = GalleryImage(
            title=title,
            image_url=image_url,
            caption=caption,
            display_order=display_order
        )

        db.session.add(new_image)

        db.session.commit()

        return redirect(
            url_for("admin_gallery")
        )

    return render_template(
        "admin/gallery_form.html"
    )


@app.route(
    "/admin/gallery/<int:gallery_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def admin_edit_gallery(gallery_id):

    from models import GalleryImage

    gallery_image = db.session.get(
        GalleryImage,
        gallery_id
    )

    if gallery_image is None:

        return redirect(
            url_for("admin_gallery")
        )

    if request.method == "POST":

        title = request.form.get(
            "title", ""
        ).strip()

        image_url = request.form.get(
            "image_url", ""
        ).strip()

        caption = request.form.get(
            "caption", ""
        ).strip()

        display_order = request.form.get(
            "display_order", "1"
        ).strip()

        if not image_url:

            return render_template(
                "admin/gallery_form.html",
                gallery_image=gallery_image,
                error="Image URL is required."
            )

        try:

            display_order = int(
                display_order or 1
            )

        except ValueError:

            display_order = 1

        gallery_image.title = title

        gallery_image.image_url = image_url

        gallery_image.caption = caption

        gallery_image.display_order = display_order

        db.session.commit()

        return redirect(
            url_for("admin_gallery")
        )

    return render_template(
        "admin/gallery_form.html",
        gallery_image=gallery_image
    )


@app.route(
    "/admin/gallery/<int:gallery_id>/delete",
    methods=["POST"]
)
@login_required
def admin_delete_gallery(gallery_id):

    from models import GalleryImage

    gallery_image = db.session.get(
        GalleryImage,
        gallery_id
    )

    if gallery_image is not None:

        db.session.delete(
            gallery_image
        )

        db.session.commit()

    return redirect(
        url_for("admin_gallery")
    )
# =========================
# ADMIN LOGOUT
# =========================

@app.route("/admin/logout")
@login_required
def admin_logout():

    logout_user()

    return redirect(
        url_for("admin_login")
    )
# =========================
# CREATE DATABASE TABLES
# =========================

with app.app_context():

    from models import (
        Project,
        Skill,
        Education,
        Experience,
        GalleryImage,
        Admin
    )

    from werkzeug.security import generate_password_hash

    db.create_all()

    # Create admin account if it does not exist
    if Admin.query.count() == 0:

        admin_username = app.config.get(
            "ADMIN_USERNAME"
        )

        admin_password = app.config.get(
            "ADMIN_PASSWORD"
        )

        if admin_username and admin_password:

            admin = Admin(
                username=admin_username,
                password_hash=generate_password_hash(
                    admin_password
                )
            )

            db.session.add(admin)
            db.session.commit()




    # =========================
# CHANGE PROFILE PICTURE
# =========================

@app.route(
    "/admin/profile-picture",
    methods=["GET", "POST"]
)
@login_required
def admin_profile_picture():

    from models import SiteSetting

    setting = SiteSetting.query.first()

    if setting is None:

        setting = SiteSetting(
            profile_image="images/profile.jpg"
        )

        db.session.add(setting)
        db.session.commit()

    if request.method == "POST":

        file = request.files.get(
            "profile_image"
        )

        if not file or file.filename == "":
            flash(
                "Please select an image.",
                "error"
            )

            return redirect(
                url_for("admin_profile_picture")
            )

        filename = secure_filename(
            file.filename
        )

        extension = filename.rsplit(
            ".",
            1
        )[-1].lower()

        allowed_extensions = app.config.get(
            "ALLOWED_PROFILE_EXTENSIONS",
            set()
        )

        if extension not in allowed_extensions:
            flash(
                "Only JPG, JPEG, PNG, and WEBP images are allowed.",
                "error"
            )

            return redirect(
                url_for("admin_profile_picture")
            )

        new_filename = (
            "profile."
            + extension
        )

        file_path = os.path.join(
            PROFILE_UPLOAD_FOLDER,
            new_filename
        )

        file.save(file_path)

        setting.profile_image = (
            "uploads/profile/"
            + new_filename
        )

        db.session.commit()

        flash(
            "Profile picture updated successfully.",
            "success"
        )

        return redirect(
            url_for("admin_profile_picture")
        )

    return render_template(
        "admin/profile_picture.html",
        setting=setting
    )
# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(debug=True)