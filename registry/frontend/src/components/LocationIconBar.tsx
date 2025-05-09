import {MouseEvent, MouseEventHandler} from 'react';
import {IconDefinition} from '@fortawesome/fontawesome-svg-core';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faArrowUpRightFromSquare, faBook, faDownload, faGear, faHouse} from '@fortawesome/free-solid-svg-icons';
import {Location} from '../misc/interfaces';

interface LocationIconBarProps {
    locations: Location[];
    inline: boolean;
    onLocationClick: (loc: Location, e: MouseEvent<HTMLAnchorElement>) => void;
}

export default function LocationIconBar({locations, inline, onLocationClick}: LocationIconBarProps) {
    return (
        <div className={`iconBar ${inline ? 'inline' : ''}`}>
            {locations.map(loc =>
                <LocationIcon key={loc.location} location={loc} onClick={e => onLocationClick(loc, e)}/>)}
        </div>
    );
}

function LocationIcon({location, onClick}: {
    location: Location,
    onClick?: MouseEventHandler<HTMLAnchorElement>
}) {
    let iconDefinition: IconDefinition, text: string;
    if (location.type === 'homepage') {
        switch (location.recipe) {
            case 'skosmos':
                iconDefinition = faArrowUpRightFromSquare;
                text = 'Open in Skosmos';
                break;
            case 'doc':
                iconDefinition = faBook;
                text = 'Open documentation';
                break;
            default:
                iconDefinition = faHouse;
                text = 'Go to homepage';
                break;
        }
    }
    else {
        switch (location.recipe) {
            case 'sparql':
                iconDefinition = faGear;
                text = 'Query with SPARQL';
                break;
            case 'cache':
                iconDefinition = faDownload;
                text = 'Get cached vocabulary';
                break;
            default:
                iconDefinition = faDownload;
                text = 'Get vocabulary';
                break;
        }
    }

    return (
        <div className="icon">
            <a href={location.location} target="_blank" onClick={onClick}>
                <FontAwesomeIcon icon={iconDefinition}/>
                {text}
            </a>
        </div>
    );
}
