import {Button, Card, CardBody, CardHeader, CardText, CardTitle, Input, Label, Spinner} from "reactstrap";
import {useEffect, useState} from "react";
import {request} from "../utility/request";

const Kpgz = () => {
    const [maxResults, setMaxResults] = useState(0)
    const [nextPage, setNextPage] = useState('')
    const [kpgzList, setKpgzList] = useState(null)

    const loadMore = async () => {
        const data = await request('get', nextPage.split('.ru/')[1])
        setNextPage(data.next)
        setKpgzList(prev => [...prev, ...data.results])
    }

    useEffect(() => {
        request('get', 'kpgz/').then(data => {
            setNextPage(data.next)
            setKpgzList(data.results)
            setMaxResults(data.count)
        })
    }, [])

    return (
        <div>
            <Card>
                <CardBody>
                    <Label>Поиск</Label>
                    <Input />
                </CardBody>
            </Card>

            <Card>
                <CardBody>
                    {kpgzList ? <div className='react-List block'>
                        {kpgzList.map(e => <Card key={e.code}>
                            <CardHeader>
                                <CardTitle>№{e.code} {e.name}</CardTitle>
                                <div>
                                    <Button.Ripple color='flat-primary'>Редактирвать</Button.Ripple>
                                    <Button.Ripple color='flat-primary' style={{ marginRight: 12 }}>Удалить</Button.Ripple>
                                </div>
                            </CardHeader>
                        </Card>)}
                    </div> : <div>
                        <Spinner/>
                    </div>
                    }
                </CardBody>
                {maxResults > kpgzList?.length && <div style={{padding: 12, width: '100%'}}>
                    <Button onClick={loadMore} style={{width: '100%'}} color='flat-primary'>загрузить еще</Button>
                </div>}
            </Card>
        </div>

    )
}

export default Kpgz;
