import {Button, Card, CardBody, CardHeader, CardTitle, Form, Input, Label} from "reactstrap";
import Select from "react-select";

const UploadEstimate = () => {
    return (
        <div>
            <Card>
                <CardHeader>
                    <CardTitle>
                        Загрузка сметы
                    </CardTitle>
                </CardHeader>
                <CardBody>
                    <div style={{display: 'flex', flexDirection: 'column', gap: 16, marginBottom: 16}}>
                        <div>
                            <Label>Название</Label>
                            <Input/>
                        </div>
                        <div>
                            <Label>Шаблон</Label>
                            <Select options={[
                                {
                                    label: "Вариант 1"
                                },
                                {
                                    label: "Вариант 2"
                                },
                                {
                                    label: "Вариант 3"
                                }
                            ]}/>
                        </div>
                    </div>
                    <Button>Загрузить файл сметы</Button>
                </CardBody>
                <Button color="primary">Готово</Button>
            </Card>
        </div>
    )
}

export default UploadEstimate;
