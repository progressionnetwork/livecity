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
import {useNavigate} from "react-router-dom";
import {useSelector} from "react-redux";

const ListSn = () => {
    const nav = useNavigate()
    const user = useSelector(state => state.user)

    const [search, setSearch] = useState('');
    const [maxResults, setMaxResults] = useState(0)
    const [nextPage, setNextPage] = useState('')
    const [snList, setSnList] = useState(null)

    const [editItem, setEditItem] = useState();
    const [isModalEdit, setIsModalEdit] = useState(false)

    useEffect(() => {
        if (!user.data) {
            nav('/login')
        }
        request('get', `sn/?search=${search}`).then(data => {
            setSnList(data)
        })
    }, [])

    useEffect(() => {
        request('get', `sn/?search=${search}`).then(data => {
            setSnList(data)
        })
    }, [search])

    return (
        <div>
            <Card>
                <CardHeader>
                    <CardTitle>

                    </CardTitle>
                    <div>
                        <Button>Обновить</Button>
                    </div>
                </CardHeader>
                <CardBody>
                    {snList ? <div className='react-List block'>
                        {snList.map(e => <Card key={e.code} style={{ marginBottom: 0 }} onClick={() => nav(`/sn/${e.id}`)}>
                            <CardHeader>
                                <CardTitle>{e.type_ref}</CardTitle>
                                {user.data?.role < 3 && <div>
                                    <Button.Ripple color='flat-primary' onClick={(j) => {
                                        // setIsModalEdit(true)
                                        // setEditItem(e)
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
                    <Button color='primary'>
                        Сохранить
                    </Button>{' '}
                </ModalFooter>
            </Modal>
        </div>

    )
}

export default ListSn;
