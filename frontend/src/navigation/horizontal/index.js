import { Mail, Home } from "react-feather"

export default [
  {
    id: "home",
    title: "Сметы",
    icon: <Home size={20} />,
    navLink: "/home"
  },
  {
    id: "secondPage",
    title: "Справочники",
    icon: <Mail size={20} />,
    navLink: "/second-page"
  },
  {
    id: "users",
    title: "Пользователи",
    icon: <Mail size={20} />,
    navLink: "/users"
  }
]
