import { Mail, Home, Book } from "react-feather"

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
    icon: <Book size={20} />,
    navLink: "/second-page"
  },
  {
    id: "okpd",
    title: "okpd",
    icon: <Book size={20} />,
    navLink: "/okpd"
  },
  {
    id: "okpd2",
    title: "okpd2",
    icon: <Book size={20} />,
    navLink: "/okpd2"
  },
  {
    id: "users",
    title: "Пользователи",
    icon: <Mail size={20} />,
    navLink: "/users"
  }
]
