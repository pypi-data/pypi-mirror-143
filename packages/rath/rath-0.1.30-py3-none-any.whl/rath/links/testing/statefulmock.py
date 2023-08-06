import asyncio
from typing import AsyncIterator, Awaitable, Callable, Dict, Optional

from pydantic import Field
from rath.links.base import AsyncTerminatingLink
from rath.operation import GraphQLResult, Operation
from graphql import FieldNode, OperationType
import uuid
from rath.links.errors import TerminatingLinkError


def target_from_node(node: FieldNode) -> str:
    return (
        node.alias.value if hasattr(node, "alias") and node.alias else node.name.value
    )


class AsyncMockResolver:
    def __getitem__(self, key):
        return getattr(self, f"resolve_{key}")

    def __contains__(self, key):
        return hasattr(self, f"resolve_{key}")
        #


class ConfigurationError(TerminatingLinkError):
    pass


class AsyncStatefulMockLink(AsyncTerminatingLink):
    query_resolver: Dict[str, Callable[[Operation], Awaitable[Dict]]] = Field(
        default_factory=dict, exclude=True
    )
    mutation_resolver: Dict[str, Callable[[Operation], Awaitable[Dict]]] = Field(
        default_factory=dict, exclude=True
    )
    subscription_resolver: Dict[str, Callable[[Operation], Awaitable[Dict]]] = Field(
        default_factory=dict, exclude=True
    )
    resolver: Dict[str, Callable[[Operation], Awaitable[Dict]]] = Field(
        default_factory=dict, exclude=True
    )

    _connected: bool = False
    _futures: Optional[Dict[str, asyncio.Future]] = None
    _inqueue: Optional[asyncio.Queue] = None
    _connection_task: Optional[asyncio.Task] = None

    async def __aenter__(self) -> None:
        self._connected = True
        self._futures = {}
        self._inqueue = asyncio.Queue()
        self._connection_task = asyncio.create_task(self.resolving())

    async def __aexit__(self, *args, **kwargs) -> None:
        self._connected = False
        self._connection_task.cancel()

        try:
            await self._connection_task
        except asyncio.CancelledError:
            pass

    async def resolving(self):
        while True:
            operation, id = await self._inqueue.get()

            resolve_futures = []

            try:
                if operation.node.operation == OperationType.QUERY:
                    for op in operation.node.selection_set.selections:
                        if op.name.value in self.query_resolver:
                            resolve_futures.append(
                                self.query_resolver[op.name.value](operation)
                            )
                        elif op.name.value in self.resolver:
                            resolve_futures.append(
                                self.resolver[op.name.value](operation)
                            )
                        else:
                            raise NotImplementedError(
                                f"Mocked Resolver for Query '{op.name.value}' not in resolvers: {self.query_resolver}, {self.resolver}  for AsyncMockLink"
                            )

                if operation.node.operation == OperationType.MUTATION:
                    for op in operation.node.selection_set.selections:
                        if op.name.value in self.mutation_resolver:
                            resolve_futures.append(
                                self.mutation_resolver[op.name.value](operation)
                            )
                        elif op.name.value in self.resolver:
                            resolve_futures.append(
                                self.resolver[op.name.value](operation)
                            )
                        else:
                            raise NotImplementedError(
                                f"Mocked Resolver for Query '{op.name.value}' not in resolvers: {self.mutation_resolver}, {self.resolver}  for AsyncMockLink"
                            )
                resolved = await asyncio.gather(*resolve_futures)
                self._futures[id].set_result(
                    GraphQLResult(
                        data={
                            target_from_node(op): resolved[i]
                            for i, op in enumerate(
                                operation.node.selection_set.selections
                            )
                        }
                    )
                )
            except AttributeError as t:
                raise ConfigurationError(f"No resolver for operation {op}") from t

            except Exception as e:

                self._futures[id].set_exception(e)

            self._inqueue.task_done()

    async def submit(self, o, id):
        await self._inqueue.put((o, id))

    async def aquery(self, operation: Operation) -> GraphQLResult:
        uniqueid = uuid.uuid4()
        self._futures[uniqueid] = asyncio.Future()
        await self.submit(operation, uniqueid)
        return await self._futures[uniqueid]

    async def asubscribe(self, operation: Operation) -> AsyncIterator[GraphQLResult]:
        if operation.node.operation == OperationType.SUBSCRIPTION:
            assert (
                len(operation.node.selection_set.selections) == 1
            ), "Only one Subscription at a time possible"

            op = operation.node.selection_set.selections[0]
            if op.name.value in self.subscription_resolver:
                iterator = self.subscription_resolver[op.name.value](operation)
            elif op.name.value in self.resolver:
                iterator = self.resolver[op.name.value](operation)
            else:
                raise NotImplementedError(
                    f"Mocked Resolver for Query '{op.name.value}' not in resolvers: {self.subscription_resolver}, {self.resolver}  for AsyncMockLink"
                )

            async for event in iterator:
                yield GraphQLResult(data={target_from_node(op): event})

        else:
            raise NotImplementedError("Only subscription are mocked")

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
