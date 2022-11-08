import {
    Button,
    Card,
    CardBody,
    CardHeader,
    CardSubtitle,
    CardText,
    CardTitle,
    Input,
    Label,
    Modal, ModalBody, ModalFooter,
    Spinner
} from "reactstrap";
import {useEffect, useState} from "react";
import {request} from "../utility/request";
import {useNavigate} from "react-router-dom";
import {useSelector} from "react-redux";

const Okpd2 = () => {
    const nav = useNavigate()
    const user = useSelector(state => state.user)
    const [maxResults, setMaxResults] = useState(0)
    const [nextPage, setNextPage] = useState('')
    const [spgzList, setSpgzList] = useState(null)

    const [editItem, setEditItem] = useState();
    const [isModalEdit, setIsModalEdit] = useState(false)

    const [search, setSearch] = useState('');

    const updateSpgz = async () => {
        try {
            await request('put', `spgz/${editItem?.code}/`,
                editItem
            );
        } catch (e) {
            console.log('update spgz', 'что то пошло не так')
        }

        setSpgzList(prev => {
            const list = prev.splice(0);
            const i = list.findIndex(e => e.code === editItem.code);
            list.splice(i, 1, editItem)
            return list;
        })
        setIsModalEdit(false)
    }

    const loadMore = async () => {
        console.log(nextPage)
        const data = await request('get', nextPage.split('.ru/')[1])
        setNextPage(data.next)
        setSpgzList(prev => [...prev, ...data.results])
    }

    useEffect(() => {
        if (!user.data) {
            nav('/login')
        }

        request('get', `spgz/?search=${search}`).then(data => {
            setNextPage(data.next)
            setSpgzList(data.results)
            setMaxResults(data.count)
        })
    }, [])

    useEffect(() => {
        request('get', `kpgz/?search=${search}`).then(data => {
            setNextPage(data.next)
            setSpgzList(data.results)
            setMaxResults(data.count)
        })
    }, [search])

    return (
        <div>
            <Card>
                <CardBody>
                    <Label>Поиск</Label>
                    <Input value={search} onChange={(e) => setSearch(e.target.value)} />
                </CardBody>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>
                        Справочник предметов государственного заказа
                    </CardTitle>
                    <div>
                        <Button>
                            Обновить
                        </Button>
                    </div>
                </CardHeader>
                <CardBody>
                    {spgzList ? <div className='react-List block'>
                        {spgzList.map(e => <Card key={e.id} style={{ marginBottom: 0 }}>
                            <CardHeader>
                                <CardTitle>{e.id} - {e.name} ({e.key})</CardTitle>
                                {user.data?.role < 3 && <div>
                                    <Button.Ripple color='flat-primary' onClick={(j) => {
                                        setIsModalEdit(true)
                                        setEditItem(e)
                                        j.preventDefault()
                                    }}>Редактирвать</Button.Ripple>
                                    <Button.Ripple color='flat-primary'
                                                   style={{marginRight: 12}}>Удалить</Button.Ripple>
                                </div>}
                            </CardHeader>
                        </Card>)}
                    </div> : <div>
                        <Spinner/>
                    </div>
                    }
                </CardBody>
                {maxResults > spgzList?.length && <div style={{padding: 12, width: '100%'}}>
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
                    <Button color='primary' onClick={updateSpgz}>
                        Сохранить
                    </Button>{' '}
                </ModalFooter>
            </Modal>
        </div>

    )
}

export default Okpd2;
