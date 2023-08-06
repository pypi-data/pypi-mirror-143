from typing import AsyncIterator, Optional
from graphql import (
    GraphQLSchema,
    build_ast_schema,
    build_client_schema,
    get_introspection_query,
    validate,
)
from graphql.language.parser import parse
from pydantic import root_validator
from rath.links.base import ContinuationLink
from rath.links.errors import ContinuationLinkError
from rath.operation import GraphQLResult, Operation, opify
from glob import glob


def schemify(
    schema_dsl: str = None, schema_glob: str = None, schema_url: str = None
) -> GraphQLSchema:
    if schema_dsl:
        return build_ast_schema(parse(schema_dsl))
    if schema_glob:
        files = glob(schema_glob, recursive=True)
        dsl_string = ""
        for file in files:
            with open(file, "r") as f:
                if file.endswith(".graphql"):
                    dsl_string += f.read()

        assert dsl_string, f"No schema found in glob {schema_glob}"
        return build_ast_schema(parse(dsl_string))

    raise NotImplementedError("Please provide either a dsl or glob")


class ValidationError(ContinuationLinkError):
    pass


class ValidatingLink(ContinuationLink):
    schema_dsl: Optional[str] = None
    schema_glob: Optional[str] = None
    allow_introspection: bool = False

    graphql_schema: Optional[GraphQLSchema] = None

    @root_validator(allow_reuse=True)
    def check_schema_dsl_or_schema_glob(cls, values):
        if not values.get("schema_dsl") and not values.get("schema_glob"):
            if not values.get("allow_introspection"):
                raise ValueError(
                    "Please provide either a schema_dsl or schema_glob or allow introspection"
                )

        else:
            values["graphql_schema"] = schemify(
                schema_dsl=values.get("schema_dsl"),
                schema_glob=values.get("schema_glob"),
            )

        return values

        return values

    async def aload_schema(self, operation: Operation) -> None:
        assert self.allow_introspection, "Introspection is not allowed"
        introspect_operation = opify(get_introspection_query())
        introspect_operation.context = operation.context
        introspect_operation.extensions = operation.extensions

        schema_result = await self.next.aquery(introspect_operation)
        self.graphql_schema = build_client_schema(schema_result.data)

    def load_schema(self, operation: Operation) -> None:
        assert self.allow_introspection, "Introspection is not allowed"
        introspect_operation = opify(get_introspection_query())
        introspect_operation.context = operation.context
        introspect_operation.extensions = operation.extensions

        schema_result = self.next.query(introspect_operation)
        self.graphql_schema = build_client_schema(schema_result.data)

    def validate(self, operation: Operation):
        errors = validate(self.graphql_schema, operation.document_node)

        if len(errors) > 0:
            raise ValidationError(
                f"{operation} does not comply with the schema!\n Errors: \n\n"
                + "\n".join([e.message for e in errors])
            )

    async def aquery(self, operation: Operation, **kwargs) -> GraphQLResult:
        if not self.graphql_schema:
            await self.aload_schema(operation)

        self.validate(operation)
        return await self.next.aquery(operation, **kwargs)

    async def asubscribe(
        self, operation: Operation, **kwargs
    ) -> AsyncIterator[GraphQLResult]:
        if not self.graphql_schema:
            await self.aload_schema(operation)

        self.validate(operation)
        async for result in self.next.asubscribe(operation, **kwargs):
            yield result

    def query(self, operation: Operation, **kwargs) -> GraphQLResult:
        if not self.graphql_schema:
            self.load_schema(operation)

        self.validate(operation)
        return self.next.query(operation, **kwargs)

    def subscribe(self, operation: Operation, **kwargs) -> AsyncIterator[GraphQLResult]:
        if not self.graphql_schema:
            self.load_schema(operation)

        self.validate(operation)
        return self.next.subscribe(operation, **kwargs)

    class Config:
        arbitrary_types_allowed = True
