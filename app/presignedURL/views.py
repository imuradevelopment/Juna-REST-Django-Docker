import boto3
from rest_framework.views import APIView
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# Create your views here.
class PresignedURLView(APIView):
    # aws_access_key_id = 'YOUR_KEY'
    # aws_secret_access_key = 'YOUR_SECRET'
    BUCKET = 'juna-bucket'
    permission_classes = [IsAuthenticated]
    bad_request_message = 'An error has occurred'

    def get(self, request):
        if "content_type" in request.GET and "file_hash" in request.GET:
            KEY = str(request.user.id) + '/' + request.GET.get("file_hash")
            CONTENTTYPE = request.GET.get("content_type")
        else:
            return response.Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)

        boto3.session.Session(profile_name='dev')
        s3 = boto3.client(
            's3',
            endpoint_url = 'https://s3.ap-northeast-1.wasabisys.com',
            # aws_access_key_id=aws_access_key_id,
            # aws_secret_access_key=aws_secret_access_key
        )
        presingedURL = s3.generate_presigned_url(
            ClientMethod = 'put_object',
            Params = {'Bucket' : self.BUCKET, 'Key' : KEY, 'ContentType' : CONTENTTYPE},
            ExpiresIn = 300,
            HttpMethod = 'PUT'
        )
        return response.Response({'presingedURL': presingedURL}, status=status.HTTP_200_OK)

    def post(self, request):
        if "key" in request.data and "content_type" in request.data:
            KEY = request.data.get("key")
            CONTENTTYPE = request.data.get("content_type")
        else:
            return response.Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)

        boto3.session.Session(profile_name='dev')
        s3 = boto3.client(
            's3',
            endpoint_url = 'https://s3.ap-northeast-1.wasabisys.com',
            # aws_access_key_id=aws_access_key_id,
            # aws_secret_access_key=aws_secret_access_key
        )
        presingedURL = s3.generate_presigned_url(
            ClientMethod = 'put_object',
            Params = {'Bucket' : self.BUCKET, 'Key' : KEY, 'ContentType' : CONTENTTYPE},
            ExpiresIn = 3000,
            HttpMethod = 'PUT'
        )
        return response.Response(
            {
                'method': 'PUT',
                'url': presingedURL,
                'fields': [],
                'headers': {'content-type': CONTENTTYPE},
            },
            status=status.HTTP_200_OK)

    def delete(self, request):
        return response.Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)
