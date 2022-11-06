import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  CardText,
  CardLink, Button, Input, Label, CardFooter, Spinner
} from "reactstrap"

import { useSelector } from "react-redux"
import {useEffect, useState} from "react"
import {useNavigate} from "react-router-dom"

import {request} from "../utility/request";

const Home = () => {
  const nav = useNavigate()
  const user = useSelector(state => state.user)
  const [listSmeta, setListSmeta] = useState(null);

  useEffect(() => {
    if (!user.data) {
      nav('/login')
    }

    request('get', 'smeta/').then(data => {
      setListSmeta(data)
    })

  }, [])

  return (
    <div>
      <Card>
        <CardHeader>
          <CardTitle>Statistics</CardTitle>
        </CardHeader>
        <CardBody>
          <CardText></CardText>
          <CardText>
          </CardText>
        </CardBody>
      </Card>

      <Card>
        <CardHeader>
            <CardTitle>Ваши сметы</CardTitle>
            <Button color="primary" onClick={() => nav('/upload')}>Загрузить новую</Button>
        </CardHeader>
        <CardBody>
          <Label>Поиск</Label>
          <Input />
        </CardBody>
      </Card>

      {!listSmeta && <Spinner />}

      {listSmeta && listSmeta.map((e) => (
          <Card>
            <CardHeader>
              <CardTitle>
                {e.name}
              </CardTitle>
            </CardHeader>
            <CardBody>
              {e.address}
            </CardBody>
            <CardFooter>
              <Button color="primary">Подробнее</Button>
              <Button color="danger" style={{ marginLeft: 8 }}>Удалить</Button>
            </CardFooter>
          </Card>
      ))}

    </div>
  )
}

export default Home
