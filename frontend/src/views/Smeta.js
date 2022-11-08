import {useNavigate, useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {
    Button,
    Card,
    CardBody,
    CardFooter,
    CardHeader,
    CardTitle,
    Input,
    Label,
    Modal,
    ModalBody,
    ModalFooter,
    Spinner
} from "reactstrap";

import {request} from "../utility/request";
import {
    DateRange,
    DockSharp,
    DocumentScannerSharp,
    Edit, KeyboardArrowDown, KeyboardArrowUp,
    LocationCity,
    LocationOn,
    Money,
    NotificationImportantSharp
} from "@mui/icons-material";
import {
    Box,
    IconButton,
    Stack,
    Table,
    Collapse,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography, styled
} from "@mui/material";
import {useSelector} from "react-redux";
import {renderStatus} from "./Home";
import {numberWithSpaces} from "../utility/Utils";

// const CustomTableCell = styled(TableCell, {
//     color: 'var(--bs-body-color)',
//     fontSize: '1rem',
//     fontFamily: 'var(--bs-body-font-family)'
// })

const StyledTableCell = styled(TableCell)(({ theme }) => ({
    color: 'var(--bs-body-color)',
    fontSize: '1rem',
    fontFamily: 'var(--bs-body-font-family)'
}));

const Section = ({section}) => {
    const [open, setOpen] = React.useState(false);

    return (
        <React.Fragment>
            <TableRow sx={{
                '& > *': {
                    borderBottom: 'unset'
                }
            }}>
                <TableCell>
                    <IconButton
                        aria-label="expand row"
                        size="small"
                        onClick={() => setOpen(!open)}
                    >
                        {open ? <KeyboardArrowUp/> : <KeyboardArrowDown/>}
                    </IconButton>
                </TableCell>
                <StyledTableCell>
                    {section.name}
                </StyledTableCell>
                <StyledTableCell> {section.address === '' ? 'Адрес отсутствует или не найден' : section.address}</StyledTableCell>
                <StyledTableCell>{numberWithSpaces(section.sum)}</StyledTableCell>
            </TableRow>
            <TableRow>
                <TableCell style={{paddingBottom: 0, paddingTop: 0}} colSpan={4}>
                    <Collapse in={open} timeout="auto" unmountOnExit>
                        <Box sx={{margin: 1}}>
                            <Table size="small">
                                <TableBody>
                                    {section.subsections.map((subsection) => (
                                        <Subsection key={subsection.id} subsection={subsection}/>
                                    ))}
                                </TableBody>
                            </Table>
                        </Box>
                    </Collapse>
                </TableCell>
            </TableRow>
        </React.Fragment>
    );
}

const Subsection = ({subsection}) => {
    const [open, setOpen] = React.useState(false);
    const [openStats, setOpenStats] = useState([]);

    return (
        <React.Fragment>
            <TableRow sx={{'& > *': {borderBottom: 'unset'}}}>
                <StyledTableCell>
                    <IconButton
                        aria-label="expand row"
                        size="small"
                        onClick={() => setOpen(!open)}
                    >
                        {open ? <KeyboardArrowUp/> : <KeyboardArrowDown/>}
                    </IconButton>
                    {subsection.name}
                </StyledTableCell>
            </TableRow>
            <TableRow>
                <TableCell style={{paddingBottom: 0, paddingTop: 0}} colSpan={6}>
                    <Collapse in={open} timeout="auto" unmountOnExit>
                        <Box sx={{margin: 1}}>
                            <Table size="small">
                                <TableHead>
                                    <TableRow>
                                        <StyledTableCell sx={{ fontSize: '0.8rem', width: 70 }}>№ п/п</StyledTableCell>
                                        <StyledTableCell sx={{ fontSize: '0.8rem', width: 120 }}>Шифр</StyledTableCell>
                                        <StyledTableCell sx={{ fontSize: '0.8rem' }}>Название</StyledTableCell>
                                        <StyledTableCell sx={{ fontSize: '0.8rem', width: 100 }}>Кол-во</StyledTableCell>
                                        <StyledTableCell sx={{ fontSize: '0.8rem', width: 100 }}>Ед. изм.</StyledTableCell>
                                        <StyledTableCell sx={{ fontSize: '0.8rem', width: 150 }}>Сумма</StyledTableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {subsection.rows.map((row) => (
                                        <>
                                            <TableRow sx={{ cursor: 'pointer' }} key={row.id} onClick={() => {
                                                if (openStats.includes(row.id)) setOpenStats(openStats.filter(e => e !== row.id))
                                                else setOpenStats([...openStats, row.id])
                                            }}>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.num}</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.code}</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.name}</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.count}</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row?.ei?.short_name}</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{numberWithSpaces(row.sum)}</StyledTableCell>
                                            </TableRow>

                                            <TableRow sx={{ display: openStats.includes(row.id) ? undefined : 'none' }}>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }} colSpan={2}>СПГЗ по Fasttext</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.stats[0].fasttext_spgz}</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }} colSpan={2}>Вероятность по Fasttext</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.stats[0].fasstext_percent}</StyledTableCell>
                                            </TableRow>
                                            <TableRow sx={{ display: openStats.includes(row.id) ? undefined : 'none' }}>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }} colSpan={2}>СПГЗ по ключевым фразам</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.stats[0].key_phrases_spgz}</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }} colSpan={2}>Вероятность по ключевым фразам</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.stats[0].key_phrases_percent}</StyledTableCell>
                                            </TableRow>
                                            <TableRow sx={{ display: openStats.includes(row.id) ? undefined : 'none' }}>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }} colSpan={2}>Ключевые слова с вероятностями</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.stats[0].stat_words.map(e => `${e.name}(${e.percent})`).join(', ')}</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }} colSpan={2}>Рассотяние Левенштейна</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.stats[0].levenst_ratio}</StyledTableCell>
                                            </TableRow>
                                            <TableRow sx={{ display: openStats.includes(row.id) ? undefined : 'none' }}>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }} colSpan={2}>Является ключевой позицией</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.stats[0].is_key}</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }} colSpan={2}>Вероятность ключевой позиции</StyledTableCell>
                                                <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.stats[0].key_percent}</StyledTableCell>
                                            </TableRow>
                                        </>

                                    ))}
                                </TableBody>
                            </Table>
                        </Box>
                    </Collapse>
                </TableCell>
            </TableRow>
        </React.Fragment>
    );
}

