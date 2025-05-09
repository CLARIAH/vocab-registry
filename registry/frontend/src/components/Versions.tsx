import dayjs from 'dayjs';
import {Version} from '../misc/interfaces';

interface VersionsParams {
    versions: Version[];
    active: string | null;
    changeVersion: (version: string) => void;
}

interface VersionParams {
    version: Version;
    isActive: boolean;
    setActive: () => void;
}

export default function Versions({versions, active, changeVersion}: VersionsParams) {
    return (
        <div className="vocabVersions">
            <div className="vocabVersionsHeader">Versions:</div>

            {versions.map(version =>
                <VocabVersion key={version.version} version={version}
                              isActive={active === version.version}
                              setActive={() => changeVersion(version.version)}/>)}
        </div>
    );
}

function VocabVersion({version, isActive, setActive}: VersionParams) {
    return (
        <button className={`vocabVersion ${isActive ? 'vocabVersionActive' : ''}`} onClick={setActive}>
            {version.version}

            {version.validFrom && <div className="vocabVersionDate pill">
                {dayjs(version.validFrom).format('MMM D, YYYY')}
            </div>}
        </button>
    );
}
