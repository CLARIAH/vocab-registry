import {FreeTextFacet, ListFacet} from '@knaw-huc/browser-base-react';

export default function Facets() {
    const defaultFacetProps = {
        url: '/facet',
        usePost: true,
        isHidden: false
    };

    return <>
        <FreeTextFacet/>
        <ListFacet name="Syntax" field="syntax" {...defaultFacetProps} flex={false}/>
        <ListFacet name="Type" field="kos" {...defaultFacetProps} flex={false}/>
        <ListFacet name="Entity" field="entity" {...defaultFacetProps} flex={false}/>
        <ListFacet name="Topic (NWO)" field="nwo" {...defaultFacetProps} flex={true}/>
        <ListFacet name="Topic (UNESCO)" field="unesco" {...defaultFacetProps} flex={true}/>
        <ListFacet name="Registry" field="registries" {...defaultFacetProps} flex={false}/>
    </>;
}
