import {useEffect, useState} from 'react';
import {useRevalidator} from 'react-router-dom';
import {Rating} from 'react-simple-star-rating';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faThumbsDown, faThumbsUp} from '@fortawesome/free-solid-svg-icons';
import useAuth from '../hooks/useAuth';
import {Review as IReview, Vocab} from '../misc/interfaces';
import ReportAbuse from './ReportAbuse';
import AddReview from './AddReview';

interface ReviewsUserInteraction {
    authored: number[];
    likes: number[];
    dislikes: number[];
}

export default function Reviews({data}: { data: Vocab }) {
    const [authEnabled, userInfo] = useAuth();
    const [reviewsUserInteraction, setReviewsUserInteraction] =
        useState<ReviewsUserInteraction>({authored: [], likes: [], dislikes: []});

    useEffect(() => {
        if (authEnabled) {
            const fetchReviewsUserInteraction = async () => {
                const response = await fetch(`/reviews_user_interaction/${data.id}`);
                if (response.ok) {
                    const rsp = await response.json();
                    setReviewsUserInteraction(rsp);
                }
            };

            fetchReviewsUserInteraction();
        }
    }, [authEnabled]);

    return (
        <div>
            <div className="reviewButtons">
                <ReportAbuse id={data.id} userInfo={userInfo}/>
                <AddReview data={data} authEnabled={authEnabled} userInfo={userInfo}/>
            </div>

            {data.reviews.map(review =>
                <Review key={review.id} data={data} review={review}
                        authenticated={authEnabled && userInfo !== null}
                        authored={reviewsUserInteraction.authored.includes(review.id)}
                        liked={reviewsUserInteraction.likes.includes(review.id)}
                        disliked={reviewsUserInteraction.dislikes.includes(review.id)}/>)}
        </div>
    );
}

function Review({data, review, authenticated, authored, liked, disliked}: {
    data: Vocab,
    review: IReview,
    authenticated: boolean,
    authored: boolean,
    liked: boolean,
    disliked: boolean
}) {
    const revalidator = useRevalidator();
    const [hasToggled, setHasToggled] = useState<boolean | null>(null);

    const likes = review.likes +
        (!liked && hasToggled === true ? 1 : 0) + (liked && hasToggled === true ? -1 : 0);
    const dislikes = review.dislikes +
        (!disliked && hasToggled === false ? 1 : 0) + (disliked && hasToggled === false ? -1 : 0);

    async function onLike(isLike: boolean) {
        setHasToggled(isLike);

        await fetch(`/${isLike ? 'like' : 'dislike'}/${data.id}/${review.id}`, {
            method: 'POST'
        });

        setHasToggled(null);
        revalidator.revalidate();
    }

    return (
        <div className="review">
            <div className="flexGap hcMarginBottom1">
                <Rating className="starRating" initialValue={review.rating}
                        readonly={true} showTooltip={false} size={25}/>

                <ThumbsUpDown likes={likes} dislikes={dislikes}
                              liked={hasToggled === true ? !liked : liked}
                              disliked={hasToggled === false ? !disliked : disliked}
                              allowLike={hasToggled === null && authenticated && !authored}
                              allowDislike={hasToggled === null && authenticated && !authored}
                              onLike={() => onLike(true)} onDislike={() => onLike(false)}/>
            </div>

            <p>{review.review}</p>
        </div>
    );
}

function ThumbsUpDown({likes, dislikes, liked, disliked, allowLike, allowDislike, onLike, onDislike}: {
    likes: number;
    dislikes: number;
    liked: boolean;
    disliked: boolean;
    allowLike: boolean;
    allowDislike: boolean;
    onLike: () => void;
    onDislike: () => void;
}) {
    return (
        <div className="hcToggle">
            <button className={'hcButton' + (liked ? ' tabActive' : '')}
                    onClick={onLike} disabled={!allowLike}>
                {likes} {' '}
                <FontAwesomeIcon icon={faThumbsUp}/>
            </button>

            <button className={'hcButton' + (disliked ? ' tabActive' : '')}
                    onClick={onDislike} disabled={!allowDislike}>
                {dislikes} {' '}
                <FontAwesomeIcon icon={faThumbsDown}/>
            </button>
        </div>
    );
}
