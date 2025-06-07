from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Song, Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

@api_view(['GET'])
def api_root(request):
    songs = Song.objects.all()
    serializer = SongSerializer(songs, many=True)
    return Response({
        "message": "Welcome to VerseVault API!",
        "songs": serializer.data
    })


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=201)
        return Response(serializer.errors, status=400)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
        })


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'name', 'artist', 'album', 'genre', 'date', 'link']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    song_name = serializers.CharField(source='song.name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'song', 'song_name', 'user', 'text', 'date']


class CommentView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk=None):
        if pk:
            try:
                comment = Comment.objects.get(pk=pk)
            except Comment.DoesNotExist:
                return Response({"detail": "Not found."}, status=404)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            comments = Comment.objects.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk, user=request.user)
        except Comment.DoesNotExist:
            return Response({"detail": "Not found or not allowed."}, status=404)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk, user=request.user)
        except Comment.DoesNotExist:
            return Response({"detail": "Not found or not allowed."}, status=404)
        comment.delete()
        return Response(status=204)


@login_required
def homepage(request):
    songs = Song.objects.select_related('artist', 'album').all()
    comments = Comment.objects.select_related('user', 'song').all()
    return render(request, 'homepage.html', {
        'songs': songs,
        'comments': comments,
        'user': request.user,
    })


@require_POST
@login_required
def add_comment(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    text = request.POST.get('text')
    date = request.POST.get('date')
    if text and date:
        Comment.objects.create(song=song, user=request.user, text=text, date=date)
    return redirect('homepage')


@require_POST
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    text = request.POST.get('text')
    date = request.POST.get('date')
    if text and date:
        comment.text = text
        comment.date = date
        comment.save()
    return redirect('homepage')


@require_POST
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return redirect('homepage')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


class RegisterFormView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class SongDetailView(DetailView):
    model = Song
    template_name = 'song_detail.html'
    context_object_name = 'song'
