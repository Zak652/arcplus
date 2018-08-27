import os
from arm import app
from arm import models
from arm.database import session
from werkzeug.security import generate_password_hash, check_password_hash

def createUser():
    #Create Admin role
    adminRole = models.Role(name = 'Admin', role_desc = 'Role with admin privileges')
    session.add(adminRole)
    session.commit()

    #Create Super Admin user
    adminUser = models.User(name = 'Superadmin', email = 'admin@admin.com', role_id = 1, password = generate_password_hash('arcplusadmin'))
    session.add(adminUser)
    session.commit()

if __name__ == '__main__':
    createUser()