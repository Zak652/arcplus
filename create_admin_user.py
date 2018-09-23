import os
from arm import app
from arm import models
from arm.database import session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import utils

def createUser():
    #Create Admin role
    Admin = models.Role(name = 'Admin', description = 'Administrative users')
    session.add(Admin)
    session.commit()
    # Create User role
    User = models.Role(name = 'End-user', description = 'Front-end users')
    session.add(User)
    session.commit()

    #Create Super Admin user
    # tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))

    #Create admin user
    adminUser = models.User(username = 'Admin', email = 'admin@example.com', password = 'password5678', active = True)
    session.add(adminUser)
    Admin.user.append(adminUser)
    session.commit()
    #Create front-end user
    arcUser = models.User(username = 'User', email = 'user@example.com', password = 'password1234', active = True)
    session.add(arcUser)
    User.user.append(arcUser)
    session.commit()

if __name__ == '__main__':
    createUser()