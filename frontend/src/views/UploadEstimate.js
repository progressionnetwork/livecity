import {Button, Card, CardBody, CardFooter, CardHeader, CardTitle, Form, Input, Label, Spinner} from "reactstrap";
import Select from "react-select";
import {useEffect, useRef, useState} from "react";
import {request} from "../utility/request";
import {Stack} from "@mui/material";
import {FilePresent} from "@mui/icons-material";
import axios from "axios";
import {useNavigate} from "react-router-dom";

const UploadEstimate = () => {
    const nav = useNavigate()
    const [tzList, setTzList] = useState(null);
    const inputFileRef = useRef(null);
    const [loading, setLoading] = useState(false)

    const [file, setFile] = useState()

    useEffect(() => {
        request('get', 'tz/').then(data => {
            setTzList(data)
        })
    }, [])

    const handleFileChange = (event) => {
        const file = event.target.files && event.target.files[0];
        if (!file) {
            return;
        }
        setFile(file)
    }

    const handleUploadSmeta = () => {
        const formData = new FormData();
        formData.append('type_file', 'smeta')
        formData.append('file', file)
        setLoading(true)
        axios.post(`${process.env.REACT_APP_BACKEND_URL}/update/file/`, formData, {
            headers: {
                Authorization: `Token ${localStorage.getItem('token')}`
            }
        }).then(res => {
            console.log(res.data)
            nav(`/smeta/${res.data.id}`)
            setLoading(false)
        })
    }

    return (
        <div>
            <input
                style={{display: 'none'}}
                ref={inputFileRef}
                type="file"
                onChange={handleFileChange}
                accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
            />
            <Card>
                <CardHeader>
                    <CardTitle>
                        Загрузка сметы
                    </CardTitle>
                </CardHeader>
                <CardBody>
                    <div style={{display: 'flex', flexDirection: 'column', gap: 16, marginBottom: 16}}>
                        {/*<div>*/}
                        {/*    <Label>Название</Label>*/}
                        {/*    <Input/>*/}
                        {/*</div>*/}
                        <div>
                            <Label>Шаблон</Label>
                            <Select options={tzList?.map((e) => ({
                                label: e.name
                            }))}/>
                        </div>
                    </div>
                    {file ?
                        <div>
                            Файл загружен
                            <Stack mt={1} direction="row" spacing={1}>
                                <FilePresent />
                                {file.name}
                            </Stack>
                        </div> :
                        <Button onClick={() => inputFileRef.current.click()}>Загрузить файл сметы</Button>
                    }
                </CardBody>
                <CardFooter>
                    <div>
                        {
                            loading ? <Spinner /> :
                            <Button style={{width: '100%'}} color="primary"
                                 onClick={() => handleUploadSmeta()}>Готово</Button>
                        }
                    </div>
                </CardFooter>
            </Card>
        </div>
    )
}

export default UploadEstimate;
