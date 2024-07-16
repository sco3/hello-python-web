

out=$(readlink -f target/hello-ws-client)

rm -rf out


cd src/main/go/ws-client/

go build -o $out  hello-ws-client.go  && $out
