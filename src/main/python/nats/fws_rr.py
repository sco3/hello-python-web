##
#
# prefix = "/square/"
# prefix_len = len(prefix)
#
#
# def app(environ, start_response) -> bytes:
#    thread_id: int = threading.get_ident()
#    pid: int = os.getpid()
#    print(f"Current thread id: {thread_id} pid: {pid} {type(environ)}")
#
#    try:
#        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
#    except ValueError:
#        request_body_size = 0
#
#    headers = [("Content-Type", "text/plain")]
#    start_response("200 OK", headers)
#    path = environ.get("PATH_INFO", "")
#    if not path == "":
#        v = int(path[prefix_len:])
#
#    loop = asyncio.get_event_loop()
#    r = loop.run_until_complete(call(v))
#    # print(r)
#
#    return str(r).encode()
