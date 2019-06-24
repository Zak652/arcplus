from . import app, models
from .database import session
from flask import url_for, redirect, request, abort
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user,utils
from wtforms.fields import PasswordField

class UserAdmin(ModelView):
    #Remove user delete option
    can_delete = False
    
    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password', 'login_count', 'confirmed_at', 'last_login_at', 'current_login_at', 'last_login_ip', 'current_login_ip')

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has the "Admin" role
    def is_accessible(self):
        # return current_user.has_role('Admin')
        if not current_user.is_authenticated or not current_user.has_role('Admin'):
            return redirect(url_for('logout'))
        return True
    
    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):

            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = utils.encrypt_password(model.password2)

# Customized Role model for SQL-Admin
class RoleAdmin(ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "Admin" role
    def is_accessible(self):
        if not current_user.is_authenticated or not current_user.has_role('Admin'):
            return redirect(url_for('logout'))
        return True


class PeopleAdmin(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ('person_code', 'first_name', 'last_name', 'designation', 'phone', 'email',
                    'notes', 'user_department', 'user_location')
    
    # Prevent administration of Roles unless the currently logged-in user has the "Admin" role
    def is_accessible(self):
        if not current_user.is_authenticated or not current_user.has_role('Admin'):
            return redirect(url_for('logout'))
        return True

class AssetsAdmin(ModelView):
    can_create = False
    can_edit = True
    can_delete = True
    column_list = ('barcode', 'asset_type', 'serial_no', 'asset_status', 
                                'asset_category', 'asset_type', 'asset_model')
    
    # Prevent administration of Roles unless the currently logged-in user has the "Admin" role
    def is_accessible(self):
        if not current_user.is_authenticated or not current_user.has_role('Admin'):
            return redirect(url_for('logout'))
        return True

class CategoriesAdmin(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    
    # Prevent administration of Roles unless the currently logged-in user has the "Admin" role
    def is_accessible(self):
        if not current_user.is_authenticated or not current_user.has_role('Admin'):
            return redirect(url_for('logout'))
        return True

class TypesAdmin(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    
    # Prevent administration of Roles unless the currently logged-in user has the "Admin" role
    def is_accessible(self):
        if not current_user.is_authenticated or not current_user.has_role('Admin'):
            return redirect(url_for('logout'))
        return True

class ModelsAdmin(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    
    # Prevent administration of Roles unless the currently logged-in user has the "Admin" role
    def is_accessible(self):
        if not current_user.is_authenticated or not current_user.has_role('Admin'):
            return redirect(url_for('logout'))
        return True

class DashboardView(ModelView):
    
    # Prevent administration of Roles unless the currently logged-in user has the "Admin" role
    def is_accessible(self):
        if not current_user.is_authenticated or not current_user.has_role('Admin'):
            return redirect(url_for('logout'))
        return True

admin = Admin(app, name='Admin', template_mode='bootstrap3')
admin.add_view(UserAdmin(models.User, session, category='Users & Roles', name='Users', endpoint='users'))
admin.add_view(RoleAdmin(models.Role, session, category='Users & Roles', name='User Roles', endpoint='user_roles'))
admin.add_view(PeopleAdmin(models.People, session, category='Tracking', name='People', endpoint='people'))
admin.add_view(ModelsAdmin(models.Location, session, category='Tracking', name='Location', endpoint='location'))
admin.add_view(AssetsAdmin(models.Asset, session, category='Register', name='Assets', endpoint='assets'))
admin.add_view(CategoriesAdmin(models.AssetCategory, session, category='Properties', name='Categories', endpoint='categories'))
admin.add_view(TypesAdmin(models.AssetType, session, category='Properties', name='Types', endpoint='types'))
admin.add_view(ModelsAdmin(models.AssetModel, session, category='Properties', name='Models', endpoint='models'))
admin.add_view(ModelsAdmin(models.CostCenter, session, category='Cost Centers', name='Cost Centers', endpoint='cost_centers'))
admin.add_view(ModelsAdmin(models.Department, session, category='Cost Centers', name='Department', endpoint='department'))
admin.add_view(ModelsAdmin(models.AssetStatus, session, category='Register', name='Status', endpoint='status'))
admin.add_view(ModelsAdmin(models.AssetCondition, session, category='Register', name='Condition', endpoint='condition'))
admin.add_view(ModelsAdmin(models.Supplier, session, category='Suppliers', name='Suppliers', endpoint='suppliers'))
admin.add_view(ModelsAdmin(models.SupplierCategory, session, category='Suppliers', name='Supplier Category', endpoint='supplier_category'))
