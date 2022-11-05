import {
    Button,
    Card,
    CardBody,
    CardHeader,
    CardText,
    CardTitle,
    Input,
    Label,
    Modal,
    ModalBody, ModalFooter,
    Spinner
} from "reactstrap";
import {useEffect, useState} from "react";
import {request} from "../utility/request";

const Kpgz = () => {
    const [maxResults, setMaxResults] = useState(0)
    const [nextPage, setNextPage] = useState('')
    const [kpgzList, setKpgzList] = useState(null)

    const [editItem, setEditItem] = useState();
    const [isModalEdit, setIsModalEdit] = useState(false)

    const updateKpgz = async () => {
        try {
            await request('put', `kpgz/${editItem?.code}/`,
                editItem
            );
        } catch (e) {
            console.log('update kpgz', 'что то пошло не так')
        }

        setKpgzList(prev => {
          const list = prev.splice(0);
          const i = list.findIndex(e => e.code === editItem.code);
          list.splice(i, 1, editItem)
            return list;
        })
        setIsModalEdit(false)
    }

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
                <CardHeader>
                    <CardTitle>
                        Классификатор предметов государственного заказа
                    </CardTitle>
                    <div>
                        <Button>Обновить</Button>
                    </div>
                </CardHeader>
                <CardBody>
                    {kpgzList ? <div className='react-List block'>
                        {kpgzList.map(e => <Card key={e.code} style={{ marginBottom: 0 }}>
                            <CardHeader>
                                <CardTitle>{e.name}</CardTitle>
                                <div>
                                    <Button.Ripple color='flat-primary' onClick={(j) => {
                                        setIsModalEdit(true)
                                        setEditItem(e)
                                        j.preventDefault()
                                    }}>Редактирвать</Button.Ripple>
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

            <Modal isOpen={isModalEdit} toggle={() => setIsModalEdit(!isModalEdit)} className='modal-dialog-centered'>
                <ModalBody>
                    <div>
                        <Label className='form-label' for='name'>
                            Название:
                        </Label>
                        <Input type='name' id='name' value={editItem?.name} onChange={(e => setEditItem(prev => ({
                            ...prev,
                            name: e.target.value
                        })))} placeholder='Название' />
                    </div>
                </ModalBody>
                <ModalFooter>
                    <Button color='primary' onClick={updateKpgz}>
                        Сохрнать
                    </Button>{' '}
                </ModalFooter>
            </Modal>
        </div>

    )
}

export default Kpgz;
