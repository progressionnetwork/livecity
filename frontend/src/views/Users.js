import {Card, CardHeader, CardBody, CardTitle, Button} from "reactstrap"
import {
    Paper,
    Table,
    TableBody,
    TableContainer,
    TableHead,
    TableRow,
    TableCell,
    styled,
    Chip, Stack, TableFooter, TablePagination
} from "@mui/material";
import {request} from "../utility/request";

import {DeleteOutline, Edit, EditAttributes} from "@mui/icons-material";
import {useEffect, useState} from "react";

const Users = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        request('get', 'users/').then(data => {
            setUsers(data.results)
        })
    }, [])

    const renderRole = (role) => {
        const mapRole = {
            1: <Chip label="Супер админ" />,
            2: <Chip label="Админ" />,
            3: <Chip label="Пользотватель" />
        }
        return mapRole[role]
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>Пользователи 👨🏼‍💻</CardTitle>
            </CardHeader>
            <CardBody>
                    <TableContainer>
                        <Table size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell>id</TableCell>
                                    <TableCell align="right">Name</TableCell>
                                    <TableCell align="right">Role</TableCell>
                                    <TableCell align="right">Дейсвия</TableCell>
                                </TableRow>
                            </TableHead>

                            <TableBody>
                                {users.map((row) => (
                                    <TableRow key={row.name}>
                                        <TableCell>
                                            {row.id}
                                        </TableCell>
                                        <TableCell align="left">{row.username}</TableCell>
                                        <TableCell align="left">{renderRole(row.role)}</TableCell>
                                        <TableCell align="center">
                                            <Stack direction='row' spacing={1}>
                                                <Button.Ripple className="btn-icon rounded-circle" color='flat-primary'>
                                                    <Edit size={16} />
                                                </Button.Ripple>
                                                <Button.Ripple className='btn-icon rounded-circle' color='flat-danger'>
                                                    <DeleteOutline size={16} />
                                                </Button.Ripple>
                                            </Stack>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                {/*<TablePagination*/}
                {/*    component="div"*/}
                {/*    count={users.length}*/}
                {/*    rowsPerPage={25}*/}
                {/*    page={0}*/}
                {/*    onPageChange={(e) => console.log(e)}*/}
                {/*/>*/}
            </CardBody>
        </Card>
    )
}

export default Users
