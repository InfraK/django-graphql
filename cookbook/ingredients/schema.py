import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from cookbook.ingredients.models import Category, Ingredient


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ["name", "ingredients"]
        interfaces = (relay.Node,)


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "notes": ["exact", "icontains"],
            "category": ["exact"],
            "category__name": ["exact"],
        }
        interfaces = (relay.Node,)


class IngredientMutation(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        id = graphene.ID()

    ingredient = graphene.Field(IngredientNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, name, id):
        ingredient = Ingredient.objects.get(pk=from_global_id(id)[1])
        ingredient.name = name
        ingredient.save()

        return IngredientMutation(ingredient=ingredient)


class Query(graphene.ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)


class Mutation(graphene.ObjectType):
    update_ingredient = IngredientMutation.Field()