const Stat = ({ stat }) => {
    const [open, setOpen] = React.useState(false);

    return (
        <React.Fragment>
            <TableRow sx={{'& > *': {borderBottom: 'unset'}}}>
                <StyledTableCell>
                    <IconButton
                        aria-label="expand row"
                        size="small"
                        onClick={() => setOpen(!open)}
                    >
                        {open ? <KeyboardArrowUp/> : <KeyboardArrowDown/>}
                    </IconButton>
                    Статистика
                </StyledTableCell>
            </TableRow>
            <TableRow>
                <TableCell style={{paddingBottom: 0, paddingTop: 0}} colSpan={6}>
                    <Collapse in={open} timeout="auto" unmountOnExit>
                        <Box sx={{margin: 1}}>
                            <Table size="small">
                                <TableHead>
                                    <TableRow>
                                        <StyledTableCell sx={{ fontSize: '0.8rem', width: 70 }}>№ п/п</StyledTableCell>
                                        <StyledTableCell sx={{ fontSize: '0.8rem', width: 120 }}>Шифр</StyledTableCell>
                                        <StyledTableCell sx={{ fontSize: '0.8rem' }}>Название</StyledTableCell>
                                        <StyledTableCell sx={{ fontSize: '0.8rem', width: 100 }}>Кол-во</StyledTableCell>
                                        <StyledTableCell sx={{ fontSize: '0.8rem', width: 100 }}>Ед. изм.</StyledTableCell>
                                        <StyledTableCell sx={{ fontSize: '0.8rem', width: 150 }}>Сумма</StyledTableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {subsection.rows.map((row) => (
                                        <TableRow key={row.id}>
                                            <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.num}</StyledTableCell>
                                            <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.code}</StyledTableCell>
                                            <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.name}</StyledTableCell>
                                            <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row.count}</StyledTableCell>
                                            <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{row?.ei?.short_name}</StyledTableCell>
                                            <StyledTableCell sx={{ fontSize: '0.8rem', color: 'white', backgroundColor: row.color }}>{numberWithSpaces(row.sum)}</StyledTableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </Box>
                    </Collapse>
                </TableCell>
            </TableRow>
        </React.Fragment>
    );
}

const Smeta = () => {
    const nav = useNavigate()
    const user = useSelector(state => state.user)
    const {id} = useParams()
    const [smeta, setSmeta] = useState(null);

    const [editItem, setEditItem] = useState();
    const [isModalEdit, setIsModalEdit] = useState(false)

    const updateSmeta = async () => {
        setIsModalEdit(false)
    }


    useEffect(() => {
        if (id) {
            request('get', `smeta/${id}/`).then(data => {
                setSmeta(data)
            })
        }
    }, [id])

    useEffect(() => {
        if (!user.data) {
            nav('/login')
        }
    }, [])

    return (
        <div>
            {
                smeta ? <Card>
                    <CardHeader>
                        <CardTitle>{smeta.name} {renderStatus(smeta.status_file)}</CardTitle>
                    </CardHeader>
                    <CardBody>
                        <Stack spacing={1} direction="row">
                            <LocationOn/>
                            <div>
                                Адрес: {smeta.address}
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <Money/>
                            <div>
                                Сумма без НДС: {numberWithSpaces(smeta.sum)} р.
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <Money/>
                            <div>
                                НДС: {numberWithSpaces(smeta.tax)} р.
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <Money/>
                            <div>
                                Сумма с НДС: {numberWithSpaces(smeta.sum_with_tax)} р.
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <DateRange/>
                            <div>
                                {smeta.coef_date}
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <DocumentScannerSharp/>
                            <div>
                                {smeta.type_ref}
                            </div>
                        </Stack>
                    </CardBody>
                    <CardFooter>
                        <TableContainer sx={{
                            color: 'white',
                            fontSize: '1rem'
                        }}>
                            <Table aria-label="collapsible table">
                                <TableBody>
                                    {smeta.sections.map((section) => (
                                        <Section key={section.id} section={section}/>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </CardFooter>
                </Card> : <Spinner/>
            }

            <Modal isOpen={isModalEdit} toggle={() => setIsModalEdit(!isModalEdit)} className='modal-dialog-centered'>
                <ModalBody>
                    <div>
                        <Label className='form-label' for='name'>
                            Название:
                        </Label>
                        <Input type='name' id='name' value={editItem?.value} onChange={(e => setEditItem(prev => ({
                            ...prev,
                            value: e.target.value
                        })))} placeholder='Название'/>
                    </div>
                </ModalBody>
                <ModalFooter>
                    <Button color='primary' onClick={updateSmeta}>
                        Сохранить
                    </Button>{' '}
                </ModalFooter>
            </Modal>

        </div>
    )
}

export default Smeta;
