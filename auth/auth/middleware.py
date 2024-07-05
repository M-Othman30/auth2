#middleware.py
import logging
import requests
import jwt
from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model


# logger = logging.getLogger(__name__)

User = get_user_model()

class APIGatewayMiddleware:
    SERVICE_URLS = {
        'car': 'http://34.118.233.250:80/',  
        'garage': 'http://34.118.235.11:80/',
        'rating':'http://34.118.230.18:80/',
        'notification':'http://34.118.235.83:80/',
        'booking':'http://34.118.236.97:80/',
        'invoices':'http://34.118.238.184:80/',
       
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Exclude authentication and authorization checks for specific paths
            if request.path.startswith('/auth/') or request.path == '/token/refresh/':
                return self.get_response(request)    

            # Perform JWT token verification and authorization
            auth_result,token = self.verify_jwt_token(request)
            if not auth_result['success']:
                return self._unauthorized_response(auth_result['message'])
            
            if request.path.startswith('/user/'):
                return self.get_response(request)
            
            # Determine which microservice should handle the request
            microservice_url = self._get_microservice_url(request)
            response = self.proxy_request(request, microservice_url,token)

            return response
        except Exception as e:
            # logger.exception('Error in API Gateway Middleware: %s', str(e))
            return self._error_response('Internal Server Error')


    def authorize_request(self, request):
        # TODO: Implement authorization logic here
        return True 
    
    def verify_jwt_token(self, request):
        jwt_authentication = JWTAuthentication()
        try:
            user, token = jwt_authentication.authenticate(request)
            if not user or not token:
                raise AuthenticationFailed('Invalid token')
            # Log successful token verification
            # logger.info('JWT Token Verification Successful')

            return {'success': True, 'message': 'Authentication successful'},str(token)
        except AuthenticationFailed as e:
            # Log token authentication failure
            # logger.error('JWT Token Verification Failed: %s', str(e))
            return {'success': False, 'message': str(e) }

    def _get_microservice_url(self, request):
        # Determine the microservice URL based on the request path
        path_components = request.path.split('/')
        if len(path_components) >= 2:
            microservice_name = path_components[1].lower()
            if microservice_name in self.SERVICE_URLS:
                return self.SERVICE_URLS[microservice_name]

        return 'http://127.0.0.1:8000'  # Default fallback service URL

    def proxy_request(self, request, microservice_url,jwt_token):

        # Log the JWT token before sending the proxy request
        # logger.debug('JWT Token in Request Headers: %s', jwt_token)

        # Proxy the request to the microservice with the JWT token included
        # Decode the jwt token and Extract user id from token
        decoded_token = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["HS256"])
        user_id = decoded_token['user_id']
        userData= User.objects.get(pk=user_id)
        try:
           response = requests.request(
               method=request.method,
               url=microservice_url + request.path,
               data=request.body,
               headers={
                   'Content-Type': 'application/json',
                   'userId': str(user_id),
                   'userType': userData.user_type,
               },
               params=request.GET,
               cookies=request.COOKIES,
               allow_redirects=False
           )
           response.raise_for_status()
        except requests.RequestException as e:
            # logger.error('Microservice Proxy Request Error: %s', str(e))
            return self._error_response('Microservice Error: ' + str(e))

        # Log the microservice response status code and headers
        # logger.debug('Microservice Response Status Code: %s', response.status_code)
        # logger.debug('Microservice Response Headers: %s', response.headers)

        # Process the response from the microservice
        django_response = HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type')
        )

        return django_response

    def _unauthorized_response(self, message):
        return HttpResponse(message, status=401)

    def _error_response(self, message):
        return HttpResponse(message, status=500)
