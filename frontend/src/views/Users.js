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
import {DeleteOutline, Edit, EditAttributes} from "@mui/icons-material";

const rows = [
    { id: 1, username: 'Snow', role: 1 },
    { id: 2, username: 'Lannister', role: 1  },
    { id: 3, username: 'Lannister', role: 1  },
    { id: 4, username: 'Stark', role: 1 },
    { id: 5, username: 'Targaryen', role: 1  },
    { id: 6, username: 'Melisandre', role: 1 },
    { id: 7, username: 'Clifford', role: 1  },
    { id: 8, username: 'Frances', role: 1 },
    { id: 9, username: 'Roxie', role: 1 }
];

const Users = () => {

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
                <CardTitle>Users List 🙌</CardTitle>
            </CardHeader>
            <CardBody>
                    <TableContainer>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>id</TableCell>
                                    <TableCell align="right">Name</TableCell>
                                    <TableCell align="right">Role</TableCell>
                                    <TableCell align="right">Дейсвия</TableCell>
                                </TableRow>
                            </TableHead>

                            <TableBody>
                                {rows.map((row) => (
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
                <TablePagination
                    component="div"
                    count={rows.length}
                    rowsPerPage={25}
                    page={0}
                    onPageChange={(e) => console.log(e)}
                />
            </CardBody>
        </Card>
    )
}

export default Users
