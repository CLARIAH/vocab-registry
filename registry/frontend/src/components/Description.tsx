import dayjs from 'dayjs';
import React, {ReactElement} from 'react';
import ReactMarkdown from 'react-markdown';
import LocationIconBar from './LocationIconBar';
import LocationInteract from './LocationInteract';
import useLocationFocus from '../hooks/useLocationFocus';
import {Publisher, Vocab, VocabVersion} from '../misc/interfaces';

export default function Description({data, version}: { data: Vocab, version?: VocabVersion }) {
    const [locationFocus, onLocationClick] = useLocationFocus();
    const locations = data.locations.concat(...(version?.locations || []));

    return (
        <div>
            {locations.length > 0 && <div className="extraBottomMargin">
                <LocationIconBar locations={locations} onLocationClick={onLocationClick} inline={false}/>
            </div>}

            {data.description && <ReactMarkdown className="detailLine extraBottomMargin">
                {data.description}
            </ReactMarkdown>}

            <div className="detailTable">
                <DetailRow label="Type" values={data.type.syntax}/>
                <DetailRow label="Created" values={dayjs(data.created).format('MMM D, YYYY HH:mm')}/>
                <DetailRow label="Modified" values={dayjs(data.modified).format('MMM D, YYYY HH:mm')}/>
                <DetailRow label="License" values={<a href={data.license.uri}>{data.license.label}</a>}/>
                {data.publishers &&
                    <DetailRow label="Publisher" values={data.publishers.map(publisher =>
                        <a key={publisher.uri} href={publisher.uri} target="_blank">
                            {publisher.name}
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
