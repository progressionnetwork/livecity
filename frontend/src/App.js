import React, {Suspense} from "react"

// ** Router Import
import Router from "./router/Router"
import {AuthProvider} from "./utility/context/AuthContext";

const App = () => {

    console.log(process.env)

    return (
        <Suspense fallback={null}>
            <AuthProvider>
                <Router/>
            </AuthProvider>
        </Suspense>
    )
}

export default App
