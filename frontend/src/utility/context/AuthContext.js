import {createContext, useEffect, useState} from "react";
import {request} from "../request";
import {setUserData} from "../../redux/user";
import {useDispatch} from "react-redux";

export const AuthProvider = ({children}) => {
    const [loading, setLoading] = useState(true);
    const dispatch = useDispatch()
    useEffect(() => {
        request('get', 'me/').then((e) => {
            dispatch(setUserData(e))
            setLoading(false)
        })
    }, [])

    // if (loading) {
    //     return (
    //         <div>
    //             loaing
    //         </div>
    //     )
    // }

    return children;
}
