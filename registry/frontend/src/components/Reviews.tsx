import React from 'react';
import {ReviewForm, StarRating} from 'review-component-react';
import ReportAbuse from './ReportAbuse';
import {Review, Vocab} from '../misc/interfaces';
import useAuth from '../hooks/useAuth';
import ThumbUpDown from "./ThumbUpDown";

export default function Reviews({data}: { data: Vocab }) {
    return (
        <div>
            <ListReviews reviews={data.reviews} pageId={data.id}/>
            <AddReview id={data.id} reviews={data.reviews}/>
            <ReportAbuse url_target="/mail"/>
        </div>
    );
}

function ListReviews({reviews, pageId, author}: { reviews: Review[], pageId: number, author: string}) {
    const [authEnabled, userInfo] = useAuth();
    const handleButtonThumbClick = async (action: "LikeAction" | "DislikeAction", author: string) => {
        const response = await fetch(`/thumb/${pageId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
                {
                "author": {"name": author},
                "interactionStatistic": [
                    {
                        "interactionType": action,
                        "author": {"name": userInfo?.email}
                    }
                 ]
            })
        });
        if (!response.ok) {
            throw new Error(`Got an error ${response.status}`);
        }
        const json = await response.json()

        return window.location.reload();
    }

    return (

        <>
            {reviews.map(review => (
                <div className="review" key={review.author}>
                    <div className="hcAlignLeft hcMarginBottom1">
                        <StarRating rate={review.rating} readonly={true} handleRating={() => null}/>
                    </div>
                    <p>{review.review}</p>
                    <ThumbUpDown handleThumbClick={handleButtonThumbClick} likeList={review.like} dislikeList={review.dislike} author={review.author}></ThumbUpDown>
                </div>
            ))}
        </>
    );
}


function AddReview({id, reviews}: { id: string, reviews: []}) {
    const [authEnabled, userInfo] = useAuth();

    const handleRating = async (stars: number, text: string) => {
        const response = await fetch(`/review/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
                {"author": {"name": userInfo?.email},
                    "reviewBody": text, "reviewRating": {"ratingValue": Number(stars)}
                })
        });
        if (!response.ok) {
            throw new Error(`Got an error ${response.status}`);
        }
        const json = await response.json()

        return window.location.reload();
    }

    if (authEnabled && !userInfo) {
        const redirectUri = `/login?redirect-uri=${encodeURIComponent(window.location.href)}`;

        return (
            <p>
                Do you want write a review? Please <a href={redirectUri}>log in</a>.
            </p>
        );
    }
    for (let i = 0; i < reviews.length; i++) {
        if (userInfo?.email == reviews[i].author)
            return (
                <div>
                    <b>Your given review:</b>
                    <div>{reviews[i].review}</div>
                    <b>Your given rating:</b>
                    {reviews[i].rating}
                </div>
            );
    }

    return <ReviewForm handleRating={handleRating}/>;
}
