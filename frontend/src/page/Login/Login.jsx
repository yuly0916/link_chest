import s from './Login.module.css';

const Login = () => {

    const moveToLogin = () => {
        window.location.href = `https://kauth.kakao.com/oauth/authorize?client_id=${import.meta.env.VITE_CLIENT_ID}&redirect_uri=${import.meta.env.VITE_REDIRECT_URI}&response_type=code`;
    }
    

    return (
        <div className={s.container}>
            <img className={s.sideImg} src="/login/login_trans.png" />

            <div className={s.box}>
                <img className={s.logo} src="/login/icon.png" />

                <div className={s.text}>
                    <div>흩어진 모든 취향,</div>
                    <div>카테고리로 모아 한눈에 다시 찾기</div>
                </div>

                <img onClick={moveToLogin} style={{cursor:'pointer'}} src="/login/kakao_login.png" />
            </div>
        </div>

    )
}

export default Login;