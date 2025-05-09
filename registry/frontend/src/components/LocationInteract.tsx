import Yasgui from '../misc/Yasgui';
import {Location} from '../misc/interfaces';

export default function LocationInteract({location}: { location: Location | null }) {
    return (
        <div className={`vocabVersionBody ${location ? 'open' : ''}`}>
            {location && location.recipe === 'sparql' && <VersionYasgui endpoint={location.location}/>}
        </div>
    );
}

function VersionYasgui({endpoint}: { endpoint: string }) {
    const config = {requestConfig: {endpoint}, persistenceId: endpoint};
    return <Yasgui config={config} disableEndpointSelector={true}/>;
}
