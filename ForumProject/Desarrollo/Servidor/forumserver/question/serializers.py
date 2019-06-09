""" Serializers for question app """
from forumserver import settings
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, DateTimeField
from drf_extra_fields.fields import Base64ImageField
from start.serializers import PersonSerializer
from question.models import (
    Question, QuestionImage, Answer, Tag,
    QuestionTag, QuestionPersonLike)


class TagSerializer(ModelSerializer):
    """ Serializer for Tag model """

    class Meta:
        """ Meta class for tag serializer """
        model = Tag
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True, 'required': False}}


class QuestionSerializer(ModelSerializer):
    """ Serializer for Question model """
    image_question = SerializerMethodField()
    tags = SerializerMethodField()
    likes = SerializerMethodField()
    dislikes = SerializerMethodField()
    has_like = SerializerMethodField()
    creation_date = DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        """ Meta class for question serializer """
        model = Question
        fields = ['id', 'creator', 'title', 'statement', 'creation_date',
                  'image_question', 'tags', 'likes', 'dislikes', 'has_like']
        extra_kwargs = {'id': {'read_only': True, 'required': False}}

    def __init__(self, *args, **kwargs):
        super(QuestionSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
            self.fields['creator'] = PersonSerializer(read_only=True,
                                                      context=kwargs['context'])
        if self.context['request'].method == 'PATCH':
            self.fields['creator'] = PersonSerializer(context=kwargs['context'])

    def create(self, validated_data):
        """ Create method for the serializer """
        question = Question.objects.create(**validated_data)
        question.save()
        if 'tag' in self.context['request'].data:
            tag = Tag.objects.get(id=self.context['request'].data['tag'])
            question_tag = QuestionTag.objects.create(question=question,
                                                      tag=tag)
            question_tag.save()
        return question

    def get_image_question(self, obj):
        """ Method to obtain an image for a question """
        question_image = 'Sin imagen'
        if QuestionImage.objects.filter(question=obj).exists():
            question_image = (QuestionImage.objects.filter(question=obj)
                              .order_by('-upload_date').first())
            question_image = (settings.IMAGE_HOST + question_image.image.url)
        return question_image

    def get_tags(self, obj):
        """ Method to obtain a list of tags associated of a question """
        if QuestionTag.objects.filter(question=obj).exists():
            id_tags = QuestionTag.objects.filter(question=obj).values('tag__id')
            tags_obj = Tag.objects.filter(id__in=id_tags)
            return TagSerializer(tags_obj, many=True).data
        else:
            return "No tags"

    def get_likes(self, obj):
        """ Method to obtain likes for a question """
        return QuestionPersonLike.objects.filter(question=obj,
                                                 like=True).count()

    def get_dislikes(self, obj):
        """ Method to obtain dislikes for a question """
        return QuestionPersonLike.objects.filter(question=obj,
                                                 like=False).count()

    def get_has_like(self, obj):
        """ Method to know if a person liked a question """
        if 'person_id' in self.context['request'].GET:
            if (QuestionPersonLike.objects
                .filter(person__id=self.context['request'].GET['person_id'],
                        question=obj).exists()):
                return (QuestionPersonLike.objects
                        .filter(person__id=self.context['request']
                                .GET['person_id'],
                                question=obj)
                        .last().id)
        return 0


class QuestionImageSerializer(ModelSerializer):
    """ Serializer for Image of user profiles """
    image = Base64ImageField()
    url_image = SerializerMethodField()
    upload_date = DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    extra_kwargs = {'id': {'read_only': True, 'required': False}}

    def to_representation(self, obj):
        ret = super(QuestionImageSerializer, self).to_representation(obj)
        if self.context['request'].method == 'POST':
            ret.pop('id')
            ret.pop('question')
            ret.pop('image')
            ret.pop('upload_date')
        return ret

    class Meta:
        """ Meta class for ImageDetail serializer """
        model = QuestionImage
        fields = '__all__'

    def update(self, instance, validated_data):
        """ Function to update user information """
        instance.image.delete(save=False)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    def get_url_image(self, obj):
        """ Function to obtain the url for an image """
        return settings.SERVER_HOST + obj.image.url


class AnswerSerializer(ModelSerializer):
    """ Serializer for Answer model """
    creation_date = DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        """ Meta class for answer serializer """
        model = Answer
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True, 'required': False}}

    def __init__(self, *args, **kwargs):
        super(AnswerSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
            self.fields['creator'] = PersonSerializer(read_only=True,
                                                      context=kwargs['context'])
            self.fields['question'] = QuestionSerializer(read_only=True,
                                                         context=kwargs
                                                         ['context'])
        if self.context['request'].method == 'PATCH':
            self.fields['creator'] = PersonSerializer(context=kwargs['context'])
            self.fields['question'] = QuestionSerializer(context=kwargs
                                                         ['context'])


class QuestionTagSerializer(ModelSerializer):
    """ Serializer for QuestionTag model """

    class Meta:
        """ Meta class for question tag serializer """
        model = QuestionTag
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True, 'required': False}}

    def __init__(self, *args, **kwargs):
        super(QuestionTagSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
            self.fields['tag'] = TagSerializer(read_only=True,
                                               context=kwargs['context'])
            self.fields['question'] = QuestionSerializer(read_only=True,
                                                         context=kwargs
                                                         ['context'])


class QuestionPersonLikeSerializer(ModelSerializer):
    """ Serializer for likes of persons """

    class Meta:
        """ Meta class for the serializer """
        model = QuestionPersonLike
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True, 'required': False}}

    def __init__(self, *args, **kwargs):
        super(QuestionPersonLikeSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
            self.fields['person'] = PersonSerializer(read_only=True,
                                                     context=kwargs['context'])
            self.fields['question'] = QuestionSerializer(read_only=True,
                                                         context=kwargs
                                                         ['context'])
