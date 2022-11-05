import {useSkin} from "@hooks/useSkin"
import {Link, useNavigate} from "react-router-dom"
import logo from '../assets/images/logo/logo.png'
import {Facebook, Twitter, Mail, GitHub} from "react-feather"
import InputPasswordToggle from "@components/input-password-toggle"
import {
    Row,
    Col,
    CardTitle,
    CardText,
    Form,
    Label,
    Input,
    Button
} from "reactstrap"
import "@styles/react/pages/page-authentication.scss"
import axios from "axios";
import {useDispatch, useSelector} from "react-redux";
import {setUserData} from "../redux/user";
import {useEffect} from "react";

const Login = () => {
    const user = useSelector(state => state.user.data)
    const {skin} = useSkin()
    const dispatch = useDispatch()
    const nav = useNavigate()

    const illustration = skin === "dark" ? "login-v2-dark.svg" : "login-v2.svg",
        source = require(`@src/assets/images/pages/${illustration}`).default

    const handleLoginUser = async (e) => {
        const data = {}
        event.preventDefault()
        const form = new FormData(e.target)
        form.forEach((value, name) => data[name] = value)
        try {
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/login/`, data)
            if (response.data) {
                localStorage.setItem('token', response.data.token)
                dispatch(setUserData(response.data?.user))
            }
        } catch (e) {
            console.log('Bad auth')
        }
    }

    useEffect(() => {
        if (user) {
            nav('/')
        }
    }, [user])

    return (
        <div className="auth-wrapper auth-cover">
            <Row className="auth-inner m-0">
                <Link className="brand-logo" to="/" onClick={(e) => e.preventDefault()}>
                    <img src={logo} style={{
                        height: 28,
                        width: 28
                    }} />

                    <h2 className="brand-text text-primary ms-1">Живой город</h2>
                </Link>
                <Col className="d-none d-lg-flex align-items-center p-5" lg="8" sm="12">
                    <div className="w-100 d-lg-flex align-items-center justify-content-center px-5">
                        <img className="img-fluid" src={source} alt="Login Cover"/>
                    </div>
                </Col>
                <Col
                    className="d-flex align-items-center auth-bg px-2 p-lg-5"
                    lg="4"
                    sm="12"
                >
                    <Col className="px-xl-2 mx-auto" sm="8" md="6" lg="12">
                        <CardTitle tag="h2" className="fw-bold mb-1">
                            Добро пожаловать в Живой Город 👋
                        </CardTitle>
                        <CardText className="mb-2">
                            Войдите в ваш аккаунт
                        </CardText>
                        <Form
                            className="auth-login-form mt-2"
                            onSubmit={handleLoginUser}
                        >
                            <div className="mb-1">
                                <Label className="form-label" for="login-email">
                                    Почта
                                </Label>
                                <Input
                                    name="email"
                                    type="email"
                                    id="login-email"
                                    placeholder="john@example.com"
                                    autoFocus
                                />
                            </div>
                            <div className="mb-1">
                                <div className="d-flex justify-content-between">
                                    <Label className="form-label" for="login-password">
                                        Пароль
                                    </Label>
                                    <Link to="/forgot-password">
                                        <small>Забыли пароль?</small>
                                    </Link>
                                </div>
                                <InputPasswordToggle
                                    name="password"
                                    className="input-group-merge"
                                    id="login-password"
                                />
                            </div>
                            <div className="form-check mb-1">
                                <Input type="checkbox" id="remember-me"/>
                                <Label className="form-check-label" for="remember-me">
                                    Запомнить меня
                                </Label>
                            </div>
                            <Button color="primary" block>
                                Войти
                            </Button>
                        </Form>
                    </Col>
                </Col>
            </Row>
        </div>
    )
}

export default Login
