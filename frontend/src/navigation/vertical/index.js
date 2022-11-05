import { Mail, Home, Book } from "react-feather"

export default [
  {
    id: "home",
    title: "Сметы",
    icon: <Home size={20} />,
    navLink: "/home"
  },
  {
    id: "reference_books",
    title: "Справочники",
    icon: <Book size={20} />,
    children: [
      {
        id: "spgz",
        title: "СПГЗ",
        icon: <Book size={20} />,
        navLink: "/spgz"
      },
      {
        id: "kpgz",
        title: "КПГЗ",
        icon: <Book size={20} />,
        navLink: "/kpgz"
      },
      {
        id: "sn",
        title: "СН и ТСН",
        icon: <Book size={20} />,
        navLink: "/sn"
      },
      {
        id: "tz",
        title: "ТЗ",
        icon: <Book size={20} />,
        navLink: "/tz"
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
        id: "okei",
        title: "ОКЕИ",
        icon: <Book size={20} />,
        navLink: "/okei"
      }
    ]
  },
  {
    id: "users",
    title: "Пользователи",
    icon: <Mail size={20} />,
    navLink: "/users"
  }
]
