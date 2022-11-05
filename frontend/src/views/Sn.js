import {useLocation, useParams} from "react-router-dom";
import {useEffect, useState} from "react";

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

    const [sn, setSn] = useState(null);
    const [nodes, setNodes] = useState([]);

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
                                multiSelect
                            >
                                {sn.sections.map((e1, i1) => (
                                    <TreeItem nodeId={i1.toString()} label={e1.name}>
                                        <TreeItem nodeId="3" label="dfs">
                                            <TreeItem nodeId="fdsfhjkahjf" label="vfdhgagr5q34g">
                                            </TreeItem>
                                            <TreeItem nodeId="dfhjsdfg" label="feafsd">
                                            </TreeItem>
                                            <TreeItem nodeId="dsfr44" label="fweg">
                                            </TreeItem>
                                        </TreeItem>
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
