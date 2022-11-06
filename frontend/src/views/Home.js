import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  CardText,
  CardLink, Button, Input, Label, CardFooter, Spinner
} from "reactstrap"
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

const MySwal = withReactContent(Swal)


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
              <Button color="primary" onClick={() => {
                nav(`/smeta/${e.id}`)
              }}>Подробнее</Button>
              <Button color="primary" outline style={{ marginLeft: 8 }} onClick={() => {
                request('get', `smeta/${e.id}/short_smeta`).then(() => {
                  return MySwal.fire({
                    title: 'Информация',
                    text: 'Поставили в очередь на обработку. Это может занять некоторое время',
                    icon: 'info',
                    customClass: {
                      confirmButton: 'btn btn-primary'
                    },
                    buttonsStyling: false
                  })
                })
              }}>Обработать</Button>
              <Button color="success" outline style={{ marginLeft: 8 }} onClick={() => {
                request('get', `smeta/${e.id}/exel`).then()
              }}>Выгрузить в exel</Button>
              <Button color="danger" style={{ marginLeft: 8 }}>Удалить</Button>
            </CardFooter>
          </Card>
      ))}

    </div>
  )
}

export default Home
