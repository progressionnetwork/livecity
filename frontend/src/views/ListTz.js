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

const ListTz = () => {
    const nav = useNavigate()
    const user = useSelector(state => state.user)
    const [maxResults, setMaxResults] = useState(0)
    const [nextPage, setNextPage] = useState('')
    const [tzList, setTzList] = useState(null)

    const [editItem, setEditItem] = useState();
    const [isModalEdit, setIsModalEdit] = useState(false)

    const [search, setSearch] = useState('');

    useEffect(() => {
        if (!user.data) {
            nav('/login')
        }
        request('get', `tz?search=${search}`).then(data => {
            setTzList(data)
        })
    }, [])

    useEffect(() => {
        request('get', `kpgz/?search=${search}`).then(data => {
            setNextPage(data.next)
            setTzList(data.results)
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

                    </CardTitle>
                    <div>
                        <Button>Обновить</Button>
                    </div>
                </CardHeader>
                <CardBody>
                    {tzList ? <div className='react-List block'>
                        <TableContainer sx={{
                            color: 'white',
                            fontSize: '1rem'
                        }}>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <StyledTableCell sx={{fontSize: '1rem'}}>Название</StyledTableCell>
                                        <StyledTableCell sx={{fontSize: '1rem'}}>Действия</StyledTableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {tzList.map((e, i) => (
                                        <TableRow>
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
                                                    request('delete', `tz/${e.id}/`).then()
                                                    setTzList(prev => prev.filter(el => el.id !== e.id))
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

export default ListTz;

