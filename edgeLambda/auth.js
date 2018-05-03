const unauthorizedResponse = {
    status: '401',
    statusDescription: 'Unauthorized',
    body: 'Unauthorized',
    headers: { 'www-authenticate': [{ key: 'WWW-Authenticate', value: 'Basic' }] }
};

const expectedAuthString = `Basic ${new Buffer('martini:sposi').toString('base64')}`;

const isAuthValid = auth => auth instanceof Array && auth[0].value === expectedAuthString;

exports.handler = (event, context, callback) => {
    const { request } = event.Records[0].cf;
    
    const callbackValue = isAuthValid(request.headers.authorization) ? request : unauthorizedResponse;

    callback(null, callbackValue);
}