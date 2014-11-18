var httpProxy = require('http-proxy');

var proxy = httpProxy.createProxyServer({
    target: 'ws://127.0.0.1:10138/',
    ws: true
});

proxy.listen(10139)
