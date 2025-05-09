import {MouseEvent, useState} from 'react';
import {Location} from '../misc/interfaces';

type LocationFocusHook = [
    Location | null,
    (loc: Location, e: MouseEvent<HTMLAnchorElement>) => void
];

export default function useLocationFocus(): LocationFocusHook {
    const [locationFocus, setLocationFocus] = useState<Location | null>(null);

    const onLocationClick = (loc: Location, e: MouseEvent<HTMLAnchorElement>) => {
        if (locationFocus && locationFocus.type === loc.type &&
            locationFocus.recipe === loc.recipe && locationFocus.location === loc.location) {
            setLocationFocus(null);
            e.preventDefault();
        }
        else if (loc.recipe === 'sparql') {
            setLocationFocus(loc);
            e.preventDefault();
        }
    };

    return [locationFocus, onLocationClick];
}
