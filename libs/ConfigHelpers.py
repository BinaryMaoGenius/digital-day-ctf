import hashlib
import filetype
import logging
from base64 import b64decode
from datetime import datetime

from past.builtins import basestring
from tornado.options import options

from libs.ValidationError import ValidationError
from libs.XSSImageCheck import is_xss_image


def save_config():
    logging.info("Saving current config to: %s" % options.config)
    with open(options.config, "w", encoding="utf-8") as fp:
        fp.write("##########################")
        fp.write(" Root the Box Config File ")
        fp.write("##########################\n")
        fp.write(
            "# Documentation: %s\n"
            % "https://github.com/moloch--/RootTheBox/wiki/Configuration-File-Details"
        )
        fp.write("# Last updated: %s\n" % datetime.now())
        for group in options.groups():
            # Shitty work around for Tornado 4.1
            if "rootthebox.py" in group.lower() or group == "":
                continue
            fp.write("\n# [ %s ]\n" % group.title())
            opt = list(options.group_dict(group).items())
            for key, value in opt:
                try:
                    # python2
                    value_type = basestring
                except NameError:
                    # python 3
                    value_type = str
                if isinstance(value, value_type):
                    # Str/Unicode needs to have quotes
                    fp.write('%s = "%s"\n' % (key, value))
                else:
                    # Int/Bool/List use __str__
                    fp.write("%s = %s\n" % (key, value))


def save_config_image(b64_data):
    image_data = bytearray(b64decode(b64_data))
    if len(image_data) < (2048 * 2048):
        kind = filetype.guess(image_data)
        if kind is None:
            raise ValidationError("Invalid image format")
        ext = kind.extension
        file_name = "/story/%s.%s" % (hashlib.sha1(image_data).hexdigest(), ext)
        if ext in ["png", "jpg", "jpeg", "gif", "bmp"] and not is_xss_image(image_data):
            with open("files" + file_name, "wb") as fp:
                fp.write(image_data)
            return file_name
        else:
            raise ValidationError(
                "Invalid image format, avatar must be: .png .jpeg .gif or .bmp"
            )
    else:
        raise ValidationError("The image is too large")


def create_demo_user():
    from models import dbsession
    from models.GameLevel import GameLevel
    from models.Team import Team
    from models.User import User

    if Team.by_name("player") is None:
        user = User()
        user.handle = "player"
        user.password = "rootthebox"
        user.name = "player"
        user.email = "player@rootthebox.com"
        team = Team()
        team.name = "player"
        team.motto = "Don't hate the player"
        team.set_score("start", 0)
        team.game_levels.append(GameLevel.all()[0])
        team.members.append(user)
        dbsession.add(user)
        dbsession.add(team)
        dbsession.commit()
