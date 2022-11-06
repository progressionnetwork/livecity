
import {useLocation, useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";

import TreeView from '@mui/lab/TreeView';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import TreeItem from '@mui/lab/TreeItem';

import {request} from '../utility/request'
import {Card, CardBody, CardHeader, CardTitle, Spinner} from "reactstrap";


function generateNodeId() {
    return (Math.random() + 1).toString(36).substring(7);
}

const Sn = () => {
    const params = useParams();

    const [expanded, setExpanded] = React.useState([]);

    const handleToggle = (event, nodeIds)  => {
        setExpanded(nodeIds);
    };

    const [sn, setSn] = useState(null);
    const [info, setInfo] = useState(null)


    useEffect(() => {
        if (params.id) {
            request('get', `sn/${params.id}/`).then(data => {
                setSn(data)
            })
        }
    }, [params.id])

    return (
        <div>
            {sn ? <Card>
                    <CardHeader>
                        <CardTitle>{sn.type_ref}</CardTitle>
                    </CardHeader>
                        <CardBody>
                            <TreeView
                                aria-label="disabled items"
                                defaultCollapseIcon={<ExpandMoreIcon />}
                                defaultExpandIcon={<ChevronRightIcon />}
                                onNodeToggle={handleToggle}
                                expanded={expanded}
                            >
                                {sn.sections.map((e, i) => (
                                    <TreeItem nodeId={i.toString()} label={e.name} onClick={async () => {
                                        if (info?.id === e.id) {
                                            return;
                                        }
                                        const data = await request('get', `sn_section/${e.id}`);
                                        setInfo(data)
                                        setExpanded([i.toString()])
                                    }}>
                                        {e.id === info?.id && info.rows.map((row) => (
                                            <TreeItem nodeId={row.id} label={row.name} />
                                        ))}
                                    </TreeItem>
                                ))}
                            </TreeView>
                        </CardBody>
                </Card> : <Spinner />
            }

        </div>
    )
}

export default Sn;
