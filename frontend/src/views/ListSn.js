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

const Okei = () => {
    const [maxResults, setMaxResults] = useState(0)
    const [nextPage, setNextPage] = useState('')
    const [snList, setSnList] = useState(null)

    const [editItem, setEditItem] = useState();
    const [isModalEdit, setIsModalEdit] = useState(false)

    useEffect(() => {
        request('get', 'sn/').then(data => {
            setSnList(data)
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

                    </CardTitle>
                    <div>
                        <Button>Обновить</Button>
                    </div>
                </CardHeader>
                <CardBody>
                    {snList ? <div className='react-List block'>
                        {snList.map(e => <Card key={e.code} style={{ marginBottom: 0 }}>
                            <CardHeader>
                                <CardTitle>{e.type_ref}</CardTitle>
                                <div>
                                    <Button.Ripple color='flat-primary' onClick={(j) => {
                                        // setIsModalEdit(true)
                                        // setEditItem(e)
                                        // j.preventDefault()
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
                        Сохрнать
                    </Button>{' '}
                </ModalFooter>
            </Modal>
        </div>

    )
}

export default Okei;
