import { FaRegTrashAlt } from "react-icons/fa";
import { truncate } from "../../../common/functions";
import { Tooltip } from "react-tooltip";
import api from "../../../api";
import { CiEdit } from "react-icons/ci";
import { useState } from "react";

const LinkList = ({ links, setLinks, s }) => {
    const [isEdit, setIsEdit] = useState(false);
    async function 삭제하기(code) {
        try {
            const response = await api.delete(`/content?code=${code}`);
            setLinks(links.filter(link => link.code !== code))
        } catch (err) {
            console.log(err);
        }
    }
    function 수정하기() {
        setIsEdit(!isEdit);
    }
    return (
        <div className={s.content}>
            <Tooltip style={{ zIndex: 9999, background: '#e2b7e7' }} id="msg" />
            {
                links.map(link => (
                    <div key={link.code} className={s.content_li}>

                        {isEdit?<div className={s.linkTitle}><input/></div>:<div onClick={()=>{window.open(link.link)}}  className={s.linkTitle} data-tooltip-id="msg" data-tooltip-content={link.title}>{truncate(link.title, 40)}</div>}
                        <div className={s.category}>{link.category_name}</div>

                        {/* <div className={s.edit} onClick={수정하기}><CiEdit /></div> */}
                        <div onClick={() => 삭제하기(link.code)}><FaRegTrashAlt /></div>
                    </div>
                ))
            }
        </div>
    )
}

export default LinkList;