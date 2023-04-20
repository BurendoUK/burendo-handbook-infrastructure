function handler(event) {
    var response = event.response;
    var headers = response.headers;
    headers['cache-control'] = {value: 'no-store'};
    return response;
}
