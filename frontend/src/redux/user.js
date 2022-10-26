// ** Redux Imports
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"

// ** Axios Imports
import axios from "axios"

export const userMe = createAsyncThunk(
    "user/me",
    async () => {
        const response = await axios.get("/api/bookmarks/data")
        return {
            data: response.data.suggestions,
            bookmarks: response.data.bookmarks
        }
    }
)

export const userLogin = createAsyncThunk(
    "user/login",
    async (id) => {
        await axios.post(`${process.env.REACT_APP_BACKEND_URL}/login`, { id })
        return id
    }
)

export const userSlice = createSlice({
    name: "user",
    initialState: {
        data: null
    },
    reducers: {
        login: (state, action) => {
            window.localStorage.setItem('token', action.payload.token)
            state.data = action.payload.user
        },
        me: (state, action) => {
            state.data = action.payload
        }
    }
})


export default userSlice.reducer
