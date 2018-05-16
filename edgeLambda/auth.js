const isAuthorized = cookie => cookie && cookie.length && cookie[0].value && cookie[0].value.includes('Logged=1');

const sanitiseHttpMethod = request => request.method = 'GET';

exports.handler = (event, context, callback) => {
    const { request } = event.Records[0].cf;
    const { uri, headers } = request;
    const cookie = headers.cookie;

    if(!isAuthorized(cookie)) {
        request.uri = '/login.html';
    }

    sanitiseHttpMethod(request);
    callback(null, request);
}