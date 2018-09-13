from . import app, models
from .database import session
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_user import current_user, login_required, roles_required, UserManager, SQLAlchemyAdapter

class UsersView(ModelView):
    can_create = False
    can_edit = False
    column_list = ('username', 'email')
    def is_accessible(self):
        return super().is_accessible()

class RolesView(ModelView):
    can_create = False
    def is_accessible(self):
        return super().is_accessible()

class PeopleView(ModelView):
    can_create = False
    column_list = ('person_code', 'first_name', 'last_name', 'designation', 'phone', 'email',
                    'notes', 'user_department', 'user_location')
    def is_accessible(self):
        return super().is_accessible()

class AssetsView(ModelView):
    can_create = False
    can_edit = False
    column_list = ('barcode', 'asset_type', 'serial_no', 'asset_status', 
                                'asset_category', 'asset_type', 'asset_model')
    def is_accessible(self):
        return super().is_accessible()

class CategoriesView(ModelView):
    can_create = False
    can_edit = False
    def is_accessible(self):
        return super().is_accessible()

class TypesView(ModelView):
    can_create = False
    can_edit = False
    def is_accessible(self):
        return super().is_accessible()

class ModelsView(ModelView):
    can_create = False
    can_edit = False
    def is_accessible(self):
        return super().is_accessible()

class DashboardView(ModelView):
    def is_accessible(self):
        return super().is_accessible()

admin = Admin(app, name='Admin', template_mode='bootstrap3')
admin.add_view(UsersView(models.User, session, name='Users', endpoint='users'))
admin.add_view(ModelView(models.Role, session, name='User Roles', endpoint='user_roles'))
admin.add_view(PeopleView(models.People, session, name='People', endpoint='people'))
admin.add_view(AssetsView(models.Asset, session, name='Assets', endpoint='assets'))
admin.add_view(CategoriesView(models.AssetCategory, session, name='Categories', endpoint='categories'))
admin.add_view(TypesView(models.AssetType, session, name='Types', endpoint='types'))
admin.add_view(ModelsView(models.AssetModel, session, name='Models', endpoint='models'))
admin.add_view(ModelView(models.CostCenter, session))
# admin.add_view(DashboardView(models, session, name='Dashboard', url='/register/view'))
