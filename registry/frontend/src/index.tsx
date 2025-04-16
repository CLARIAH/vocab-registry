import React from 'react';
import ReactDOM from 'react-dom/client';
import {createBrowserRouter, Outlet, RouteObject, RouterProvider, ScrollRestoration} from 'react-router-dom';
import {
    App,
    PageHeader,
    Search,
    Detail as BrowserDetail,
    createSearchLoader,
    createDetailLoader,
    searchUtils,
    SearchParams
} from '@knaw-huc/browser-base-react';
import Detail from './components/Detail.js';
import Facets from './components/Facets.js';
import ListItem from './components/ListItem.js';
import RegisterNewVocab from './components/RegisterNewVocab.js';

// @ts-ignore
import logo from './assets/logo.svg';
import './index.css';

const title = 'CLARIAH+ FAIR Vocabulary Registry';
const shortTitle = 'FAIR Vocabulary Registry';
const searchLoader = createSearchLoader(searchUtils.getSearchObjectFromParams, '/browse', 10);
const detailLoader = createDetailLoader(id => `/vocab/${id}`);

const pageHeader = <PageHeader
    title={shortTitle}
    logo={<img src={logo} className="logo" alt="Clariah"/>}
    items={<RegisterNewVocab/>}/>;

const routeObject: RouteObject = {
    path: '/',
    element: <App header={pageHeader}>
        <ScrollRestoration/>
        <Outlet/>
    </App>,
    children: [{
        index: true,
        loader: async ({request}) => searchLoader(new URL(request.url).searchParams),
        element: <Search title={title} pageLength={10} withPaging={true}
                         hasIndexPage={false} showSearchHeader={false} updateDocumentTitle={false}
                         searchParams={SearchParams.PARAMS} facetsElement={<Facets/>} ResultItemComponent={ListItem}/>
    }, {
        path: ':id/:tab?',
        loader: async ({params}) => detailLoader(params.id as string),
        element: <BrowserDetail title={title} updateDocumentTitle={false} DetailComponent={Detail}/>
    }]
};

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>
        <RouterProvider router={createBrowserRouter([routeObject])}/>
    </React.StrictMode>
);
