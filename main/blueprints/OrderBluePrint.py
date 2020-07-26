from flask import Blueprint, request, abort, g, jsonify
from main import db
from main import Order, User, Restaurant
from werkzeug.exceptions import NotFound
from main.helpers.common import without_keys, only_keys
from main.blueprints.AuthBluePrint import login_required
from smalluuid import SmallUUID
import datetime

blueprint = Blueprint('order', __name__)


@blueprint.route('', methods=['GET', 'POST'])
@login_required()
def orders():
    if request.method == 'GET':
        try:
            # get current user
            current_user = g.get('user', None)
            # print('----------------', current_user.id)
            # query
            q = Order.query
            q = q.filter_by(user_id=current_user.id)
            # order
            q = q.order_by(Order.ordered_at.desc())
            # orders
            orders = q.all()

            order_list = [order.to_json() for order in orders]

            refactor_dict = dict()
            for order_dict in order_list:
                order_dict.get('code')
                if not refactor_dict.get(order_dict.get('code')):
                    refactor_dict[order_dict.get('code')] = []
                refactor_dict[order_dict.get('code')].append(order_dict)

            refactor_list = []
            for code in refactor_dict:
                order_item_list = refactor_dict.get(code, [])
                order_place = ''
                if len(order_item_list) > 0:
                    order_place = order_item_list[0].get('order_place', '')
                refactor_list.append({
                    'code': code,
                    'order_place': order_place,
                    'order': refactor_dict.get(code, [])
                })

            return jsonify({'orders': refactor_list}), 200
        except NotFound as e:
            return jsonify(orders.response), 200
        except Exception as e:
            return abort(500, e)

    if request.method == 'POST':
        try:
            keys = ['amount', 'note']
            data = request.get_json()
            order_req_list = data.get('orders', None)
            order_place = data.get('order_place', None)

            # get current user
            current_user = g.get('user', None)

            # add orders model to a list
            if (order_req_list and type(order_req_list) == list):
                # make same order_code in list of order for group by later
                today_str = str(datetime.date.today().isoformat())
                order_code = f'{today_str}/{SmallUUID()}'
                for order_req in order_req_list:
                    order = Order(**only_keys(order_req, *keys))
                    order.order_place = order_place
                    order.code = order_code
                    order.ordered_at = datetime.datetime.utcnow()

                    # associate
                    item = Restaurant.query.filter_by(id=order_req.get('item_id', None)).first_or_404()
                    order.item = item
                    current_user.orders.append(order)
                    db.session.add(order)
                db.session.commit()
                return {"message": "order successful"}, 200
            abort(500, {"message": "cannot make order"})
        except Exception as e:
            abort(500, e)
