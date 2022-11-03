import {Button, Card, CardBody, CardHeader, CardText, CardTitle, Input, Label, Spinner} from "reactstrap";
import {useEffect, useState} from "react";
import {request} from "../utility/request";

const Okei = () => {
    const [maxResults, setMaxResults] = useState(0)
    const [nextPage, setNextPage] = useState('')
    const [okeiList, setOkeiList] = useState(null)

    const loadMore = async () => {
        const data = await request('get', nextPage.split('.ru/')[1])
        setNextPage(data.next)
        setOkeiList(prev => [...prev, ...data.results])
    }

    useEffect(() => {
        request('get', 'okei/').then(data => {
            setNextPage(data.next)
            setOkeiList(data.results)
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
                    {okeiList ? <div className='react-List block'>
                        {okeiList.map(e => <Card key={e.code}>
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
                {maxResults > okeiList?.length && <div style={{padding: 12, width: '100%'}}>
                    <Button onClick={loadMore} style={{width: '100%'}} color='flat-primary'>загрузить еще</Button>
                </div>}
            </Card>
        </div>

    )
}

export default Okei;
