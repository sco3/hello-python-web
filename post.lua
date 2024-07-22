-- post.lua
local file = io.open("text-request.txt", "r")
local body = file:read("*all")
file:close()

request = function()
    headers = {}
    headers["Content-Type"] = "application/octet-stream"  -- Adjust the content type if necessary
    return wrk.format("POST", "/", headers, body)
end
