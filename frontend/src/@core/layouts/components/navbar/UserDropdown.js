// ** React Imports
import { Link } from "react-router-dom"

// ** Custom Components
import Avatar from "@components/avatar"

// ** Third Party Components
import {
  User,
  Mail,
  CheckSquare,
  MessageSquare,
  Settings,
  CreditCard,
  HelpCircle,
  Power
} from "react-feather"

// ** Reactstrap Imports
import {
  UncontrolledDropdown,
  DropdownMenu,
  DropdownToggle,
  DropdownItem
} from "reactstrap"

// ** Default Avatar Image
import defaultAvatar from "@src/assets/images/portrait/small/avatar-s-11.jpg"
import {useSelector} from "react-redux";
import {Chip} from "@mui/material";

const UserDropdown = () => {
  const user = useSelector(state => state.user?.data)

  const renderRole = (role) => {
    const mapRole = {
      1: "Супер админ",
      2: "Админ",
      3: "Пользотватель"
    }
    return mapRole[role]
  }

  return (
    <UncontrolledDropdown tag="li" className="dropdown-user nav-item">
      <DropdownToggle
        href="/"
        tag="a"
        className="nav-link dropdown-user-link"
        onClick={(e) => e.preventDefault()}
      >
        <div className="user-nav d-sm-flex  d-none">
          <span className="user-name fw-bold">{user?.username}</span>
          <span className="user-status">{renderRole(user?.role)}</span>
        </div>
        <Avatar
          img={defaultAvatar}
          imgHeight="40"
          imgWidth="40"
          status="online"
        />
      </DropdownToggle>
      <DropdownMenu end>
        <DropdownItem tag={Link} to="/login"  onClick={() => {
          localStorage.setItem('token', '')
          window.location.reload()
        }}>
          <Power size={14} className="me-75" />
          <span className="align-middle">Выйти</span>
        </DropdownItem>
      </DropdownMenu>
    </UncontrolledDropdown>
  )
}

export default UserDropdown
