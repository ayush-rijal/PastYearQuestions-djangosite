from rest_framework import serializers
from .models import Category, Quiz, Question, Choice, QuizSubmission, UserRank

# Serializer for Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # Use this to expose all fields of the Category model

# Serializer for Quiz model
class QuizSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nesting the Category serializer

    class Meta:
        model = Quiz
        fields = '__all__'

# Serializer for Question model
class QuestionSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)  # Nesting the Quiz serializer

    class Meta:
        model = Question
        fields = '__all__'

# Serializer for Choice model
class ChoiceSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)  # Nesting the Question serializer

    class Meta:
        model = Choice
        fields = '__all__'

# Serializer for QuizSubmission model
class QuizSubmissionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Using the user's string representation
    quiz = QuizSerializer(read_only=True)  # Nesting the Quiz serializer

    class Meta:
        model = QuizSubmission
        fields = '__all__'

# Serializer for UserRank model
class UserRankSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Using the user's string representation

    class Meta:
        model = UserRank
        fields = '__all__'
