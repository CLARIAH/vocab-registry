import dayjs from 'dayjs';
import {ReactElement} from 'react';
import ReactMarkdown from 'react-markdown';
import LocationIconBar from './LocationIconBar';
import LocationInteract from './LocationInteract';
import useLocationFocus from '../hooks/useLocationFocus';
import {Vocab, Version} from '../misc/interfaces';

export default function Description({data, version}: { data: Vocab, version?: Version }) {
    const [locationFocus, onLocationClick] = useLocationFocus();
    const locations = data.locations.concat(...(version?.locations || []));

    return (
        <div>
            {locations.length > 0 && <div className="extraBottomMargin">
                <LocationIconBar locations={locations} onLocationClick={onLocationClick} inline={false}/>
            </div>}

            {data.description && <div className="detailLine extraBottomMargin">
                <ReactMarkdown>{data.description}</ReactMarkdown>
            </div>}

            <div className="detailTable">
                <DetailRow label="Type" values={data.type.syntax}/>
                <DetailRow label="Date issued" values={dayjs(data.date_issued).format('MMM D, YYYY HH:mm')}/>
                <DetailRow label="License" values={data.licenses.map(license =>
                    license.uri ? <a href={license.uri}>{license.label}</a> : <>license.label</>)}/>
                {data.registries &&
                    <DetailRow label="Registry" values={data.registries.map(registry =>
                        <a key={registry.url} href={registry.landing_page || registry.url} target="_blank">
                            {registry.title}
                        </a>
                    )}/>}
            </div>

            <LocationInteract location={locationFocus}/>
        </div>
    );
}

function DetailRow({label, values}: { label: string, values: string | string[] | ReactElement | ReactElement[] }) {
    return (
        <div className="detailRow">
            <div className="labelCell">{label}</div>
            <div className="cell">
                {Array.isArray(values) ? (<ul className="hcNoList">
                    {values.map((v, i) =>
                        <li key={i}>{v}</li>
                    )}
                </ul>) : values}

            </div>
        </div>
    );
}
