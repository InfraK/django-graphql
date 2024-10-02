import graphene

import cookbook.ingredients.schema


class Query(cookbook.ingredients.schema.Query, graphene.ObjectType):
    pass


class Mutation(cookbook.ingredients.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

