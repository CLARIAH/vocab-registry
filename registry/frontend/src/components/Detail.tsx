import {useEffect, useState} from 'react';
import {Link, useNavigate, useParams} from 'react-router-dom';
import {Vocab} from '../misc/interfaces';
import Description from './Description';
import Summary from './Summary';
import Reviews from './Reviews';
import Versions from './Versions';

enum ViewOpened { DESCRIPTION, SUMMARY, REVIEWS}

export default function Detail({data}: { data: Vocab }) {
    const navigate = useNavigate();
    const {id, tab} = useParams();
    const [viewOpened, setViewOpened] = useState<ViewOpened>(ViewOpened.DESCRIPTION);
    const [currentVersion, setCurrentVersion] = useState<string | null>(null);

    useEffect(() => {
        switch (tab) {
            case 'summary':
                setViewOpened(ViewOpened.SUMMARY);
                break;
            case 'reviews':
                setViewOpened(ViewOpened.REVIEWS);
                break;
            case 'description':
            default:
                setViewOpened(ViewOpened.DESCRIPTION);
        }
    }, [id, tab]);

    const versions = data.versions
        .sort((a, b) => -1 * a.version.localeCompare(b.version));
    const version = versions.find(v => v.version === currentVersion);

    if (currentVersion === null)
        setCurrentVersion(versions[0].version);

    return (
        <div className="hcContentContainer">
            <div className="hcBasicSideMargin">
                <div className="vocabHeader">
                    <h1>{data.title}</h1>

                    <div className="justify fitContent">
                        <a className="back" href="#" onClick={_ => navigate(-1)}>
                            &larr; Return to previous page
                        </a>

                        <div className="hcToggle">
                            <Link to={`/vocab/${id}/description`}
                                  className={`hcButton ${viewOpened === ViewOpened.DESCRIPTION ? 'tabActive' : ''}`}>
                                Description
                            </Link>
                            <Link to={`/vocab/${id}/summary`}
                                  className={`hcButton ${viewOpened === ViewOpened.SUMMARY ? 'tabActive' : ''}`}>
                                Summary
                            </Link>
                            <Link to={`/vocab/${id}/reviews`}
                                  className={`hcButton ${viewOpened === ViewOpened.REVIEWS ? 'tabActive' : ''}`}>
                                Reviews
                            </Link>
                        </div>
                    </div>
                </div>

                <div className="vocabContentVersions">
                    <div className="vocabContent">
                        {viewOpened === ViewOpened.DESCRIPTION && <Description data={data} version={version}/>}
                        {viewOpened === ViewOpened.SUMMARY && <Summary version={version}/>}
                        {viewOpened === ViewOpened.REVIEWS && <Reviews data={data}/>}
                    </div>

                    {(viewOpened === ViewOpened.DESCRIPTION || viewOpened === ViewOpened.SUMMARY) &&
                        <Versions versions={versions} active={currentVersion} changeVersion={setCurrentVersion}/>}
                </div>
            </div>
        </div>
    );
}
