import {useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {Card, CardBody, CardFooter, CardHeader, CardTitle, Spinner} from "reactstrap";

import {request} from "../utility/request";
import TreeView from "@mui/lab/TreeView";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import TreeItem from "@mui/lab/TreeItem";
import {DateRange, DockSharp, DocumentScannerSharp, Edit, LocationCity, LocationOn, Money} from "@mui/icons-material";
import {rowBlackList, rowMapper} from "../configs/rowTree";
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
                                {smeta.address}
                            </div>
                        </Stack>
                        <Stack spacing={1}  mt={1}  direction="row">
                            <Money />
                            <div>
                                {smeta.sum} р.
                            </div>
                        </Stack>
                        <Stack spacing={1}  mt={1}  direction="row">
                            <Money />
                            <div>
                                {smeta.tax} р.
                            </div>
                        </Stack>
                        <Stack spacing={1}  mt={1}  direction="row">
                            <Money />
                            <div>
                                {smeta.sum_with_tax} р.
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
                                <TreeItem key={section.id} nodeId={section.id.toString()} label={section.name}>
                                    {section.subsections.map((subsection) => (
                                        <TreeItem key={subsection.id} nodeId={generateNodeId()} label={subsection.name}>
                                            {subsection.rows.map((row) => (
                                                <TreeItem nodeId={generateNodeId()} label={row.name}>
                                                    {Object.keys(row).filter(name => !rowBlackList.includes(name)).map((name) => (
                                                        name === 'ei' ? <TreeItem nodeId={generateNodeId()}
                                                                                  label={`${name} - ${row.ei?.name}`}/> : <TreeItem nodeId={generateNodeId()}
                                                                      label={`${rowMapper[name]} - ${row[name]}`}/>
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
