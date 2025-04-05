from enum import Enum

class TableNames(Enum):
    USER = 'users'
    ROLE = 'roles'
    
    def __str__(self):
        return self.value
    