import {Card, CardBody, CardHeader, CardTitle} from "reactstrap";

export const Forbidden = () => {
    return (
        <div>
            <Card>
                <CardHeader>
                    <CardTitle>
                        У вас нет доступа 💁‍♂
                    </CardTitle>
                </CardHeader>
                <CardBody>
                    Обратитесь к superadmin@livecity.gg
                </CardBody>
            </Card>
        </div>
    )
}
