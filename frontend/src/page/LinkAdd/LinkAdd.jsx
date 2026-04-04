import { useState } from "react";
import s from './LinkAdd.module.css';
import { useLocation, useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import api from "../../api";

const LinkAdd = () => {
    const nav = useNavigate();
    const location = useLocation();
    const category = location.state;

    
    const [cookies, setCookie, removeCookie] = useCookies(['jwt_token']);
    const [link, setLink] = useState({title:'', link:''});
    const handleInput = (e) => setLink(p=>({...p, [e.target.name]: e.target.value}));
    async function 링크추가하기(){
        const response = await api.post('/link',{
            category_code: category.code, 
            link: !link.link.startsWith("https") ? "https://www."+link.link : link.link, 
            title: link.title
        })        
        
        if(response.data){
            nav("/home")
        }
        else{
            alert("error")
        }
        
    }
    return (
        <div className={s.pageWrapper}>
            <div className={s.container}>
                <header className={s.header}>
                    <h1>나만의 보물상자 만들기</h1>
                    <p>저장할 링크를 알려주세요</p>
                </header>

                <main className={s.content}>

                    <div className={s.addCategory}>
                        <input
                            value={link.title}
                            name="title"
                            onChange={handleInput}
                            placeholder="링크에 대해 짧게 설명해주세요"
                        />
                        <input
                            type="text"
                            name="link"
                            value={link.link}
                            onChange={handleInput}
                            placeholder="저장할 링크 입력"
                        />
                    </div>
                </main>

                <footer className={s.footer}>
                    <button onClick={링크추가하기} type="button" className={s.nextBtn}>완성하고 보러가기</button>
                    <button onClick={() => nav(-1)} type="button" className={s.nextBtn}>뒤로 가기</button>
                </footer>
            </div>
        </div>
    );
}

export default LinkAdd;