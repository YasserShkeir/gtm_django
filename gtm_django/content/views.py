from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from .models import Content, Language
from .serializers import ContentSerializer, LanguageSerializer, DashBoardRowSerializer


# Separate API
@api_view(["POST"])
def content_list(request):
    language = request.data.get("language")

    if language is None:
        return Response({"error": "Please provide a language"}, status=400)
    
    try:
        language_id = Language.objects.get(name=language)
        contents = Content.objects.filter(language=language_id)
        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data, status=200)
    except Language.DoesNotExist:
        return Response({"error": "Language not found"}, status=404)


# Sign In API
@csrf_exempt
def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            response = HttpResponse("Sign-in successful")
            response.set_cookie(key='auth_token', value=token.key, httponly=True)
            return response
        else:
            return JsonResponse({'message': 'Sign-in failed'}, status=400)
    return render(request, 'sign_in.html')

# Obtain Auth Token API
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


# Dashboard APIs
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def dashboard_content_list(request):
    language = request.data.get("language") or ""
    points = request.data.get("points") or ""
    search_title = request.data.get("search_title") or ""

    page_size = 10
    page = int(request.data.get("page")) or 1
    start = (page - 1) * page_size
    end = page * page_size

    contents = Content.objects.all()

    if language == "" and search_title == "" and points == "":
        serializer = DashBoardRowSerializer(contents[start:end], many=True)
        return Response(serializer.data, status=200)
    
    try:
        if language != "":
            language = Language.objects.get(name=language)
            contents = Content.objects.filter(language=language)
        
        if search_title != "":
            contents = contents.filter(title__icontains=search_title)

        if points != "":
            contents = contents.filter(points=points)

        serializer = DashBoardRowSerializer(contents[start:end], many=True)
        return Response(serializer.data, status=200)
    except Language.DoesNotExist:
        return Response({"error": "Language not found"}, status=404)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def language_list(request):
    languages = Language.objects.all()
    serializer = LanguageSerializer(languages, many=True)
    return Response(serializer.data, status=200)


@csrf_exempt
@permission_classes([IsAuthenticated])
def content_list_view(request):
    return render(request, 'content_list.html')


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_content_view(request):
    title = request.data.get("title")
    text = request.data.get("text")
    language = request.data.get("language")
    points = request.data.get("points")

    if language is None or text is None:
        return Response({"error": "Please provide all required fields"}, status=400)

    id, _ = Language.objects.get_or_create(name=language)

    Content.objects.create(
        title=title,
        text=text,
        language=id,
        points=points,
    )
    return Response({"success": "Content created successfully"}, status=201)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_content(request):
    content_id = request.data.get("id")
    title = request.data.get("title")
    points = request.data.get("points")
    language_name = request.data.get("language")

    try:
        content = Content.objects.get(id=content_id)
        if title:
            content.title = title
        if points:
            content.points = points
        if language_name:
            language, _ = Language.objects.get_or_create(name=language_name)
            content.language = language
        content.save()
        return Response({"success": "Content updated successfully"}, status=200)
    except Content.DoesNotExist as e:
        return Response({"error": "Content not found"}, status=404)
    except Language.DoesNotExist:
        return Response({"error": "Language not found"}, status=404)
