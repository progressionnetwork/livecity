import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import {Card, CardHeader, CardTitle, Spinner} from "reactstrap";

import {request} from "../utility/request";

const Smeta = () => {
    const { id } = useParams()
    const [smeta, setSmeta] = useState(null);

    useEffect(() => {
        request('get', `smeta/${id}/`).then(data => {
            console.log(data)
            setSmeta(data)
        })
    }, [id])

    return (
        <div>
            {
                smeta ? <Card>
                        <CardHeader>
                            <CardTitle>dsfjfs</CardTitle>
                        </CardHeader>
                    </Card> : <Spinner />
            }
        </div>
    )
}

export default Smeta;
