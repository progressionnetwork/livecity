import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  CardText,
  CardLink, Button, Input, Label, CardFooter, Spinner, Badge
} from "reactstrap"
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

const MySwal = withReactContent(Swal)


import { useSelector } from "react-redux"
import {useEffect, useState} from "react"
import {useNavigate} from "react-router-dom"

import {request} from "../utility/request";

export const renderStatus = (status) => {
  const style = {
    fontSize: '1.2rem'
  }
  const mapperStatus = {
    '-1':  <Badge pill color='light-danger' style={style}>Ошибка</Badge>,
    0:  <Badge pill color='light-primary' style={style}>Загружен файл</Badge>,
    1:  <Badge pill color='light-info' style={style}>Загружен в БД</Badge>,
    2:  <Badge pill color='light-warning' style={style}>Обрабатывается</Badge>,
    3:  <Badge pill color='light-success' style={style}>Готов</Badge>
  }
  return mapperStatus[status]
}

const Home = () => {
  const nav = useNavigate()
  const user = useSelector(state => state.user)
  const [listSmeta, setListSmeta] = useState(null);

  const [search, setSearch] = useState('');

  useEffect(() => {
    if (!user.data) {
      nav('/login')
    }

    request('get', 'smeta/').then(data => {
      setListSmeta(data)
    })

    const interval = setInterval(() => {
      request('get', 'smeta/').then(data => {
        setListSmeta(data)
      })
    }, 5 * 1000)

    return () => {
      setListSmeta(null)
      clearInterval(interval)
    }
  }, [])

  useEffect(() => {
    request('get', `smeta/?search=${search}`).then(data => {
      setListSmeta(data)
    })
  }, [search])

  return (
    <div>
      <Card>
        <CardHeader>
            <CardTitle>Ваши сметы</CardTitle>
            <Button color="primary" onClick={() => nav('/upload')}>Загрузить новую</Button>
        </CardHeader>
        <CardBody>
          <Label>Поиск</Label>
          <Input value={search} onChange={(e) => setSearch(e.target.value)} />
        </CardBody>
      </Card>

      {!listSmeta && <Spinner />}

      {listSmeta && listSmeta.map((e, i) => (
          <Card>
            <CardHeader>
              <CardTitle>
                {e.name}
              </CardTitle>
              {renderStatus(e.status_file)}
            </CardHeader>
            <CardBody>
              {e.address}
            </CardBody>
            <CardFooter style={{
              display: 'flex',
              justifyContent: 'flex-end'
            }}>
              <Button color="primary" onClick={() => {
                nav(`/smeta/${e.id}`)
              }}>Подробнее</Button>
              <Button color="primary" outline style={{ marginLeft: 8 }} onClick={() => {
                request('get', `smeta/${e.id}/short_smeta`).then(() => {
                  setListSmeta(prev => {
                    const list = prev.splice(0)
                    list[i].status_file = 2
                    return list;
                  })
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

                fetch(`https://api.livecity.goodgenius.ru/smeta/${e.id}/excel/`, {
                  method: 'GET',
                  headers: {
                    'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    Authorization: `Token ${localStorage.getItem('token')}`
                  }
                })
                    .then((response) => response.blob())
                    .then((blob) => {
                      const url = window.URL.createObjectURL(
                          new Blob([blob])
                      );
                      const link = document.createElement('a');
                      link.href = url;
                      link.setAttribute(
                          'download',
                          `${e.name}.xlsx`
                      );

                      // Append to html link element page
                      document.body.appendChild(link);

                      // Start download
                      link.click();

                      // Clean up and remove the link
                      link.parentNode.removeChild(link);
                    });
              }}>Выгрузить</Button>
              <Button color="danger" style={{ marginLeft: 8 }} onClick={() => {
                request('delete', `smeta/${e.id}/`).then()
                setListSmeta(prev => prev.filter((el) => el.id !== e.id))
              }}>Удалить</Button>
            </CardFooter>
          </Card>
      ))}
    </div>
  )
}

export default Home
