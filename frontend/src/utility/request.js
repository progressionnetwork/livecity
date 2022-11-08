import axios from "axios";

export const request = async (method, path, payload) => {
    const headers = {
        Authorization: `Token ${localStorage.getItem('token')}`
    }

    if (['post', 'put', 'patch'].includes(method.toLowerCase())) {
        const result = await axios[method.toLowerCase()](`${process.env.REACT_APP_BACKEND_URL}/${path}`, payload, {headers})
        return result.data;
    } else {
        const result = await axios[method.toLowerCase()](`${process.env.REACT_APP_BACKEND_URL}/${path}`, {headers})
        return result.data;
    }
}
