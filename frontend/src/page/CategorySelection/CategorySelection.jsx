import { useEffect, useState } from "react";
import s from './CategorySelection.module.css';
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import api from "../../api";

const CategorySelection = () => {
    //이 페이지가 나오는 순간은 두 가지입니다.
    // 1. 첫 로그인 했을 때 유저가 추가한 링크가 하나도 없는 경우에 나옵니다.
    // 2. 추가한 링크가 이미 있는 유저가 새로운 링크를 등록하려고 할 때 나옵니다.
    const nav = useNavigate();
    const [cookies, setCookie, removeCookie] = useCookies(['jwt_token']);

    // 초기 카테고리 데이터
    const [categories, setCategories] = useState([]);
    const [seletedCategory, setSelectedCategory] = useState({ code: 0, label: "" });

    const [newCategory, setNewCategory] = useState();
    const [errMsg, setErrMsg] = useState('');

    // 카테고리 선택/해제 토글
    const toggleCategory = (cat) => {
        setSelectedCategory(cat);
    };

    // 새로운 카테고리 추가
    const addCategory = async () => {
        if (!newCategory.trim()) {
            alert('카테고리 이름을 입력해주세요!');
            return;
        }
        try {
            const res = await api.post('/category', newCategory);
            const newNode = { code: res.data, label: newCategory };
            setCategories([...categories, newNode]);
            setNewCategory('');
            setSelectedCategory(newNode);
        } catch (err) {
            setErrMsg(err.response.data.detail);
        }

    };
    const 유저카테고리가져오기 = async () => {
        const response = await api.get('/category');

        const userCustom = response.data.map(item => ({
            code: item.category_code,
            label: item.name
        }));

        setCategories(prev => [...prev, ...userCustom]);
    }
    useEffect(() => {
        유저카테고리가져오기();
    }, [])

    return (
        <div className={s.pageWrapper}>
            <div className={s.container}>
                <header className={s.header}>
                    <h1>나만의 보물상자 만들기</h1>
                    {errMsg ? <p className={s.errMsg}>{errMsg}</p>:<p>어떤 카테고리의 링크를 저장할까요?</p>}
                </header>

                <main className={s.content}>
                    <div className={s.categoryGrid}>
                        {categories.map((cat, i) => (
                            <div
                                key={i}
                                className={cat.code===seletedCategory.code ? s.categoryItemActive : s.categoryItem}
                                onClick={() => toggleCategory(cat)}
                            >
                                <span className={s.label}>{cat.label}</span>
                            </div>
                        ))}
                    </div>

                    <div className={s.addCategory}>
                        <input
                            type="text"
                            value={newCategory}
                            onChange={(e) => setNewCategory(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && addCategory()}
                            placeholder="새 카테고리 입력"
                            maxLength="10"
                        />
                        <button type="button" onClick={addCategory}>추가</button>
                    </div>
                </main>

                <footer className={s.footer}>
                    <button onClick={() => nav('/link_add', {
                        state: seletedCategory
                    })} type="button" className={s.nextBtn}>다음 단계로</button>
                </footer>
            </div>
        </div>
    );
}

export default CategorySelection;