
from flask import Blueprint, request, abort, g
from main import db
from main import Order, User, Restaurant
from main.helpers.common import without_keys
from main.blueprints.AuthBluePrint import login_required
from smalluuid import SmallUUID
import datetime


blueprint = Blueprint('order', __name__)


@blueprint.route('', methods=['GET', 'POST'])
@login_required()
def orders():
    if request.method == 'GET':
        return {'data': []}, 200
    if request.method == 'POST':
        try:
            keys = ['item_id', 'amount', 'note', 'order_place']
            data = request.get_json()
            order = Order(**without_keys(data, 'item_id'))
            
            today_str = str(datetime.date.today().isoformat())

            current_user = g.get('user', None)
            order.code = f'{today_str}/{SmallUUID()}'
            item = Restaurant.query.filter_by(id=data.get('item_id', None)).first_or_404()
            # associate
            order.item = item
            current_user.orders.append(order)
            
            order.code = f'{today_str}/{SmallUUID()}'
            order.ordered_at = datetime.datetime.utcnow()

            db.session.add(order)
            db.session.commit()
        
            return {"message": "order successful"}, 200

        except Exception as e:
            abort(500, e)



    