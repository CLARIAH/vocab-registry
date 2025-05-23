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
                <LocationIconBar locations={locations} onLocationClick={onLocationClick}/>
            </div>}

            {data.description && <div className="detailLine extraBottomMargin">
                <ReactMarkdown>{data.description}</ReactMarkdown>
            </div>}

            <div className="detailTables">
                <div className="detailTable">
                    {data.namespace && <DetailRow label="Namespace" values={<>{data.namespace.uri} <span className="pill">{data.namespace.prefix}</span></>}/>}
                    <DetailRow label="Type" values={[data.type.syntax, data.type.entity, data.type.kos].filter(type => type !== null)}/>
                    {data.topic && <DetailRow label="Topics" values={[data.topic.nwo, data.topic.unesco].filter(type => type !== null)}/>}
                    <DetailRow label="Date issued" values={dayjs(data.date_issued).format('MMM D, YYYY HH:mm')}/>
                    {data.languages.length > 0 && <DetailRow label="Languages" values={data.languages}/>}
                    <DetailRow label="License" values={data.licenses.map((license, idx) =>
                        <MaybeHref key={idx} href={license.uri} label={license.label}/>)}/>
                    {data.registries &&
                        <DetailRow label="Registries" values={data.registries.map(registry =>
                            <a key={registry.url} href={registry.landing_page || registry.url} target="_blank">
                                {registry.title}
                            </a>
                        )}/>}
                </div>

                <div className="detailTable">
                    {data.creators.length > 0 &&
                        <DetailRow label="Creators" values={data.creators.map((creator, idx) =>
                            <MaybeHref key={idx} href={creator.uri} label={creator.label}/>)}/>}
                    {data.maintainers.length > 0 &&
                        <DetailRow label="Maintainers" values={data.maintainers.map((maintainer, idx) =>
                            <MaybeHref key={idx} href={maintainer.uri} label={maintainer.label}/>)}/>}
                    {data.contributors.length > 0 &&
                        <DetailRow label="Contributors" values={data.contributors.map((contributor, idx) =>
                            <MaybeHref key={idx} href={contributor.uri} label={contributor.label}/>)}/>}
                </div>
            </div>

            <LocationInteract location={locationFocus}/>
        </div>
    );
}

function MaybeHref({href, label}: { href?: string | null, label: string }) {
    return href ? <a href={href} target="_blank">{label}</a> : label;
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
