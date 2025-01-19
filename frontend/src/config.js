// const API_BASE_URL = 'http://127.0.0.1:8000/';
const API_BASE_URL =  'https://wge6ph8070.execute-api.us-east-1.amazonaws.com/prod/';

export const API_ENDPOINTS = {
    POST_CREATE_USER: API_BASE_URL + 'users/',
    GET_USER: `${API_BASE_URL}users/:userId`,
    DELETE_USER: `${API_BASE_URL}users/:userId`,
    POST_CREATE_CONV: API_BASE_URL + 'conversations/',
    GET_CONV: `${API_BASE_URL}conversations/:convId`,
    GET_ALL_CONV: API_BASE_URL + 'conversations/',
    PUT_UPDATE_CONV: `${API_BASE_URL}conversations/:convId`,
    DELETE_CONV: `${API_BASE_URL}conversations/:convId`,
    POST_UPLOAD_DOCS: `${API_BASE_URL}upload/:userId`
};