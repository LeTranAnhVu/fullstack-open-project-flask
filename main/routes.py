from main import app

from main.blueprints.RestaurantBluePrint import blueprint as restaurant_blueprint
from main.blueprints.TagBluePrint import blueprint as tag_blueprint
from main.blueprints.FileBluePrint import blueprint as file_blueprint
from main.blueprints.ErrorBluePrint import blueprint as error_blueprint
from main.blueprints.SeedBluePrint import blueprint as seed_blueprint
from main.blueprints.OrderBluePrint import blueprint as order_blueprint
from main.blueprints.AuthBluePrint import blueprint as auth_blueprint
from main.blueprints.admin.AdminAuthBluePrint import blueprint as admin_auth_blueprint
from main.blueprints.admin.AdminBluePrint import blueprint as admin_blueprint
from main.blueprints.admin.RoleBluePrint import blueprint as role_blueprint

#auth
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

#admin auth
app.register_blueprint(admin_auth_blueprint, url_prefix='/api/admin/auth')

#CRUD admin
app.register_blueprint(admin_blueprint, url_prefix='/api/admin/manage/admins')

#CRUD role
app.register_blueprint(role_blueprint, url_prefix='/api/admin/manage/roles')

# seed api
app.register_blueprint(seed_blueprint, url_prefix='/api/seed')

# CURD restaurants
app.register_blueprint(restaurant_blueprint, url_prefix='/api/restaurants')

# CRUD tags
app.register_blueprint(tag_blueprint, url_prefix='/api/tags')

# CRUD files
app.register_blueprint(file_blueprint, url_prefix='/api')

# CRUD orders
app.register_blueprint(order_blueprint, url_prefix='/api/orders')

# error handler
app.register_blueprint(error_blueprint, url_prefix='/api')
