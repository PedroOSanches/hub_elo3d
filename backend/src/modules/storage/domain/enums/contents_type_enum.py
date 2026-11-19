from enum import StrEnum


class ContentTypeEnum(StrEnum):

    APPLICATION_PDF = "application/pdf"
    APPLICATION_STEP = "application/step"
    APPLICATION_OCTET_STREAM = "application/octet-stream"
    APPLICATION_X_AMF = "application/x-amf"
    APPLICATION_ZIP = "application/zip"

    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"

    MODEL_STL = 'model/stl'
    MODEL_OBJ = "model/obj"
    MODEL_3MF = "model/3mf"
    MODEL_PLY = "model/ply"

    TEXT_X_GCODE = "text/x.gcode"
    TEXT_PLAIN = "text/plain"