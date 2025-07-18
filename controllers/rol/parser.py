from flask_restful import reqparse
import re

class RolParser:
    @staticmethod
    def parse_put_request():
        parser = reqparse.RequestParser()

        parser.add_argument('_id', type=str, required=False, help="ID of the lost object is required")
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('description', type=str, required=False)
        parser.add_argument('permissions', type=list,location='json', required=False)
        parser.add_argument('creation_date', type=str, required=False)
        parser.add_argument('mod_date', type=str, required=False)
        parser.add_argument('is_active', type=str, required=False)
        parser.add_argument('default_role', type=list, location='json', required=False)
        parser.add_argument('screens', type=str, required=False),
        parser.add_argument('app', type=str, required=False),

        args = parser.parse_args()

        # Validate permissions if provided
        if args['permissions']:
            for sk in args['permissions']:
                if not isinstance(sk, dict):
                    parser.error(f'permissions not provided')

        return args

