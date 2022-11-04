import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  CardText,
  CardLink, Button
} from "reactstrap"

import { useSelector } from "react-redux"
import { useEffect } from "react"
import {useNavigate} from "react-router-dom"

const Home = () => {
  const nav = useNavigate()
  const user = useSelector(state => state.user)

  useEffect(() => {
    if (!user.data) {
      nav('/login')
    }
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

        </CardBody>
      </Card>
    </div>
  )
}

export default Home
