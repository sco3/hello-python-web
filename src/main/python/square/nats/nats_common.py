import asyncio
import uvloop
from typing import ClassVar
from asyncio import Lock


class NatsCommon:
    HELLO_STR: ClassVar[str] = "Hello, world!\n"
    HELLO: ClassVar[bytes] = HELLO_STR.encode("UTF-8")
    HELLO_LEN: ClassVar[int] = len(HELLO)

    START_PORT: ClassVar[int] = 4222
    NODES: ClassVar[int] = 3

    SERVERS: ClassVar[list] = [
        f"nats://localhost:{i}" for i in range(START_PORT, START_PORT + NODES)
    ]

    USER: ClassVar[str] = "sys"
    PASS: ClassVar[str] = "pass"

    SQUARE_SUBJECT: ClassVar[str] = "square"

    REQ_PREFIX: ClassVar[str] = "req."
    REQ_ALL: ClassVar[str] = f"{REQ_PREFIX}*"
    REQ_PREFIX_LEN: ClassVar[int] = len(REQ_PREFIX)
    REQ_SUBJECT: ClassVar[str] = f"{REQ_PREFIX}" + "{}"

    RES_PREFIX: ClassVar[str] = "res."
    RES_PREFIX_LEN: ClassVar[int] = len(RES_PREFIX)
    RES_SUBJECT: ClassVar[str] = f"{RES_PREFIX}" + "{}"

    lock: ClassVar[Lock] = asyncio.Lock()

    calls: ClassVar[int] = 0
    traffic: ClassVar[int] = 0
    duration: ClassVar[float] = 0
    call_duration: ClassVar[float] = 0

    @staticmethod
    def reset_stats() -> None:
        NatsCommon.calls = 0
        NatsCommon.traffic = 0
        NatsCommon.duration = 0
        NatsCommon.call_duration = 0

    @staticmethod
    def setClusterNodes(nodes: int) -> None:
        NatsCommon.NODES = nodes
        NatsCommon.SERVERS = [
            f"nats://localhost:{i}" for i in range(4222, 4222 + nodes)
        ]

    @staticmethod
    async def connect(nc) -> bool:
        result: bool = False
        try:
            await nc.connect(
                NatsCommon.SERVERS,
                user=NatsCommon.USER,
                password=NatsCommon.PASS,
            )
            result = True
        except RuntimeError as e:
            print(f"Error: {e}")

        return result


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
