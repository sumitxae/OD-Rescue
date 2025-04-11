from enum import Enum

class Roles(Enum):
    FFF_ADMIN = "fff_admin"
    GLOBAL_ADMIN = "global_level_admin"
    SITE_ADMIN = "site_level_admin"

    def __str__(self):
        return self.value