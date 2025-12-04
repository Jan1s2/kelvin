import io
import shutil
import re


def parse_human_size(txt):
    m = re.match(r"^([0-9]+(\.[0-9]+)?)\s*(K|M|G|T)?B?$", str(txt).strip())
    if not m:
        raise ValueError(f"Invalid size: {txt}")

    num = float(m.group(1))
    multipliers = ["K", "M", "G", "T"]

    mult = 1
    if m.group(3):
        mult = 2 ** (10 * (1 + multipliers.index(m.group(3))))

    return int(num * mult)


def copyfile(src, dst):
    if isinstance(src, io.BytesIO):
        with open(dst, "wb") as f:
            f.write(src.getvalue())
    else:
        shutil.copyfile(src, dst)


def generate_identification(meta):
    login = meta.get("login")
    if login is None:
        return None
    timestamp = meta.get("submitted_at")
    if timestamp is None:
        return None
    timestamp = timestamp.timestamp()
    return {"id": f"{login}-{timestamp}"}
