import {MouseEvent, MouseEventHandler} from 'react';
import {IconDefinition} from '@fortawesome/fontawesome-svg-core';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faGithub} from '@fortawesome/free-brands-svg-icons'
import {faArrowUpRightFromSquare, faBook, faDownload, faGear, faHouse} from '@fortawesome/free-solid-svg-icons';
import {Location} from '../misc/interfaces';

interface LocationIconBarProps {
    locations: Location[];
    onLocationClick: (loc: Location, e: MouseEvent<HTMLAnchorElement>) => void;
}

export default function LocationIconBar({locations, onLocationClick}: LocationIconBarProps) {
    function sortLocations(a: Location, b: Location) {
        if (!a.recipe) return -1;
        if (!b.recipe) return 1;
        return a.recipe.localeCompare(b.recipe);
    }

    const homepages = locations.filter(loc => loc.type === 'homepage').sort(sortLocations);
    const otherLocations = locations.filter(loc => loc.type !== 'homepage').sort(sortLocations);

    return (
        <>
            <IconBar locations={homepages} onLocationClick={onLocationClick}/>
            <IconBar locations={otherLocations} onLocationClick={onLocationClick}/>
        </>
    );
}

function IconBar({locations, onLocationClick}: LocationIconBarProps) {
    return (
        <div className="iconBar">
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
                if (location.location.startsWith('https://github.com')) {
                    iconDefinition = faGithub;
                    text = 'Go to GitHub repository';
                }
                else {
                    iconDefinition = faHouse;
                    text = 'Go to homepage';
                }
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
