import { useNavigate } from "react-router-dom";
import { FaArrowUp } from "react-icons/fa";
import { FaArrowDown } from "react-icons/fa";
import { useEffect, useState } from "react";
import api from "../../../api";

const Sidebar = ({ setLinks, 링크가져오기, sort, setSort, s }) => {
    const nav = useNavigate();
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');

    async function 카테고리가져오기() {
        const 서버응답 = await api.get('/category');
        setCategories(서버응답.data)
    }
    async function 카테고리링크가져오기(name) {
        const res = await api.get(`/link/category?name=${name}`);
        setLinks(res.data);
        setSelectedCategory(name);
    }
    function 모두보기() {
        setSelectedCategory('');
        링크가져오기();
    }
    useEffect(() => {
        카테고리가져오기();
    }, [])
    return (
        <div className={s.side}>
            <button onClick={() => nav("/category_selection")} className={s.add_btn}><span>추가하기</span></button>
            <div className={s.sortBox}>
                <h2>정렬 기준</h2>
                <button className={s.add_btn}
                    onClick={() => setSort(!sort)}
                ><span>{sort ? "최신순" : "오래된 순"}{sort ? <FaArrowUp /> : <FaArrowDown />}</span> </button>
            </div>
            <div className={s.categoryList}>
                <h2>나만의 카테고리</h2>
                <div onClick={모두보기} className={s.category}>모두보기</div>
                {
                    categories.map(category => (
                        <div key={category.category_code} onClick={() => 카테고리링크가져오기(category.name)} className={selectedCategory === category.name ? s.selectedCategory : s.category}>
                            <div>{category.name}</div>
                        </div>
                    ))
                }
            </div>
        </div>
    )
}

export default Sidebar;