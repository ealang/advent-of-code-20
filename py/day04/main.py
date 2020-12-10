import re
from typing import NamedTuple, Optional


class PassportFields(NamedTuple):
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str


def parse_passport(passport_text: str) -> Optional[PassportFields]:
    def extract(fname: str) -> str:
        match = re.search(fr"{fname}:(.*?)($|\s)", passport_text)
        if match is None:
            raise ValueError()
        return match.group(1)
    try:
        return PassportFields(
            byr=extract("byr"),
            iyr=extract("iyr"),
            eyr=extract("eyr"),
            hgt=extract("hgt"),
            hcl=extract("hcl"),
            ecl=extract("ecl"),
            pid=extract("pid"),
        )
    except ValueError:
        return None


EYE_COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def passport_is_valid(passport: PassportFields) -> bool:
    def validate_byr():
        val = int(passport.byr)
        return 1920 <= val <= 2002

    def validate_iyr():
        val = int(passport.iyr)
        return 2010 <= val <= 2020

    def validate_eyr():
        val = int(passport.eyr)
        return 2020 <= val <= 2030

    def validate_hgt():
        match = re.match(r"^(\d+)(cm|in)$", passport.hgt)
        if match is None:
            return False

        val, unit = match.groups()
        val = int(val)
        if unit == "cm":
            return 150 <= val <= 193
        if unit == "in":
            return 59 <= val <= 76
        return False

    def validate_hcl():
        return re.match(r"^#[a-f0-9]{6}$", passport.hcl) is not None

    def validate_ecl():
        return passport.ecl in EYE_COLORS

    def validate_pid():
        return re.match(r"^\d{9}$", passport.pid) is not None

    return (
        validate_byr() and
        validate_iyr() and
        validate_eyr() and
        validate_hgt() and
        validate_hcl() and
        validate_ecl() and
        validate_pid()
    )


with open("input.txt") as fp:
    passports = [
        passport
        for passport in map(parse_passport, fp.read().split("\n\n"))
        if passport is not None
    ]

valid_passports = list(filter(passport_is_valid, passports))

print(len(passports))
print(len(valid_passports))
