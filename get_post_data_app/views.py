# get_post_data_app/views.py
import base64
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SERPResult, SERPTaskPostResult
from .serializers import SERPResultSerializer, SERPTaskPostResultSerializer
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class DataForSEOFetchAndSaveView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        print("Fetching data with user-supplied base URL and task_id")

        # username = request.GET.get('username')
        # password = request.GET.get('password')
        username = request.user.email
        password = request.user.seo_api_token
        base_url = request.GET.get('url')
        task_id = request.GET.get('task_id')

        if not username or not password:
            return Response(
                {"error": "Missing 'username' or 'password' query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not base_url or not task_id:
            return Response(
                {"error": "Missing 'url' or 'task_id' query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        final_url = f"{base_url.rstrip('/')}/{task_id}"
        print(f"Calling DataForSEO URL: {final_url}")

        try:
            api_response = requests.get(final_url, auth=(username, password))
        except Exception as e:
            return Response(
                {"error": "Error while calling DataForSEO", "detail": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        if api_response.status_code == 200:
            data = api_response.json()
 
            return Response(data)

        else:
            return Response(
                {
                    "error": "Failed to fetch data from DataForSEO",
                    "status_code": api_response.status_code,
                    "detail": api_response.text
                },
                status=status.HTTP_400_BAD_REQUEST
            )




class DataForSEOTaskPostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        username = request.user.email
        password = request.user.seo_api_token
        post_url = request.GET.get('url')

        if not username or not password:
            return Response(
                {"error": "Missing 'username' or 'password' query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not post_url:
            return Response(
                {"error": "Missing 'url' query parameter with DataForSEO POST endpoint."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(request.data, list):
            return Response(
                {"error": "Body must be a JSON array with task instructions."},
                status=status.HTTP_400_BAD_REQUEST
            )

        post_data = request.data

        try:
            api_response = requests.post(post_url, auth=(username, password), json=post_data)
            print(f"Called DataForSEO POST URL: {post_url}")
        except Exception as e:
            return Response(
                {"error": "Failed to reach DataForSEO.", "detail": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        if api_response.status_code != 200:
            return Response(
                {"error": "Failed to post task to DataForSEO.", "status_code": api_response.status_code, "detail": api_response.text},
                status=status.HTTP_400_BAD_REQUEST
            )

        response_data = api_response.json()

        try:
            task_id = response_data["tasks"][0]["id"]
        except (KeyError, IndexError):
            task_id = None

        if not task_id:
            return Response(
                {"error": "Task ID not found in DataForSEO response.", "response": response_data},
                status=status.HTTP_400_BAD_REQUEST
            )

 

        request.session['last_task_id'] = task_id

        # result_serializer = SERPTaskPostResultSerializer(result)
        return Response(
            {
                "task_id": task_id,
                "message": "Paste this task Id in get method"
            },
            status=status.HTTP_201_CREATED
        )


