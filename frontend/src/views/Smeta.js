import {useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {Card, CardBody, CardFooter, CardHeader, CardTitle, Spinner} from "reactstrap";

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

    useEffect(() => {
        if (id) {
            request('get', `smeta/${id}/`).then(data => {
                setSmeta(data)
            })
        }
    }, [id])

    return (
        <div>
            {
                smeta ? <Card>
                    <CardHeader>
                        <CardTitle>{smeta.name}</CardTitle>
                    </CardHeader>
                    <CardBody>
                        <Stack spacing={1} direction="row">
                            <LocationOn />
                            <div>
                                Адрес: {smeta.address}
                            </div>
                        </Stack>
                        <Stack spacing={1}  mt={1}  direction="row">
                            <Money />
                            <div>
                                Сумма без НДС: {smeta.sum} р.
                            </div>
                        </Stack>
                        <Stack spacing={1}  mt={1}  direction="row">
                            <Money />
                            <div>
                                НДС: {smeta.tax} р.
                            </div>
                        </Stack>
                        <Stack spacing={1}  mt={1}  direction="row">
                            <Money />
                            <div>
                                Сумма с НДС: {smeta.sum_with_tax} р.
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <DateRange />
                            <div>
                                {smeta.coef_date}
                            </div>
                        </Stack>
                        <Stack spacing={1} mt={1} direction="row">
                            <DocumentScannerSharp />
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
                        >
                            {smeta.sections.map((section, i) => (
                                <TreeItem
                                    icon={<Edit />}
                                    key={section.id}
                                    nodeId={section.id.toString()}
                                    label={section.name}
                                >
                                    {section.subsections.map((subsection) => (
                                        <TreeItem
                                            icon={<Edit />}
                                            key={subsection.id}
                                            nodeId={generateNodeId()}
                                            label={subsection.name}
                                        >
                                            {subsection.rows.map((row) => (
                                                <TreeItem
                                                    icon={<Edit />}
                                                    nodeId={generateNodeId()}
                                                    label={row.name}
                                                >
                                                    {Object.keys(row).filter(name => !rowBlackList.includes(name)).map((name) => (
                                                        name === 'is_key' ? <TreeItem
                                                                nodeId={generateNodeId()}
                                                                label={`${rowMapper[name] ?? name} - ${row[name] ? 'Да' : 'Нет'}`}
                                                            /> :
                                                        name === 'ei' ?
                                                            <TreeItem
                                                                nodeId={generateNodeId()}
                                                                label={`${name} - ${row.ei?.name}`}
                                                            /> : name === 'stats' ?
                                                                <TreeItem nodeId={generateNodeId()} label="Статистика">
                                                                    {row.stats.map(stat => (
                                                                        <TreeItem nodeId={generateNodeId()} label={stat.sn}>
                                                                            {Object.keys(stat).filter(name => !rowBlackList.includes(name)).filter(e => e !== 'sn').map((name) => (
                                                                                name === 'is_key' ? <TreeItem
                                                                                        nodeId={generateNodeId()}
                                                                                        label={`${statMapper[name] ?? name} - ${row[name] ? 'Да' : 'Нет'}`}
                                                                                    /> :
                                                                                name === 'stat_words' ?
                                                                                    <TreeItem nodeId={generateNodeId()} label="Статистика по словам">
                                                                                        {stat.stat_words.map(stat_word => (
                                                                                            <TreeItem nodeId={generateNodeId()} label={`${stat_word.name} - ${stat_word.percent}`} />
                                                                                        ))}
                                                                                    </TreeItem> :
                                                                                    <TreeItem nodeId={generateNodeId()} label={`${statMapper[name] ?? name} - ${stat[name]}`} />
                                                                            ))}
                                                                        </TreeItem>
                                                                    ))}
                                                                </TreeItem>
                                                            :  <TreeItem
                                                                    nodeId={generateNodeId()}
                                                                    label={`${rowMapper[name] ?? name} - ${row[name]}`}
                                                                    icon={<Edit />}
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
        </div>
    )
}

export default Smeta;
