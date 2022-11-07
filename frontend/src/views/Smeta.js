import {useParams} from "react-router-dom";
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
import TreeView from "@mui/lab/TreeView";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import TreeItem from "@mui/lab/TreeItem";
import {
    DateRange,
    DockSharp,
    DocumentScannerSharp,
    Edit,
    LocationCity,
    LocationOn,
    Money,
    NotificationImportantSharp
} from "@mui/icons-material";
import {rowBlackList, rowMapper, statMapper, statWordMapper} from "../configs/rowTree";
import {Stack} from "@mui/material";

function generateNodeId() {
    return (Math.random() + 1).toString(36).substring(7);
}


const Smeta = () => {
    const {id} = useParams()
    const [smeta, setSmeta] = useState(null);

    const [editItem, setEditItem] = useState();
    const [isModalEdit, setIsModalEdit] = useState(false)

    const [expanded, setExpanded] = React.useState([]);

    const handleToggle = (event, nodeIds) => {
        setExpanded(nodeIds);
    };

    const updateSmeta = async () => {
        // try {
        //     await request('put', `okpd/${editItem?.id}/`,
        //         {
        //             [editItem?.name]: editItem.value
        //         }
        //     );
        // } catch (e) {
        //     console.log('update okpd', 'что то пошло не так')
        // }
        //
        // setOkpdList(prev => {
        //     const list = prev.splice(0);
        //     const i = list.findIndex(e => e.code === editItem.code);
        //     list.splice(i, 1, editItem)
        //     return list;
        // })
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
        if (smeta) {
            const listNodes = [];
            for (const section of smeta.sections) {
                listNodes.push(section.id.toString());
                for (const subsection of section.subsections) {
                    listNodes.push(`${section.id}_${subsection.id}`);
                }
            }

            setExpanded(listNodes)
        }
    }, [smeta])

    return (
        <div>
            {
                smeta ? <Card>
                    <CardHeader>
                        <CardTitle>{smeta.name}</CardTitle>
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
                                Сумма без НДС: {smeta.sum} р.
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <Money/>
                            <div>
                                НДС: {smeta.tax} р.
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <Money/>
                            <div>
                                Сумма с НДС: {smeta.sum_with_tax} р.
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
                        <TreeView
                            aria-label="disabled items"
                            defaultCollapseIcon={<ExpandMoreIcon/>}
                            defaultExpandIcon={<ChevronRightIcon/>}
                            onNodeToggle={handleToggle}
                            expanded={expanded}
                        >
                            {smeta.sections.map((section, i) => (
                                <TreeItem
                                    icon={<Edit onClick={(e) => {
                                        setIsModalEdit(true)
                                        setEditItem({
                                            name: 'name',
                                            value: section.name,
                                            id: section.id
                                        })
                                        e.stopPropagation();
                                    }}/>}
                                    key={section.id}
                                    nodeId={`${section.id}`}
                                    label={section.name}
                                >
                                    {section.subsections.map((subsection) => (
                                        <TreeItem
                                            icon={<Edit
                                                onClick={(e) => {
                                                    setIsModalEdit(true)
                                                    setEditItem({
                                                        name: 'name',
                                                        value: subsection.name,
                                                        id: subsection.id
                                                    })
                                                    e.stopPropagation();
                                                }}
                                            />}
                                            key={subsection.id}
                                            nodeId={`${section.id}_${subsection.id}`}
                                            label={subsection.name}
                                        >
                                            {subsection.rows.map((row) => (
                                                <TreeItem
                                                    icon={<Edit
                                                        onClick={(e) => {
                                                            setIsModalEdit(true)
                                                            setEditItem({
                                                                name: 'name',
                                                                value: row.name,
                                                                id: row.id
                                                            })
                                                            e.stopPropagation();
                                                        }}
                                                    />}
                                                    nodeId={`${section.id}_${subsection.id}_${row.id}`}
                                                    label={row.name}
                                                    style={{backgroundColor: row.color, color: 'white'}}
                                                >
                                                    {Object.keys(row).filter(name => !rowBlackList.includes(name)).map((name) => (
                                                        name === 'is_key' ? <TreeItem
                                                                nodeId={`${section.id}_${subsection.id}_${row.id}_${name}`}
                                                                label={`${rowMapper[name] ?? name} - ${row[name] ? 'Да' : 'Нет'}`}
                                                            /> :
                                                            name === 'ei' ?
                                                                <TreeItem
                                                                    nodeId={`${section.id}_${subsection.id}_${row.id}_${name}`}
                                                                    label={`${name} - ${row.ei?.name}`}
                                                                /> : name === 'stats' ?
                                                                    <TreeItem
                                                                        nodeId={`${section.id}_${subsection.id}_${row.id}_${name}`}
                                                                        label="Статистика"
                                                                    >
                                                                        {row.stats.map(stat => (
                                                                            <TreeItem
                                                                                nodeId={`${section.id}_${subsection.id}_${row.id}_${name}_${stat.id}`}
                                                                                label={stat.sn}
                                                                            >
                                                                                {Object.keys(stat).filter(name2 => !rowBlackList.includes(name2)).filter(e => e !== 'sn').map((name2) => (
                                                                                    name2 === 'is_key' ? <TreeItem
                                                                                            nodeId={`${section.id}_${subsection.id}_${row.id}_${name}_${stat.id}_${name2}`}
                                                                                            label={`${statMapper[name2] ?? name2} - ${row[name2] ? 'Да' : 'Нет'}`}
                                                                                        /> :
                                                                                        name2 === 'stat_words' ?
                                                                                            <TreeItem
                                                                                                nodeId={`${section.id}_${subsection.id}_${row.id}_${name}_${stat.id}_${name2}`}
                                                                                                label="Статистика по словам">
                                                                                                {stat.stat_words.map(stat_word => (
                                                                                                    <TreeItem
                                                                                                        nodeId={`${section.id}_${subsection.id}_${row.id}_${name}_${stat.id}_${name2}_${stat_word.id}`}
                                                                                                        label={`${stat_word.name} - ${stat_word.percent}`}
                                                                                                    />
                                                                                                ))}
                                                                                            </TreeItem> :
                                                                                            <TreeItem
                                                                                                nodeId={`${section.id}_${subsection.id}_${row.id}_${name}_${stat.id}_${name2}`}
                                                                                                label={`${statMapper[name2] ?? name2} - ${stat[name2]}`}/>
                                                                                ))}
                                                                            </TreeItem>
                                                                        ))}
                                                                    </TreeItem>
                                                                    : <TreeItem
                                                                        nodeId={`${section.id}_${subsection.id}_${row.id}_${name}`}
                                                                        label={`${rowMapper[name] ?? name} - ${row[name]}`}
                                                                        icon={<Edit onClick={(e) => {
                                                                            setIsModalEdit(true)
                                                                            setEditItem({
                                                                                name,
                                                                                value: row[name],
                                                                                id: row.id
                                                                            })
                                                                            e.stopPropagation();
                                                                        }}/>}
                                                                    />
                                                    ))}
                                                </TreeItem>
                                            ))}
                                        </TreeItem>
                                    ))}
                                </TreeItem>
                            ))}
                        </TreeView>
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
                        Сохрнать
                    </Button>{' '}
                </ModalFooter>
            </Modal>

        </div>
    )
}

export default Smeta;
