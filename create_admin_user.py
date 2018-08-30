import os
from arm import app
from arm import models
from arm.database import session
from werkzeug.security import generate_password_hash, check_password_hash

def createUser():
    #Create Admin role
    Admin = models.Role(name = 'Admin', role_desc = 'Role with admin privileges')
    # Create User role
    User = models.Role(name = 'User', role_desc = 'Role with only user privileges')
    session.add(Admin)
    session.add(User)
    session.commit()

    #Create Super Admin user
    adminUser = models.User(username = 'Admin', email = 'admin@admin.com', password = generate_password_hash('password1'))
    #Create normal user
    arcUser = models.User(username = 'User', email = 'user@admin.com', password = generate_password_hash('password2'))
    session.add(adminUser)
    session.add(arcUser)
    Admin.user.append(adminUser)
    User.user.append(arcUser)
    session.commit()

if __name__ == '__main__':
    createUser()