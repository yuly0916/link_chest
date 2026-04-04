import { jwtDecode } from "jwt-decode";
import { useEffect, useState } from "react";
import { useCookies } from "react-cookie";
import { useNavigate } from "react-router-dom";
import s from "./Home.module.css";
import api from "../../api";

import Header from "./Components/Header";
import LinkList from "./Components/LinkList";
import Sidebar from "./Components/Sidebar";

const Home = () => {
    const nav = useNavigate();
    const [cookies, setCookie, removeCookie] = useCookies(['jwt_token']);

    const [links, setLinks] = useState([]);
    const [sort, setSort] = useState(true);
    const [user, setUser] = useState({});

    async function 링크가져오기() {
        const 서버응답 = await api.get(`/link?sort=${sort}`);
        if (서버응답.data.length === 0) nav("/category_selection")
        setLinks(서버응답.data)
    }

    useEffect(() => {
        if (Object.keys(cookies).length === 0) {
            nav('/');
        } else {
            setUser(jwtDecode(`Bearer ${cookies.jwt_token}`))
            링크가져오기()
        }
    }, [])
    useEffect(() => {링크가져오기()}, [sort])
    return (
        <div className={s.container}>
            <Header title="Link Chest" user={user} s={s}/>
            <main>
                <LinkList links={links} setLinks={setLinks} s={s}/>
                <Sidebar setLinks={setLinks} 링크가져오기={링크가져오기} sort={sort} setSort={setSort} s={s}/>
            </main>
        </div>
    )
}

export default Home;