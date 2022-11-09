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
import {IconButton, styled, Table, TableBody, TableCell, TableContainer, TableHead, TableRow} from "@mui/material";
import {Edit} from "react-feather";
import {Delete} from "@mui/icons-material";


const StyledTableCell = styled(TableCell)(({theme}) => ({
    color: 'var(--bs-body-color)',
    fontSize: '1rem',
    fontFamily: 'var(--bs-body-font-family)'
}));

const Kpgz = () => {
    const nav = useNavigate()
    const user = useSelector(state => state.user)
    const [maxResults, setMaxResults] = useState(0)
    const [nextPage, setNextPage] = useState('')
    const [kpgzList, setKpgzList] = useState(null)

    const [editItem, setEditItem] = useState();
    const [isModalEdit, setIsModalEdit] = useState(false)

    const [search, setSearch] = useState('');

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
        if (!user.data) {
            nav('/login')
        }

        request('get', `kpgz/?search=${search}`).then(data => {
            setNextPage(data.next)
            setKpgzList(data.results)
            setMaxResults(data.count)
        })
    }, [])

    useEffect(() => {
        request('get', `kpgz/?search=${search}`).then(data => {
            setNextPage(data.next)
            setKpgzList(data.results)
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
                        Классификатор предметов государственного заказа
                    </CardTitle>
                    <div>
                        <Button>Обновить</Button>
                    </div>
                </CardHeader>
                <CardBody>
                    {kpgzList ? <div className=''>
                        <TableContainer sx={{
                            color: 'white',
                            fontSize: '1rem'
                        }}>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <StyledTableCell sx={{fontSize: '1rem', width: 70}}>Код</StyledTableCell>
                                        <StyledTableCell sx={{fontSize: '1rem'}}>Название</StyledTableCell>
                                        <StyledTableCell sx={{fontSize: '1rem'}}>Действия</StyledTableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {kpgzList.map((e, i) => (
                                        <TableRow>
                                            <StyledTableCell sx={{fontSize: '1rem', width: 70}}>{e.code}</StyledTableCell>
                                            <StyledTableCell sx={{fontSize: '1rem'}}>{e.name}</StyledTableCell>
                                            {user.data?.role < 3 && <StyledTableCell sx={{fontSize: '1rem'}}>
                                                <IconButton onClick={(j) => {
                                                    setIsModalEdit(true)
                                                    setEditItem(e)
                                                    j.preventDefault()
                                                }}>
                                                    <Edit/>
                                                </IconButton>
                                                <IconButton onClick={() => {
                                                    request('delete', `kpgz/${e.code}/`).then()
                                                    setKpgzList(prev => prev.filter(el => el.code !== e.code))
                                                }}>
                                                    <Delete/>
                                                </IconButton>
                                            </StyledTableCell>}
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
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
                        })))} placeholder='Название'/>
                    </div>
                </ModalBody>
                <ModalFooter>
                    <Button color='primary' onClick={updateKpgz}>
                        Сохранить
                    </Button>{' '}
                </ModalFooter>
            </Modal>
        </div>

    )
}

export default Kpgz;
