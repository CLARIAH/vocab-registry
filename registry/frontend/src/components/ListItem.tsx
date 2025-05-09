import {Link} from 'react-router-dom';
import {useMemo, useState} from 'react';
import {VocabIndex} from '../misc/interfaces';
import {parseTextFromMarkDown} from '../misc/markdown';

const MAX_LENGTH = 500;

export default function ListItem({item}: { item: VocabIndex }) {
    const [showMore, setShowMore] = useState(false);
    const description = useMemo(() => parseTextFromMarkDown(item.description), [item.description]);

    return (
        <div className="hcResultListDetail">
            <div className="justify">
                <h2><Link to={item.id}>{item.title}</Link></h2>
                <span className="pill">{item.syntax}</span>
            </div>

            <div className="detailLine">
                {showMore || description.length <= MAX_LENGTH
                    ? description
                    : description.substring(0, MAX_LENGTH) + '...'}

                {description.length > MAX_LENGTH &&
                    <button className="hcButton" onClick={() => setShowMore(!showMore)}>
                        {showMore ? 'Show less' : 'Show more'}
                    </button>}
            </div>
        </div>
    );
}
