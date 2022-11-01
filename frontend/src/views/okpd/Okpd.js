import {Button, Card, CardBody, CardHeader, CardText, CardTitle, Spinner} from "reactstrap";
import {useEffect, useState} from "react";
import {request} from "../../utility/request";

const Okpd = () => {
    const [maxResults, setMaxResults] = useState(0)
    const [nextPage, setNextPage] = useState('')
    const [okpdList, setOkpdList] = useState(null)

    const loadMore = async () => {
        console.log(nextPage)
        const data = await request('get', nextPage.split('.ru/')[1])
        setNextPage(data.next)
        setOkpdList(prev => [...prev, ...data.results])
    }

    useEffect(() => {
        request('get', 'okpd/').then(data => {
            setNextPage(data.next)
            setOkpdList(data.results)
            setMaxResults(data.count)
        })
    }, [])

    return (
        <Card>
            <CardBody>
                {okpdList ? <div className='react-List block'>
                        {okpdList.map(e => <Card key={e.code}>
                            <CardTitle>{e.code} {e.name}</CardTitle>
                            <CardBody>
                                <Button.Ripple color='flat-primary'>Редактирвать</Button.Ripple>
                                <Button.Ripple color='flat-primary' style={{ marginRight: 12 }}>Удалить</Button.Ripple>
                            </CardBody>
                        </Card>)}
                    </div> : <div>
                        <Spinner/>
                    </div>
                }
            </CardBody>
            {maxResults > okpdList?.length && <div style={{padding: 12, width: '100%'}}>
                <Button onClick={loadMore} style={{width: '100%'}} color='flat-primary'>загрузить еще</Button>
            </div>}
        </Card>
    )
}

export default Okpd;
