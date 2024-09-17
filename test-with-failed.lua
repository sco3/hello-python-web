-- wrk script to track HTTP errors (non-2xx and non-3xx responses)
errors = 0

response = function(status, headers, body)
    if status >= 400 then
        errors = errors + 1
    end
end

done = function(summary, latency, requests)
    io.write("Requests: ", summary.requests, "\n")
    io.write("Duration: ", summary.duration / 1000000, " seconds\n")
    io.write("Errors: ", errors, "\n")
end
