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
    Typography, styled, Switch
} from "@mui/material";
import {useSelector} from "react-redux";
import {renderStatus} from "./Home";
import {numberWithSpaces} from "../utility/Utils";

// const CustomTableCell = styled(TableCell, {
//     color: 'var(--bs-body-color)',
//     fontSize: '1rem',
//     fontFamily: 'var(--bs-body-font-family)'
// })

const StyledTableCell = styled(TableCell)(({theme}) => ({
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

const Subsection = (props) => {
    const [open, setOpen] = React.useState(false);
    const [openStats, setOpenStats] = useState([]);

    const [subsection, setSubsection] = useState(props.subsection);

    useEffect(() => {
        if (props.subsection) {
            setSubsection(subsection)
        }
    }, [props.subsection])

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
                                        <StyledTableCell sx={{fontSize: '0.8rem', width: 70}}>№ п/п</StyledTableCell>
                                        <StyledTableCell sx={{fontSize: '0.8rem', width: 120}}>Шифр</StyledTableCell>
                                        <StyledTableCell sx={{fontSize: '0.8rem'}}>Название</StyledTableCell>
                                        <StyledTableCell sx={{fontSize: '0.8rem', width: 100}}>Кол-во</StyledTableCell>
                                        <StyledTableCell sx={{fontSize: '0.8rem', width: 100}}>Ед.
                                            изм.</StyledTableCell>
                                        <StyledTableCell sx={{fontSize: '0.8rem', width: 150}}>Сумма</StyledTableCell>
                                        <StyledTableCell sx={{fontSize: '0.8rem', width: 150}}>Является
                                            ключевой</StyledTableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {subsection.rows.map((row, i) => (
                                        <>
                                            <TableRow sx={{cursor: 'pointer'}} key={row.id} onClick={() => {
                                                if (openStats.includes(row.id)) setOpenStats(openStats.filter(e => e !== row.id))
                                                else setOpenStats([...openStats, row.id])
                                            }}>
                                                <StyledTableCell sx={{
                                                    fontSize: '0.8rem',
                                                    color: 'white',
                                                    backgroundColor: row.color
                                                }}>{row.num}</StyledTableCell>
                                                <StyledTableCell sx={{
                                                    fontSize: '0.8rem',
                                                    color: 'white',
                                                    backgroundColor: row.color
                                                }}>{row.code}</StyledTableCell>
                                                <StyledTableCell sx={{
                                                    fontSize: '0.8rem',
                                                    color: 'white',
                                                    backgroundColor: row.color
                                                }}>{row.name}</StyledTableCell>
                                                <StyledTableCell sx={{
                                                    fontSize: '0.8rem',
                                                    color: 'white',
                                                    backgroundColor: row.color
                                                }}>{row.count}</StyledTableCell>
                                                <StyledTableCell sx={{
                                                    fontSize: '0.8rem',
                                                    color: 'white',
                                                    backgroundColor: row.color
                                                }}>{row?.ei?.short_name}</StyledTableCell>
                                                <StyledTableCell sx={{
                                                    fontSize: '0.8rem',
                                                    color: 'white',
                                                    backgroundColor: row.color
                                                }}>{numberWithSpaces(row.sum)}</StyledTableCell>
                                                <StyledTableCell sx={{
                                                    fontSize: '0.8rem',
                                                    color: 'white',
                                                    backgroundColor: row.color
                                                }}><Switch onClick={(e) => {
                                                    setSubsection(prev => {
                                                        request('patch', `smeta_row/${row.id}/`, {
                                                            is_key: !row.is_key
                                                        }).then()
                                                        const rows = prev.rows.splice(0)
                                                        rows[i].is_key = !row.is_key
                                                        return {
                                                            ...prev,
                                                            rows
                                                        }
                                                    })
                                                    e.stopPropagation()
                                                }} checked={row.is_key}/></StyledTableCell>
                                            </TableRow>

                                            <TableRow sx={{display: openStats.includes(row.id) ? undefined : 'none'}}>
                                                <StyledTableCell sx={{fontSize: '0.8rem', fontWeight: 800}} colSpan={2}>СПГЗ
                                                    по Fasttext</StyledTableCell>
                                                <StyledTableCell
                                                    sx={{fontSize: '0.8rem'}}>{row.stats[0].fasttext_spgz}</StyledTableCell>
                                                <StyledTableCell sx={{fontSize: '0.8rem', fontWeight: 800}} colSpan={2}>Вероятность
                                                    по Fasttext</StyledTableCell>
                                                <StyledTableCell
                                                    sx={{fontSize: '0.8rem'}}>{row.stats[0].fasstext_percent}</StyledTableCell>
                                            </TableRow>
                                            <TableRow sx={{display: openStats.includes(row.id) ? undefined : 'none'}}>
                                                <StyledTableCell sx={{fontSize: '0.8rem', fontWeight: 800}} colSpan={2}>СПГЗ
                                                    по ключевым фразам</StyledTableCell>
                                                <StyledTableCell
                                                    sx={{fontSize: '0.8rem'}}>{row.stats[0].key_phrases_spgz}</StyledTableCell>
                                                <StyledTableCell sx={{fontSize: '0.8rem', fontWeight: 800}} colSpan={2}>Вероятность
                                                    по ключевым фразам</StyledTableCell>
                                                <StyledTableCell
                                                    sx={{fontSize: '0.8rem'}}>{row.stats[0].key_phrases_percent}</StyledTableCell>
                                            </TableRow>
                                            <TableRow sx={{display: openStats.includes(row.id) ? undefined : 'none'}}>
                                                <StyledTableCell sx={{fontSize: '0.8rem', fontWeight: 800}} colSpan={2}>Ключевые
                                                    слова с вероятностями</StyledTableCell>
                                                <StyledTableCell
                                                    sx={{fontSize: '0.8rem'}}>{row.stats[0].stat_words.map(e => `${e.name}(${e.percent})`).join(', ')}</StyledTableCell>
                                                <StyledTableCell sx={{fontSize: '0.8rem', fontWeight: 800}} colSpan={2}>Рассотяние
                                                    Левенштейна</StyledTableCell>
                                                <StyledTableCell
                                                    sx={{fontSize: '0.8rem'}}>{row.stats[0].levenst_ratio}</StyledTableCell>
                                            </TableRow>
                                            <TableRow sx={{display: openStats.includes(row.id) ? undefined : 'none'}}>
                                                <StyledTableCell sx={{fontSize: '0.8rem', fontWeight: 800}} colSpan={2}>Является
                                                    ключевой позицией</StyledTableCell>
                                                <StyledTableCell
                                                    sx={{fontSize: '0.8rem'}}>{row.stats[0].is_key ? 'Да' : 'Нет'}</StyledTableCell>
                                                <StyledTableCell sx={{fontSize: '0.8rem', fontWeight: 800}} colSpan={2}>Вероятность
                                                    ключевой позиции</StyledTableCell>
                                                <StyledTableCell
                                                    sx={{fontSize: '0.8rem'}}>{row.stats[0].key_percent}</StyledTableCell>
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

const Smeta = () => {
    const nav = useNavigate()
    const user = useSelector(state => state.user)
    const {id} = useParams()
    const [smeta, setSmeta] = useState(null);

    const [editItem, setEditItem] = useState();
    const [isModalEdit, setIsModalEdit] = useState(false)

    const updateSmeta = async () => {
        request('patch', `smeta/${smeta.id}/`, editItem).then()
        setSmeta(prev => ({
            ...prev,
            ...editItem
        }))
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

        const interval = setInterval(() => {
            request('get', `smeta/${id}/`).then(data => {
                setSmeta(data)
            })
        }, 5 * 1000)

        return () => {
            setSmeta(null)
            clearInterval(interval)
        }
    }, [])

    if (smeta?.status_file !== 3) {
        return (
            smeta ?
                <div>
                    <Card>
                        <CardHeader>
                            <CardTitle>{smeta?.name}</CardTitle>
                            {renderStatus(smeta?.status_file)}
                        </CardHeader>
                        <CardBody>
                            Смета еще не обработана
                        </CardBody>
                    </Card>
                </div> : <Spinner/>

        )
    }

    return (
        <div>
            {
                smeta ? <Card>
                    <CardHeader>
                        <CardTitle>{smeta.name}</CardTitle>
                        {renderStatus(smeta.status_file)}
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
                                Дата сметных нормативов: {smeta.coef_date}
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <DocumentScannerSharp/>
                            <div>
                                Название сметных нормативов: {smeta.type_ref}
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <DocumentScannerSharp/>
                            <div>
                                Контроль сумм по
                                строкам: {smeta?.check_row_sum?.check ? `Пройдено (${numberWithSpaces(smeta.check_row_sum.value)})` : `Не пройдено (${numberWithSpaces(smeta.check_row_sum.value)})`}
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <DocumentScannerSharp/>
                            <div>
                                Контроль сумм по ключевым
                                строкам: {smeta?.check_keys_row_sum?.check ? `Пройдено (${numberWithSpaces(smeta.check_keys_row_sumeck?.value)})` : `Не пройдено (${numberWithSpaces(smeta.check_keys_row_sum.value)})`}
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <DocumentScannerSharp/>
                            <div>
                                Использованный шаблон ТЗ: {smeta.tz}
                            </div>
                        </Stack>
                        <Stack spacing={1} direction="row" mt={1}>
                            <Button color="primary" onClick={() => {
                                setEditItem({
                                    name: smeta.name,
                                    address: smeta.address,
                                    sum: smeta.sum,
                                    tax: smeta.tax,
                                    sum_with_tax: smeta.sum_with_tax,
                                    coef_date: smeta.coef_date
                                })
                                setIsModalEdit(true)
                            }
                            }>Редактировать</Button>
                            <Button color="success" outline style={{marginLeft: 8}} onClick={() => {

                                fetch(`https://api.livecity.goodgenius.ru/smeta/${smeta.id}/excel/`, {
                                    method: 'GET',
                                    headers: {
                                        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                        Authorization: `Token ${localStorage.getItem('token')}`
                                    }
                                })
                                    .then((response) => response.blob())
                                    .then((blob) => {
                                        const url = window.URL.createObjectURL(
                                            new Blob([blob])
                                        );
                                        const link = document.createElement('a');
                                        link.href = url;
                                        link.setAttribute(
                                            'download',
                                            `${smeta.name}.xlsx`
                                        );

                                        // Append to html link element page
                                        document.body.appendChild(link);

                                        // Start download
                                        link.click();

                                        // Clean up and remove the link
                                        link.parentNode.removeChild(link);
                                    });
                            }}>Выгрузить</Button>
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
                        <Input type='name' id='name' value={editItem?.name} onChange={(e => setEditItem(prev => ({
                            ...prev,
                            name: e.target.value
                        })))} placeholder='Название'/>
                    </div>
                    <div>
                        <Label className='form-label' for='name'>
                            Адрес:
                        </Label>
                        <Input type='name' id='name' value={editItem?.address} onChange={(e => setEditItem(prev => ({
                            ...prev,
                            address: e.target.value
                        })))} placeholder='Адрес'/>
                    </div>
                    <div>
                        <Label className='form-label' for='name'>
                            Сумма без НДС:
                        </Label>
                        <Input type='name' id='name' value={editItem?.sum} onChange={(e => setEditItem(prev => ({
                            ...prev,
                            sum: e.target.value
                        })))} placeholder='  Сумма без НДС'/>
                        <div>
                            <Label className='form-label' for='name'>
                                НДС:
                            </Label>
                            <Input type='name' id='name' value={editItem?.tax} onChange={(e => setEditItem(prev => ({
                                ...prev,
                                tax: e.target.value
                            })))} placeholder='  Сумма без НДС'/>
                        </div>
                        <Label className='form-label' for='name'>
                            Сумма с НДС:
                        </Label>
                        <Input type='name' id='name' value={editItem?.sum_with_tax}
                               onChange={(e => setEditItem(prev => ({
                                   ...prev,
                                   sum_with_tax: e.target.value
                               })))} placeholder='Сумма с НДС'/>

                        <Label className='form-label' for='name'>
                            Дата:
                        </Label>
                        <Input type='date' id='name' value={editItem?.coef_date} onChange={(e => setEditItem(prev => ({
                            ...prev,
                            coef_date: e.target.value
                        })))} placeholder='Дата'/>

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
