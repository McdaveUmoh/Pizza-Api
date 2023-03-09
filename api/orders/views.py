from flask_restx import Namespace, Resource, fields
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
 

order_namespace = Namespace('orders', description='name space for Order')

order_model = order_namespace.model(
    'Order',{
        'id': fields.Integer(description="An ID"),
        'size': fields.String(description="Size of Order", required=True,
            enum = ['SMALL','MEDIUM','LARGE','EXTRA_LARGE']                
        ),
        'order_status': fields.String(description='The Status of our Order', required=True,
            enum = ['PENDING', 'IN_TRANSIT', 'DELIVERED']
        ),
        'flavour': fields.String(description='Type of Pizza Flavour', required=True),
        'quantity': fields.String(description='Quantity of Pizza', required=True),
    }
)

@order_namespace.route("/orders")
class OrderGetCreate(Resource):
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self):
        """
            Get all orders
        """
        orders = Order.query.all()
        
        return orders, HTTPStatus.OK
    
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
            place an order
        """
        
        username = get_jwt_identity()
        
        current_user = User.query.filter_by(username=username).first()
        
        data = order_namespace.payload
        
        new_order = Order(
            size =  data['size'],
            quantity = data['quantity'],
            flavour = data['flavour']
        )
        
        #yours might be new_order.customer
        new_order.user = current_user
        
        new_order.save()
        
        return new_order, HTTPStatus.CREATED
    
@order_namespace.route("/order/<int:order_id>")
class GetUpdateDelete(Resource):
    
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self, order_id):
        """
            Get an order by Id
        """
        order = Order.get_by_id(order_id)
        
        return order, HTTPStatus.OK
    
    def put(self, order_id):
        """
            Put an order by Id
        """
        pass
    
    def delete(self, order_id):
        """
            Delete an order by Id
        """
        pass
    
@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    def get(self, user_id, order_id):
        """
            Get a user specific order
        """
        pass

@order_namespace.route('/user/<int:user_id>/order')
class GetUserOrder(Resource):
    def get(self):
        """
            Get all user Order
        """
        pass

@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    
    def patch(self, order_id):
        """
            Update an Order's status
        """
        pass