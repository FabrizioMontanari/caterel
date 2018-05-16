const isAuthorized = cookie => cookie && cookie.length && cookie[0].value && cookie[0].value.includes('Logged=1');

const sanitiseHttpMethod = request => request.method = 'GET';

const passwordIsValid = pass => true;

const handleLogin = request => {
    if (request.uri === '/login.html' && request.method === 'POST' && passwordIsValid(request.passwordLocation)) {
        request.headers.cookie[0] = {
            value: 'Logged=1;',
            key: 'Cookie'
        };
        request.uri = '/';
    }
}

exports.handler = (event, context, callback) => {
    const { request } = event.Records[0].cf;
    const { uri, headers } = request;
    const cookie = headers.cookie;

    handleLogin(request);
    sanitiseHttpMethod(request);

    if (!isAuthorized(cookie)) {
        request.uri = '/login.html';
    }
    
    callback(null, request);
}