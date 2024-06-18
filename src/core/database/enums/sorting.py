import enum


class OrderBY(enum.StrEnum):
    DESC = "desc"
    ASC = "asc"


class SortBY(enum.StrEnum):
    ID = ("id",)
    NAME = ("name",)
    SURNAME = ("surname",)
    USERNAME = ("username",)
    ROLE = ("role",)
    IMAGE_S3_PATH = ("image_s3_path",)
    IS_BLOCKED = ("is_blocked",)
    EMAIL = ("email",)
    PHONE_NUMBER = ("phone_number",)
    GROUP_ID = ("group_id",)
