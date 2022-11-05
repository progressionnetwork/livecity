import { Mail, Home, Book } from "react-feather"

export default [
  {
    id: "home",
    title: "Сметы",
    icon: <Home size={20} />,
    navLink: "/home"
  },
  {
    id: "okpd",
    title: "ОКПД",
    icon: <Book size={20} />,
    navLink: "/okpd"
  },
  {
    id: "okpd2",
    title: "ОКПД2",
    icon: <Book size={20} />,
    navLink: "/okpd2"
  },
  {
    id: "kpgz",
    title: "КПГЗ",
    icon: <Book size={20} />,
    navLink: "/kpgz"
  },
  {
    id: "okei",
    title: "ОКЕИ",
    icon: <Book size={20} />,
    navLink: "/okei"
  },
  {
    id: "spgz",
    title: "СПГЗ",
    icon: <Book size={20} />,
    navLink: "/spgz"
  },
  {
    id: "users",
    title: "Пользователи",
    icon: <Mail size={20} />,
    navLink: "/users"
  }
]
