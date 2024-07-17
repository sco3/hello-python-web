import asyncio
from typing import ClassVar


class NatsCommon:
    HELLO_STR: ClassVar[str] = "Hello, world!\n"
    HELLO: ClassVar[bytes] = HELLO_STR.encode("UTF-8")
    HELLO_LEN: ClassVar[int] = len(HELLO)

    SERVERS: ClassVar[list] = [
        "nats://localhost:4222",
        "nats://localhost:4223",
        "nats://localhost:4224",
    ]

    USER: ClassVar[str] = "sys"
    PASS: ClassVar[str] = "pass"

    REQ_PREFIX: ClassVar[str] = "req."
    REQ_ALL: ClassVar[str] = f"{REQ_PREFIX}*"
    REQ_PREFIX_LEN: ClassVar[int] = len(REQ_PREFIX)
    REQ_SUBJECT: ClassVar[str] = f"{REQ_PREFIX}" + "{}"

    RES_PREFIX: ClassVar[str] = "res."
    RES_PREFIX_LEN: ClassVar[int] = len(RES_PREFIX)
    RES_SUBJECT: ClassVar[str] = f"{RES_PREFIX}" + "{}"

    lock: asyncio.Lock = asyncio.Lock()

    calls: ClassVar[int] = 0
    traffic: ClassVar[int] = 0
    duration: ClassVar[int] = 0
    call_duration: ClassVar[int] = 0

    @staticmethod
    def reset_stats() -> None:
        NatsCommon.calls = 0
        NatsCommon.traffic = 0
        NatsCommon.duration = 0
        NatsCommon.call_duration = 0

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