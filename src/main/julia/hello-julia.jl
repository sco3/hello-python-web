import Pkg
Pkg.add("HTTP")

using HTTP

function hello_world(req::HTTP.Request)
    return HTTP.Response(200, "Hello, World!")
end

HTTP.serve(hello_world, "0.0.0.0", 8000)
