from . import confirm_handlers, handlers, template_handler
import os

labelers = [confirm_handlers.bl,template_handler.bl, handlers.bl]

if not os.path.isdir(f"archive") or not os.path.isdir(f"attachments"):
    os.mkdir(f"archive")
    os.mkdir("attachments")
