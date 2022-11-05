import {useLocation, useParams} from "react-router-dom";
import {useEffect, useState} from "react";

import TreeView from '@mui/lab/TreeView';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import TreeItem from '@mui/lab/TreeItem';

import {request} from '../utility/request'
import {Card, CardBody, CardHeader, CardTitle, Spinner} from "reactstrap";

const Sn = () => {
    const params = useParams();

    const [sn, setSn] = useState(null);

    useEffect(() => {
        if (params.id) {
            request('get', `sn/${params.id}/`).then(data => {
                console.log(data)
                setSn(data)
            })
        }
    }, [params.id])

    return (
        <div>
            {sn ? <Card>
                    <CardHeader>
                        <CardTitle>{sn.type_ref}</CardTitle>
                        <CardBody>
                            <TreeView
                                aria-label="disabled items"
                                defaultCollapseIcon={<ExpandMoreIcon />}
                                defaultExpandIcon={<ChevronRightIcon />}
                                multiSelect
                            >
                                {/*{*/}
                                {/*    sn*/}
                                {/*}*/}
                            </TreeView>
                        </CardBody>
                    </CardHeader>
                </Card> : <Spinner />
            }

        </div>
    )
}

export default Sn;
