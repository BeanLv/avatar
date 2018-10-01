from application.blueprint import rests


@rests.route('/orders')
def get_orders():
    return 'You get orders'
