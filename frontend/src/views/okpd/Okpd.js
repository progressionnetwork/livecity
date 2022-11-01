import {Button, Card, CardBody, CardHeader, CardText, CardTitle, Spinner} from "reactstrap";
import DataTable from "react-data-table-component";
import {columns} from "./list/columns";
import {ChevronDown} from "react-feather";
import ReactPaginate from "react-paginate";
import {useEffect, useState} from "react";
import {request} from "../../utility/request";
import CardActions from "../../@core/components/card-actions";

const Okpd = () => {
    const [nextPage, setNextPage] = useState('');
    const [okpdList, setOkpdList] = useState(null);

    useEffect(() => {
        request('get', 'okpd/').then(data => {
            setNextPage(data.next)
            setOkpdList(data.results)
        })
    }, [])

    return (
        <Card>
            <CardHeader>
                <CardTitle>List okpd</CardTitle>
            </CardHeader>
            <CardBody>
                {okpdList ? <div className='react-List'>
                        {okpdList.map(e => <Card key={e.code}>
                            <CardTitle>{e.code} {e.name}</CardTitle>
                            <Button.Ripple color='flat-danger'>Danger</Button.Ripple>
                        </Card>)}
                    </div> : <div>
                        <Spinner/>
                    </div>
                }
            </CardBody>
        </Card>
    )
}

export default Okpd;
