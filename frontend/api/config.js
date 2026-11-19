  module.exports = function handler(request, response) {
    let apiBaseUrl = process.env.API_BASE_URL;
    apiBaseUrl = apiBaseUrl.replace(/\/+$/, '');

    if (!apiBaseUrl.endsWith('/api')) {
      apiBaseUrl += '/api';
    }

    response.setHeader('Content-Type', 'text/javascript; charset=utf-8');
    response.setHeader('Cache-Control', 'no-store');
    response.status(200).send(`window.ENV = Object.freeze(${JSON.stringify({
      API_BASE_URL: apiBaseUrl,
    })});`);
  };
