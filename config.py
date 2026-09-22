import os


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-change-later"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///portfolio.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # PROFILE IMAGE UPLOAD
    # =========================

    PROFILE_UPLOAD_FOLDER = os.path.join(
        "static",
        "uploads",
        "profile"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ALLOWED_PROFILE_EXTENSIONS = {
        "jpg",
        "jpeg",
        "png",
        "webp"
    }