import {FreeTextFacet, ListFacet} from '@knaw-huc/browser-base-react';

export default function Facets() {
    const defaultFacetProps = {
        url: '/facet',
        flex: false,
        usePost: true,
        isHidden: false
    };

    return <>
        <FreeTextFacet/>
        <ListFacet name="Syntax" field="syntax" {...defaultFacetProps}/>
        <ListFacet name="Type" field="kos" {...defaultFacetProps}/>
        <ListFacet name="Entity" field="entity" {...defaultFacetProps}/>
        <ListFacet name="Topic (NWO)" field="nwo" {...defaultFacetProps}/>
        <ListFacet name="Topic (UNESCO)" field="unesco" {...defaultFacetProps}/>
        <ListFacet name="Registry" field="registries" {...defaultFacetProps}/>
    </>;
}
