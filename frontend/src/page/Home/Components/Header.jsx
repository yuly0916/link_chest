import { useCookies } from "react-cookie";
import { useNavigate } from "react-router-dom";

const Header = ({ title, s, user }) => {
    const [cookies, setCookie, removeCookie] = useCookies(['jwt_token']);
    const nav = useNavigate();
    function 로그아웃() {
        removeCookie("jwt_token");
        nav("/");
    }

    return (
        <header>
            <h1 className={s.title}>{title}</h1>
            <div className={s.profile}>
                <img src={user.profile_img} />
                <div>{user.name}</div>
                <button onClick={로그아웃}>logout</button>
            </div>
        </header>)
}

export default Header;