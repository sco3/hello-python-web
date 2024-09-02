async def subscribe_to_messages(self,
                                component_type: str,
                                callback: Callable[[str, bytes], Any]):
    await logger.ainfo("consume_messages: subscribing to events on %s",
                       NATS_URL)
    self.heartbeat_task = asyncio.create_task(self.heartbeat(component_type))
    consumer_cfg = ConsumerConfig(
        durable_name=f"{self.consumer_name}_{component_type}",
        deliver_policy=DeliverPolicy.ALL,
        ack_policy=AckPolicy.EXPLICIT,
        filter_subject=self.subject.format(component_type=component_type,
                                           hostname=self.hostname),
    )

    await self.jet_stream.add_consumer(NATS_STREAM_NAME, consumer_cfg)
    # Clear the stop event to ensure we can start the loop
    self.stop_event.clear()

    while not self.stop_event.is_set():
        try:
            subscription = await self.jet_stream.pull_subscribe(
                self.subject.format(component_type=component_type,
                                    hostname=self.hostname),
                durable=f"{self.consumer_name}_{component_type}",
                config=consumer_cfg
            )
            msgs: list[Msg] = await subscription.fetch(10, timeout=NATS_TIMEOUT)
            await asyncio.gather(
                *[self.process_message(msg, callback, component_type) for msg in
                  msgs])
        except nats.errors.TimeoutError as exc:
            pass
