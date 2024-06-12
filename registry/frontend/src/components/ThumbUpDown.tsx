import React, {CSSProperties} from 'react'
import { faThumbsUp, faThumbsDown } from '@fortawesome/free-solid-svg-icons';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import useAuth from "../hooks/useAuth";

const buttonStyle = {
    "--fa-primary-color": "#ead91f",
    "--fa-secondary-color": "#ead91f",
} as CSSProperties;

interface ThumbVal {
  handleThumbClick: (action:"LikeAction" | "DislikeAction", author: string) => void;
  likeList: string[];
  dislikeList: string[];
  author: string;
}

export default function ThumbUpDown({handleThumbClick, likeList= [], dislikeList= [], author}: ThumbVal) {
    const [authEnabled, userInfo] = useAuth();
    const enableLike = authEnabled && userInfo && !likeList.includes(userInfo?.email) && author != userInfo?.email
    const enableDislike = authEnabled && userInfo && !dislikeList.includes(userInfo?.email) && author != userInfo?.email

  return (
      <div>
        <button onClick={() => handleThumbClick("LikeAction", author)} disabled={!enableLike} >
            {likeList.length}
          <FontAwesomeIcon icon={faThumbsUp} size="sm" style={buttonStyle}/>
        </button>
        <button onClick={() => handleThumbClick("DislikeAction", author)} disabled={!enableDislike}>
            {dislikeList.length}
          <FontAwesomeIcon icon={faThumbsDown} size="sm" style={buttonStyle}/>
        </button>
      </div>
  )
}