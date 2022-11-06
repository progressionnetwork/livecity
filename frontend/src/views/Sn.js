
import {useLocation, useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";

import TreeView from '@mui/lab/TreeView';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import TreeItem from '@mui/lab/TreeItem';

import {request} from '../utility/request'
import {
    Button,
    Card,
    CardBody,
    CardHeader,
    CardTitle,
    Input,
    Label,
    Modal,
    ModalBody,
    ModalFooter,
    Spinner
} from "reactstrap";
import {Edit} from "@mui/icons-material";
import {IconButton} from "@mui/material";


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

    const [editItem, setEditItem] = useState();
    const [isModalEdit, setIsModalEdit] = useState(false)

    const updateSn = async () => {
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
                                            <TreeItem nodeId={row.id} label={row.name} icon={<Edit onClick={(e) => {
                                                setIsModalEdit(true)
                                                setEditItem({
                                                    name: 'name',
                                                    value: row.name,
                                                    id: row.id
                                                })
                                                e.stopPropagation();
                                            }} />}>
                                                {Object.keys(row).filter(name => name !== 'name' && name !== 'id').map((name) => (
                                                    name === 'ei' ? <TreeItem nodeId={generateNodeId()} label={`${name} - ${row.ei.name}`} /> : <TreeItem nodeId={generateNodeId()} label={`${name} - ${row[name]}`} />
                                                ))}
                                            </TreeItem>
                                        ))}
                                    </TreeItem>
                                ))}
                            </TreeView>
                        </CardBody>
                </Card> : <Spinner />
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
                        })))} placeholder='Название' />
                    </div>
                </ModalBody>
                <ModalFooter>
                    <Button color='primary' onClick={updateSn}>
                        Сохрнать
                    </Button>{' '}
                </ModalFooter>
            </Modal>


        </div>
    )
}

export default Sn;
